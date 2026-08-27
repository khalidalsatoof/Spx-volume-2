# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  لوحة سيولة العقود — تطبيق مستقل تماماً  (v1.0)
═══════════════════════════════════════════════════════════════════════════════
  خدمة منفصلة عن SPX Paper Bot. لا تتصل به ولا تشاركه قاعدة بيانات ولا حالة.
  ⇒ خطرها على المشروع = صفر. تُنشر وتُوقف وتُعدَّل بحرية تامة.

  ── ما تعرضه ──
  N سترايك فوق السعر وN تحته، ولكل سترايك:
     الحجم اليومي (حيّ · يتراكم مع كل صفقة) · العقود المفتوحة (تموضع الأمس)
     سعر الكول · سعر البوت · المسافة عن السعر
  والجانب المهيمن: الكول فوق السعر · البوت تحته.

  ── النشر على Vercel ──
  بنية المستودع:
      api/index.py        ← هذا الملف
      requirements.txt
      vercel.json
  1) استورد المستودع في Vercel → Framework Preset: Other
  2) متغيّر بيئة واحد:  TRADIER_PROD_TOKEN = نفس رمز بيانات السوق
     (رمز قراءة فقط — لا يرسل أوامر ولا يمسّ حساب التنفيذ)
  3) Deploy. لا نوم ولا بداية باردة محسوسة.

  ⚠ الدوال بلا حالة: قد يُنفَّذ كل طلب على نسخة مختلفة.
    لهذا حساب عمود «5د» انتقل إلى المتصفح — يحفظ لقطاته في جهازك
    فيصمد عبر إغلاق الصفحة والنشر، ويعمل على أي منصة.

  ── المسارات ──
  /                 اللوحة (SPY افتراضياً)
  /?u=SPX           تبديل الأداة
  /?u=SPY&n=8&r=15  عدد السترايكات ومدة التحديث بالثواني
  /json             البيانات خاماً
  /debug            حقول Tradier كما ترجع — للتحقق من أسماء الحقول
  /health           فحص سريع
═══════════════════════════════════════════════════════════════════════════════
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

import os
from datetime import datetime

import httpx

TD_BASE    = "https://api.tradier.com/v1"
TD_TOKEN   = os.getenv("TRADIER_PROD_TOKEN", "").strip()
TD_TIMEOUT = float(os.getenv("TD_TIMEOUT", "8"))

LIQ_STRIKES = int(os.getenv("LIQ_STRIKES", "8"))      # عدد السترايكات فوق وتحت
LIQ_CACHE_SEC = float(os.getenv("LIQ_CACHE_SEC", "10"))

# الرمز الأساسي ← (رمز الاستعلام, رمز التسعير)
UNDERLYINGS = {
    "SPY": ("SPY", "SPY"),
    "SPX": ("SPX", "SPX"),
}

_CACHE = {}
_HIST = {}          # {underlying: [(ts, {(strike,side): vol})]}
HIST_KEEP_SEC = 1800
DELTA_WINDOW = 300  # نافذة التغيّر بالثواني (5 دقائق)


def _f(x, d=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def _i(x, d=0):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return d


def _get(path, params):
    if not TD_TOKEN:
        return None, "TRADIER_PROD_TOKEN غير مضبوط"
    try:
        r = httpx.get(f"{TD_BASE}{path}", params=params, timeout=TD_TIMEOUT,
                      headers={"Authorization": f"Bearer {TD_TOKEN}",
                               "Accept": "application/json"})
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:200]}"
        return r.json(), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _listify(node, key):
    if not isinstance(node, dict):
        return []
    v = node.get(key)
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _spot(sym):
    """سعر الأداة. للمؤشرات قد يفشل الاستعلام المباشر ⇒ يرجع None ويُقدَّر لاحقاً."""
    js, err = _get("/markets/quotes", {"symbols": sym, "greeks": "false"})
    if err or not isinstance(js, dict):
        return None, err or "لا رد"
    for q in _listify(js.get("quotes"), "quote"):
        for k in ("last", "close", "prevclose"):
            v = _f(q.get(k))
            if v > 0:
                return v, f"tradier:{k}"
    return None, "لا سعر في الرد"


def _spot_by_parity(rows):
    """تقدير السعر من تكافؤ الخيارات: السترايك الذي يتقارب عنده الكول والبوت."""
    best, gap = None, float("inf")
    for k, r in rows.items():
        c, p = r["call"].get("mid"), r["put"].get("mid")
        if not c or not p:
            continue
        g = abs(c - p)
        if g < gap:
            gap, best = g, k
    if best is None:
        return None
    c, p = rows[best]["call"]["mid"], rows[best]["put"]["mid"]
    return round(best + (c - p), 2)


def fetch(underlying="SPY", expiration=None, n=None, force=False):
    """يجلب السلسلة كاملة ويبني جدول السيولة. يرجع dict جاهزاً للعرض."""
    underlying = str(underlying).upper()
    if underlying not in UNDERLYINGS:
        return {"ok": False, "err": f"رمز غير مدعوم: {underlying}"}
    n = n or LIQ_STRIKES
    key = (underlying, expiration, n)
    now = datetime.now().timestamp()
    c = _CACHE.get(key)
    if not force and c and (now - c["ts"]) < LIQ_CACHE_SEC:
        return c["data"]

    q_sym = UNDERLYINGS[underlying][0]
    exp = expiration or datetime.now().strftime("%Y-%m-%d")

    js, err = _get("/markets/options/chains",
                   {"symbol": q_sym, "expiration": exp, "greeks": "false"})
    if err:
        return {"ok": False, "err": f"تعذّر جلب السلسلة: {err}",
                "underlying": underlying, "expiration": exp}
    raw = _listify(js.get("options") if isinstance(js, dict) else None, "option")
    if not raw:
        return {"ok": False, "err": f"لا سلسلة لـ{q_sym} بتاريخ {exp}",
                "underlying": underlying, "expiration": exp}

    rows = {}
    for o in raw:
        strike = _f(o.get("strike"))
        typ = str(o.get("option_type", "")).lower()
        if strike <= 0 or typ not in ("call", "put"):
            continue
        bid, ask = _f(o.get("bid")), _f(o.get("ask"))
        rows.setdefault(strike, {"call": {}, "put": {}})[typ] = {
            "symbol": o.get("symbol"),
            "bid": bid, "ask": ask,
            "mid": round((bid + ask) / 2.0, 3) if ask > 0 else None,
            "spread": round(ask - bid, 3) if ask > 0 else None,
            "vol": _i(o.get("volume")),
            "oi": _i(o.get("open_interest")),
        }

    spot, spot_src = _spot(UNDERLYINGS[underlying][1])
    if not spot:
        spot = _spot_by_parity(rows)
        spot_src = "parity"
    if not spot:
        return {"ok": False, "err": "تعذّر تحديد سعر الأداة",
                "underlying": underlying, "expiration": exp}

    ks = sorted(rows.keys())
    above = [k for k in ks if k > spot][:n]
    below = [k for k in ks if k <= spot][-n:]
    window = below + above
    spacing = round(min((b - a for a, b in zip(ks, ks[1:])), default=1.0), 2)

    table = []
    for k in sorted(window, reverse=True):
        r = rows[k]
        table.append({
            "strike": k,
            "side": "above" if k > spot else "below",
            "dist": round(k - spot, 2),
            "call_vol": r["call"].get("vol", 0), "call_oi": r["call"].get("oi", 0),
            "call_mid": r["call"].get("mid"),
            "call_bid": r["call"].get("bid"), "call_ask": r["call"].get("ask"),
            "call_spread": r["call"].get("spread"),
            "put_vol": r["put"].get("vol", 0), "put_oi": r["put"].get("oi", 0),
            "put_mid": r["put"].get("mid"),
            "put_bid": r["put"].get("bid"), "put_ask": r["put"].get("ask"),
            "put_spread": r["put"].get("spread"),
        })

    # الجانب المهيمن عند كل سترايك: الكول فوق السعر والبوت تحته
    for t in table:
        up = t["side"] == "above"
        t["main_vol"] = t["call_vol"] if up else t["put_vol"]
        t["main_oi"] = t["call_oi"] if up else t["put_oi"]
        t["main_mid"] = t["call_mid"] if up else t["put_mid"]
        t["main_spread"] = t["call_spread"] if up else t["put_spread"]
        t["spread_pct"] = (round(t["main_spread"] / t["main_mid"] * 100, 1)
                           if t["main_spread"] and t["main_mid"] else None)

    # ── التغيّر خلال DELTA_WINDOW ──
    hist = _HIST.setdefault(underlying, [])
    snap = {(t["strike"], t["side"]): t["main_vol"] for t in table}
    if not hist or (now - hist[-1][0]) >= 30:
        hist.append((now, snap))
    while hist and (now - hist[0][0]) > HIST_KEEP_SEC:
        hist.pop(0)
    ref = None
    for ts, sn in hist:
        if now - ts >= DELTA_WINDOW:
            ref = sn
        else:
            break
    age = None
    if ref is not None:
        for ts, sn in hist:
            if sn is ref:
                age = int(now - ts); break
    for t in table:
        k = (t["strike"], t["side"])
        prev = ref.get(k) if ref else None
        if prev and prev > 0:
            t["delta_pct"] = round((t["main_vol"] - prev) / prev * 100, 1)
            t["delta_abs"] = t["main_vol"] - prev
        else:
            t["delta_pct"] = None
            t["delta_abs"] = None

    tot = sum(t["main_vol"] for t in table) or 1
    for t in table:
        t["share"] = round(100.0 * t["main_vol"] / tot, 1)

    up = [t for t in table if t["side"] == "above"]
    dn = [t for t in table if t["side"] == "below"]
    wall_up = max(up, key=lambda x: x["main_vol"]) if up else None
    wall_dn = max(dn, key=lambda x: x["main_vol"]) if dn else None
    vol_up = sum(t["main_vol"] for t in up)
    vol_dn = sum(t["main_vol"] for t in dn)
    clusters = sorted(table, key=lambda x: -x["main_vol"])[:8]
    pin = max(table, key=lambda x: x["main_oi"]) if table else None
    call_v = sum(t["call_vol"] for t in table)
    put_v = sum(t["put_vol"] for t in table)

    data = {
        "ok": True, "underlying": underlying, "expiration": exp,
        "spot": round(spot, 2), "spot_src": spot_src, "spacing": spacing,
        "ts": datetime.now().strftime("%H:%M:%S"),
        "table": table,
        "wall_up": wall_up, "wall_dn": wall_dn,
        "vol_above": vol_up, "vol_below": vol_dn,
        "ratio_up_dn": round(vol_up / vol_dn, 2) if vol_dn else None,
        "clusters": [{"strike": c["strike"], "vol": c["main_vol"],
                      "side": c["side"]} for c in clusters],
        "pin": {"strike": pin["strike"], "oi": pin["main_oi"],
                "side": pin["side"]} if pin else None,
        "call_vol_total": call_v, "put_vol_total": put_v,
        "pc_ratio": round(put_v / call_v, 2) if call_v else None,
        "delta_window": DELTA_WINDOW, "delta_ref_age": age,
        "total_vol": tot, "contracts": len(raw),
        "has_oi": any(t["call_oi"] or t["put_oi"] for t in table),
    }
    _CACHE[key] = {"ts": now, "data": data}
    return data


def snapshot_row(underlying="SPY", tag="", trade_key=""):
    """صف مضغوط للتسجيل في قاعدة البيانات."""
    d = fetch(underlying)
    if not d.get("ok"):
        return None
    wu, wd = d.get("wall_up"), d.get("wall_dn")
    return {
        "ts_ny": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "underlying": underlying, "tag": tag, "trade_key": trade_key,
        "spot": d["spot"],
        "wall_up_strike": wu["strike"] if wu else None,
        "wall_up_vol": wu["main_vol"] if wu else None,
        "wall_up_dist": wu["dist"] if wu else None,
        "wall_dn_strike": wd["strike"] if wd else None,
        "wall_dn_vol": wd["main_vol"] if wd else None,
        "wall_dn_dist": wd["dist"] if wd else None,
        "vol_above": d["vol_above"], "vol_below": d["vol_below"],
        "ratio_up_dn": d["ratio_up_dn"], "total_vol": d["total_vol"],
        "table_json": str([[t["strike"], t["main_vol"], t["main_oi"]]
                           for t in d["table"]]),
    }


def debug(underlying="SPY"):
    """يعرض أول عقد خاماً كما يرجعه Tradier — للتحقق من أسماء الحقول."""
    q_sym = UNDERLYINGS.get(str(underlying).upper(), ("SPY",))[0]
    exp = datetime.now().strftime("%Y-%m-%d")
    js, err = _get("/markets/options/chains",
                   {"symbol": q_sym, "expiration": exp, "greeks": "false"})
    if err:
        return {"ok": False, "err": err}
    raw = _listify(js.get("options") if isinstance(js, dict) else None, "option")
    if not raw:
        return {"ok": False, "err": "سلسلة فارغة", "expiration": exp}
    return {"ok": True, "count": len(raw), "expiration": exp,
            "fields": sorted(raw[0].keys()), "sample": raw[0]}






app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True, "token": bool(TD_TOKEN),
            "symbols": list(UNDERLYINGS.keys()),
            "strikes": LIQ_STRIKES, "cache_sec": LIQ_CACHE_SEC,
            "delta_window": DELTA_WINDOW,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.get("/json")
def as_json(u: str = "SPY", n: int = 0, exp: str = ""):
    return JSONResponse(fetch(u, expiration=exp or None, n=n or None, force=True))


@app.get("/debug")
def dbg(u: str = "SPY"):
    return JSONResponse(debug(u))


def _page(u, n, r):
    u = u.upper() if u.upper() in UNDERLYINGS else "SPY"
    other = "SPX" if u == "SPY" else "SPY"
    n = n or LIQ_STRIKES
    r = max(5, min(r, 300))
    return (PAGE.replace("__U__", u).replace("__OTHER__", other)
                .replace("__N__", str(n)).replace("__R__", str(r)))


@app.get("/", response_class=HTMLResponse)
def dash(u: str = "SPY", n: int = 0, r: int = 20):
    return _page(u, n, r)


# مسار احتياطي: بعض إعدادات فيرسل تمرّر المسار الكامل للدالة.
# يلتقط أي مسار غير معروف ويوجّهه بحسب نهايته — يجب أن يبقى الأخير.
@app.get("/{full_path:path}", response_class=HTMLResponse)
def catch_all(full_path: str, u: str = "SPY", n: int = 0, r: int = 20):
    p = "/" + (full_path or "").strip("/")
    if p.endswith("/health"):
        return JSONResponse(health())
    if p.endswith("/debug"):
        return JSONResponse(debug(u))
    if p.endswith("/json"):
        return JSONResponse(fetch(u, n=n or None, force=True))
    return _page(u, n, r)


PAGE = """<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0a0d13">
<title>سيولة __U__</title>
<style>
:root{--bg:#0a0d13;--card:#121722;--card2:#161c29;--line:#1e2634;--tx:#e8edf5;
--dim:#7d8ba3;--faint:#4d5a70;--up:#2dd4a0;--dn:#ff5c72;--acc:#4a90ff;--warn:#ffb547}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{margin:0;background:var(--bg);color:var(--tx);
 font-family:-apple-system,BlinkMacSystemFont,system-ui,"SF Pro Text",sans-serif;
 padding:14px 12px 28px;font-variant-numeric:tabular-nums;
 background-image:radial-gradient(900px 420px at 88% -8%,#16233a 0%,transparent 62%),
                  radial-gradient(700px 380px at 6% 104%,#1a1526 0%,transparent 58%);
 background-attachment:fixed}
.hd{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:14px}
.tabs{display:flex;gap:6px}
.tab{padding:7px 16px;border-radius:11px;font-size:13px;font-weight:600;text-decoration:none;
 background:var(--card);color:var(--dim);border:1px solid var(--line);transition:.15s}
.tab.on{background:var(--acc);color:#fff;border-color:var(--acc)}
.px{text-align:left;line-height:1}
.px b{font-size:30px;font-weight:700;letter-spacing:-.6px}
.px s{display:block;font-size:11px;color:var(--dim);text-decoration:none;margin-top:5px}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--up);
 margin-left:5px;vertical-align:middle;animation:p 2s infinite}
@keyframes p{0%,100%{opacity:1}50%{opacity:.25}}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-bottom:13px}
.st{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:9px 8px;text-align:center}
.st u{display:block;font-size:10px;color:var(--dim);text-decoration:none;margin-bottom:4px}
.st b{font-size:15px;font-weight:700}
.tbl{background:var(--card);border:1px solid var(--line);border-radius:15px;overflow:hidden}
.hdr{display:grid;grid-template-columns:44px 1fr 46px 42px 40px;gap:6px;padding:9px 11px;
 font-size:9.5px;color:var(--dim);border-bottom:1px solid var(--line);text-align:center}
.rw{display:grid;grid-template-columns:44px 1fr 46px 42px 40px;gap:6px;padding:7px 11px;
 align-items:center;border-bottom:1px solid rgba(30,38,52,.55);font-size:12px}
.rw:last-child{border-bottom:none}
.rw.pin{background:rgba(255,181,71,.07)}
.sk{font-weight:700;font-size:13px;text-align:center}
.bw{position:relative;height:19px;background:rgba(255,255,255,.035);border-radius:5px;overflow:hidden}
.bf{position:absolute;inset-inline-start:0;top:0;height:100%;border-radius:5px;transition:width .4s ease}
.bv{position:absolute;inset-inline-start:7px;top:0;height:19px;line-height:19px;
 font-size:11px;font-weight:700}
.oi{text-align:center;color:var(--dim);font-size:11.5px}
.oi.big{color:var(--warn);font-weight:700}
.pr{text-align:center;font-size:11.5px;font-weight:600}
.dl{text-align:center;font-size:10.5px;color:var(--faint)}
.dl.hot{color:var(--up);font-weight:700}
.spot{display:flex;align-items:center;justify-content:center;gap:9px;padding:11px;
 background:linear-gradient(90deg,rgba(74,144,255,.10),rgba(74,144,255,.19),rgba(74,144,255,.10));
 border-top:1px solid rgba(74,144,255,.35);border-bottom:1px solid rgba(74,144,255,.35);
 font-size:14px;font-weight:700;color:#8ab6ff}
.chips{margin-top:14px}
.ctitle{font-size:10.5px;color:var(--dim);margin-bottom:7px;padding-inline-start:3px}
.crow{display:flex;gap:6px;overflow-x:auto;padding-bottom:5px;scrollbar-width:none}
.crow::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;min-width:62px;border-radius:11px;padding:8px 9px;text-align:center;
 border:1px solid}
.chip b{display:block;font-size:14px;font-weight:700;line-height:1.15}
.chip s{display:block;font-size:10.5px;text-decoration:none;margin-top:2px;opacity:.85}
.foot{margin-top:15px;font-size:10px;color:var(--faint);line-height:1.75;text-align:center}
.err{padding:26px;text-align:center;color:var(--warn);font-size:13px}
</style></head><body>

<div class="hd">
 <div class="tabs">
  <a class="tab on" href="/?u=__U__&n=__N__&r=__R__">__U__</a>
  <a class="tab" href="/?u=__OTHER__&n=__N__&r=__R__">__OTHER__</a>
 </div>
 <div class="px"><b id="spot">—</b><s><span class="dot"></span><span id="ts">…</span></s></div>
</div>

<div class="stats">
 <div class="st"><u>كول</u><b id="cv" style="color:var(--up)">—</b></div>
 <div class="st"><u>بوت / كول</u><b id="pc">—</b></div>
 <div class="st"><u>بوت</u><b id="pv" style="color:var(--dn)">—</b></div>
</div>

<div class="tbl">
 <div class="hdr"><span>سترايك</span><span>الحجم اليومي</span><span>OI</span><span>سعر</span><span>5د</span></div>
 <div id="body"><div class="err">جارٍ التحميل…</div></div>
</div>

<div class="chips">
 <div class="ctitle">أكبر التجمّعات — من الأكبر إلى الأصغر</div>
 <div class="crow" id="chips"></div>
</div>

<div class="foot">
 الشريط والرقم = حجم تداول اليوم للجانب المهيمن · OI = عقود مفتوحة من إغلاق الأمس<br>
 <span style="color:var(--warn)">◆</span> إطار ذهبي = أعلى OI في النطاق ·
 5د = نمو الحجم في آخر خمس دقائق<br>
 قراءة فقط · لا صلة بالبوت
</div>

<script>
const U="__U__",N=__N__,R=__R__;
const HK="liq_hist_"+U, WIN=300000, KEEP=1800000;
function hist(){try{return JSON.parse(localStorage.getItem(HK))||[]}catch(e){return[]}}
function push(snap){
 let h=hist(), now=Date.now();
 if(!h.length||now-h[h.length-1].t>25000)h.push({t:now,s:snap});
 h=h.filter(x=>now-x.t<KEEP);
 try{localStorage.setItem(HK,JSON.stringify(h))}catch(e){}
 let ref=null;
 for(const x of h){if(now-x.t>=WIN)ref=x.s;else break;}
 return ref;
}
const K=v=>v==null?"—":(v>=1000?(v/1000).toFixed(v>=10000?0:1)+"k":String(v));
const P=v=>v==null?"—":Number(v).toFixed(2);
async function load(){
 try{
  const d=await (await fetch(`/json?u=${U}&n=${N}`)).json();
  const B=document.getElementById("body");
  if(!d.ok){B.innerHTML=`<div class="err">⚠ ${d.err||"تعذّر الجلب"}</div>`;return;}
  document.getElementById("spot").textContent=Number(d.spot).toFixed(2);
  document.getElementById("ts").textContent=d.ts;
  document.getElementById("cv").textContent=K(d.call_vol_total);
  document.getElementById("pv").textContent=K(d.put_vol_total);
  const pc=document.getElementById("pc");
  pc.textContent=d.pc_ratio??"—";
  pc.style.color=d.pc_ratio==null?"var(--tx)":(d.pc_ratio>1.15?"var(--dn)":(d.pc_ratio<0.85?"var(--up)":"var(--tx)"));
  const ref=push(Object.fromEntries(d.table.map(t=>[t.side+t.strike,t.main_vol])));
  for(const t of d.table){
   const pv=ref?ref[t.side+t.strike]:null;
   t.delta_pct=(pv&&pv>0)?Math.round((t.main_vol-pv)/pv*1000)/10:null;
  }
  const mx=Math.max(...d.table.map(t=>t.main_vol),1);
  const pinK=d.pin?d.pin.strike:null;
  let h="",placed=false;
  for(const t of d.table){
   if(!placed&&t.side==="below"){
    h+=`<div class="spot">${U} ${Number(d.spot).toFixed(2)}</div>`;placed=true;}
   const up=t.side==="above",c=up?"#2dd4a0":"#ff5c72";
   const w=Math.max(9,Math.round(100*t.main_vol/mx));
   const hot=t.delta_pct!=null&&t.delta_pct>=8;
   const dtx=t.delta_pct==null?"—":(t.delta_pct>0?"+":"")+t.delta_pct+"%";
   h+=`<div class="rw${t.strike===pinK?" pin":""}">
    <span class="sk" style="color:${c}">${t.strike}</span>
    <span class="bw"><span class="bf" style="width:${w}%;background:${c}30"></span>
      <span class="bv" style="color:${c}">${K(t.main_vol)}</span></span>
    <span class="oi${t.strike===pinK?" big":""}">${K(t.main_oi)}</span>
    <span class="pr" style="color:${c}">${P(t.main_mid)}</span>
    <span class="dl${hot?" hot":""}">${dtx}</span></div>`;
  }
  if(!placed)h+=`<div class="spot">${U} ${Number(d.spot).toFixed(2)}</div>`;
  B.innerHTML=h;
  document.getElementById("chips").innerHTML=d.clusters.map(c=>{
    const up=c.side==="above";
    const col=up?"#2dd4a0":"#ff5c72";
    const bg=up?"rgba(45,212,160,.13)":"rgba(255,92,114,.13)";
    return `<div class="chip" style="background:${bg};border-color:${col}55">
      <b style="color:${col}">${c.strike}</b><s style="color:${col}">${K(c.vol)}</s></div>`;
  }).join("");
 }catch(e){
  document.getElementById("body").innerHTML=`<div class="err">⚠ ${e}</div>`;}
}
load();setInterval(load,R*1000);
</script></body></html>"""
