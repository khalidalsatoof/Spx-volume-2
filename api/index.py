# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  لوحة سيولة العقود — تطبيق مستقل تماماً  (v1.1)
═══════════════════════════════════════════════════════════════════════════════
  خدمة منفصلة عن SPX Paper Bot. لا تتصل به ولا تشاركه قاعدة بيانات ولا حالة.
  ⇒ خطرها على المشروع = صفر. تُنشر وتُوقف وتُعدَّل بحرية تامة.

  ── الجديد في v1.1 ──
  ① دورة موحّدة كل 5 ثوانٍ (كان 20) · إيقاف تلقائي عند إخفاء الصفحة
  ② شريط الجدران العلوي — OI فقط · نطاق ثابت ±0.5% من السعر
     ⇒ لا يختفي الجدار عند تقليص عدد السترايكات المعروضة
     البُعد بالنقاط ملوّن: أحمر إن وقع داخل شريحة الهدف
  ③ شريطا الكول والبوت متوازيان عند كل سترايك + نسبة كول/بوت
  ④ لون السعر: أخضر فوق الافتتاح · أحمر تحته · رمادي خارج الجلسة
     + نسبة التغيّر اليومي
  ⑤ VIX بخط صغير بجانب السعر
  ⑥ أزرار 20 و30 سترايكاً · خط أصغر وصفوف أقصر

  ── شريحة الهدف (من عيّنات المشروع) ──
  TP1 +35% يحتاج 5–13 نقطة SPX (وسيط 9.3) = 0.04%–0.17% من السعر.
  الجدار داخل هذه الشريحة يقع في مسار الهدف ⇒ يُلوَّن أحمر.
  ⚠ ملاحظة لا قاعدة — عيّنتان فقط حتى الآن.

  ── ما تعرضه ──
  N سترايك فوق السعر وN تحته، ولكل سترايك:
     حجم الكول وحجم البوت (شريطان متوازيان) · نسبتهما
     سعر الكول · سعر البوت · العقود المفتوحة · نمو الحجم في آخر 5 دقائق

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
    لهذا حساب عمود «5د» في المتصفح — يحفظ لقطاته في جهازك
    ويُحسب بالطابع الزمني (300 ثانية) لا بعدد اللقطات.

  ── المسارات ──
  /                 اللوحة (SPY افتراضياً)
  /?u=SPX           تبديل الأداة
  /?u=SPY&n=8&r=5   عدد السترايكات ومدة التحديث بالثواني
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

try:
    from zoneinfo import ZoneInfo
    NY = ZoneInfo("America/New_York")
except Exception:
    from datetime import timezone as _tz, timedelta as _td
    NY = _tz(_td(hours=-4))

TD_BASE    = "https://api.tradier.com/v1"
TD_TOKEN   = os.getenv("TRADIER_PROD_TOKEN", "").strip()
TD_TIMEOUT = float(os.getenv("TD_TIMEOUT", "8"))

LIQ_STRIKES = int(os.getenv("LIQ_STRIKES", "10"))      # عدد السترايكات فوق وتحت
LIQ_CACHE_SEC = float(os.getenv("LIQ_CACHE_SEC", "4"))

# نطاق شريط الجدران: ±نسبة مئوية من السعر — ثابت ومستقل عن عدد السترايكات
WALL_RANGE_PCT = float(os.getenv("WALL_RANGE_PCT", "0.5"))

# شريحة الهدف: الحركة اللازمة لبلوغ TP1 +35% (5–13 نقطة SPX من عيّنات المشروع)
TARGET_LO_PCT = float(os.getenv("TARGET_LO_PCT", "0.04"))
TARGET_HI_PCT = float(os.getenv("TARGET_HI_PCT", "0.17"))

# الرمز الأساسي ← (رمز الاستعلام, رمز التسعير)
UNDERLYINGS = {
    "SPY": ("SPY", "SPY"),
    "SPX": ("SPX", "SPX"),
}

VIX_SYMBOL = os.getenv("VIX_SYMBOL", "VIX")

_CACHE = {}
_EXPS = {}          # {underlying: (ts, [تواريخ])}
_VIX = {"ts": 0.0, "val": None}
VIX_CACHE_SEC = 20.0
CUTOFF_NY = (16, 15)   # بعده تُعرض سلسلة الانتهاء التالي
_HIST = {}          # {underlying: [(ts, {(strike,side): vol})]}
HIST_KEEP_SEC = 1800
DELTA_WINDOW = 300  # نافذة التغيّر بالثواني (5 دقائق) — متدحرجة


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
    """سعر الأداة + سعر الافتتاح + الإغلاق السابق.
       للمؤشرات قد يفشل الاستعلام المباشر ⇒ يرجع None ويُقدَّر لاحقاً."""
    js, err = _get("/markets/quotes", {"symbols": sym, "greeks": "false"})
    if err or not isinstance(js, dict):
        return None, err or "لا رد", None, None
    for q in _listify(js.get("quotes"), "quote"):
        op = _f(q.get("open")) or None
        pc = _f(q.get("prevclose")) or None
        for k in ("last", "close", "prevclose"):
            v = _f(q.get(k))
            if v > 0:
                return v, f"tradier:{k}", op, pc
    return None, "لا سعر في الرد", None, None


def _vix():
    """قيمة VIX — مع cache قصير. يفشل بصمت ولا يعطّل اللوحة."""
    now = datetime.now().timestamp()
    if _VIX["val"] is not None and (now - _VIX["ts"]) < VIX_CACHE_SEC:
        return _VIX["val"]
    js, err = _get("/markets/quotes", {"symbols": VIX_SYMBOL, "greeks": "false"})
    if err or not isinstance(js, dict):
        return _VIX["val"]
    for q in _listify(js.get("quotes"), "quote"):
        for k in ("last", "close", "prevclose"):
            v = _f(q.get(k))
            if v > 0:
                _VIX["ts"], _VIX["val"] = now, round(v, 2)
                return _VIX["val"]
    return _VIX["val"]


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


def session_state():
    """حالة الجلسة بتوقيت نيويورك: قبل الافتتاح · مفتوح · بعد الإغلاق · عطلة."""
    ny = datetime.now(NY)
    hm = ny.hour * 60 + ny.minute
    if ny.weekday() >= 5:
        return "closed", "السوق مغلق"
    if hm < 4 * 60:
        return "closed", "خارج التداول"
    if hm < 9 * 60 + 30:
        return "pre", "قبل الافتتاح"
    if hm <= 16 * 60:
        return "open", "السوق مفتوح"
    if hm <= 20 * 60:
        return "post", "بعد الإغلاق"
    return "closed", "خارج التداول"


def _expirations(q_sym, force=False):
    """قائمة تواريخ الانتهاء المتاحة من Tradier — مع cache خمس دقائق."""
    now = datetime.now().timestamp()
    c = _EXPS.get(q_sym)
    if not force and c and (now - c[0]) < 300 and c[1]:
        return c[1]
    js, err = _get("/markets/options/expirations",
                   {"symbol": q_sym, "includeAllRoots": "true"})
    if err or not isinstance(js, dict):
        return []
    out = [str(d) for d in _listify(js.get("expirations"), "date")]
    out.sort()
    if out:
        _EXPS[q_sym] = (now, out)
    return out


def pick_expiration(q_sym):
    """أقرب انتهاء صالح للعرض. يرجع (تاريخ, وسم).

       قبل 16:15 بتوقيت نيويورك ⇒ انتهاء اليوم (الأحجام تتراكم من الافتتاح).
       بعده ⇒ الانتهاء التالي، لأن سلسلة اليوم انتهت وتُصفَّر بعد التسوية."""
    ny = datetime.now(NY)
    today = ny.strftime("%Y-%m-%d")
    after = (ny.hour, ny.minute) >= CUTOFF_NY
    exps = _expirations(q_sym)
    if not exps:
        return today, ("اليوم" if not after else "اليوم (منتهٍ)")
    future = [d for d in exps if d >= today]
    if not future:
        return exps[-1], "آخر متاح"
    if after and future[0] == today and len(future) > 1:
        return future[1], "الجلسة القادمة"
    if future[0] == today:
        return today, "اليوم"
    return future[0], "الجلسة القادمة"


def _walls(rows, spot):
    """أعلى ثلاثة OI فوق السعر وأعلى ثلاثة تحته — من نطاق ثابت ±WALL_RANGE_PCT.

       ⚠ النطاق مستقل تماماً عن عدد السترايكات المعروضة في الجدول،
         وإلا اختفى الجدار كلما قلّص المستخدم العرض.
       ⚠ OI فقط لا الحجم: آلية التثبيت تنبع من المراكز القائمة،
         وOI لا يتغيّر أثناء الجلسة (يُحدَّث بعد الإغلاق)."""
    span = spot * WALL_RANGE_PCT / 100.0
    up, dn = [], []
    for k, r in rows.items():
        d = k - spot
        if abs(d) > span:
            continue
        if d > 0:
            oi = _i(r["call"].get("oi"))
            if oi > 0:
                up.append({"strike": k, "oi": oi, "dist": round(d, 2)})
        else:
            oi = _i(r["put"].get("oi"))
            if oi > 0:
                dn.append({"strike": k, "oi": oi, "dist": round(d, 2)})
    up.sort(key=lambda x: -x["oi"])
    dn.sort(key=lambda x: -x["oi"])

    def mark(lst):
        out = []
        for w in lst[:3]:
            pct = abs(w["dist"]) / spot * 100.0 if spot else 0.0
            w["in_target"] = TARGET_LO_PCT <= pct <= TARGET_HI_PCT
            out.append(w)
        return out

    return mark(up), mark(dn), round(span, 2)


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
    if expiration:
        exp, exp_tag = expiration, "مخصّص"
    else:
        exp, exp_tag = pick_expiration(q_sym)

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

    spot, spot_src, day_open, prev_close = _spot(UNDERLYINGS[underlying][1])
    if not spot:
        spot = _spot_by_parity(rows)
        spot_src, day_open, prev_close = "parity", None, None
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
        cv, pv = r["call"].get("vol", 0), r["put"].get("vol", 0)
        table.append({
            "strike": k,
            "side": "above" if k > spot else "below",
            "dist": round(k - spot, 2),
            "call_vol": cv, "call_oi": r["call"].get("oi", 0),
            "call_mid": r["call"].get("mid"),
            "call_bid": r["call"].get("bid"), "call_ask": r["call"].get("ask"),
            "call_spread": r["call"].get("spread"),
            "put_vol": pv, "put_oi": r["put"].get("oi", 0),
            "put_mid": r["put"].get("mid"),
            "put_bid": r["put"].get("bid"), "put_ask": r["put"].get("ask"),
            "put_spread": r["put"].get("spread"),
            # نسبة الجانبين عند نفس السترايك — مرشّح ضوضاء لا مؤشر اتجاه:
            # القريب من 1 يعني تحوّطاً أو سبريداً ⇒ لا معلومة اتجاهية
            "cp_ratio": (round(cv / pv, 2) if pv else None),
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

    # ── التغيّر خلال DELTA_WINDOW (نسخة الخادم — الاعتماد على نسخة المتصفح) ──
    hist = _HIST.setdefault(underlying, [])
    snap = {(t["strike"], t["side"]): t["main_vol"] for t in table}
    if not hist or (now - hist[-1][0]) >= 8:
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

    oi_up, oi_dn, wall_span = _walls(rows, spot)

    ref_price = day_open or prev_close
    chg_pct = (round((spot - ref_price) / ref_price * 100, 2)
               if ref_price else None)

    data = {
        "ok": True, "underlying": underlying, "expiration": exp,
        "exp_tag": exp_tag,
        "exp_disp": "-".join(reversed(exp.split("-"))),
        "session": session_state()[0], "session_txt": session_state()[1],
        "ny_time": datetime.now(NY).strftime("%H:%M"),
        "spot": round(spot, 2), "spot_src": spot_src, "spacing": spacing,
        "day_open": round(day_open, 2) if day_open else None,
        "prev_close": round(prev_close, 2) if prev_close else None,
        "chg_pct": chg_pct,
        "vix": _vix(),
        "ts": datetime.now().strftime("%H:%M:%S"),
        "table": table,
        "wall_up": wall_up, "wall_dn": wall_dn,
        "oi_up": oi_up, "oi_dn": oi_dn, "wall_span": wall_span,
        "target_lo_pct": TARGET_LO_PCT, "target_hi_pct": TARGET_HI_PCT,
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
    ou = (d.get("oi_up") or [None])[0]
    od = (d.get("oi_dn") or [None])[0]
    return {
        "ts_ny": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "underlying": underlying, "tag": tag, "trade_key": trade_key,
        "spot": d["spot"], "vix": d.get("vix"),
        "wall_up_strike": wu["strike"] if wu else None,
        "wall_up_vol": wu["main_vol"] if wu else None,
        "wall_up_dist": wu["dist"] if wu else None,
        "wall_dn_strike": wd["strike"] if wd else None,
        "wall_dn_vol": wd["main_vol"] if wd else None,
        "wall_dn_dist": wd["dist"] if wd else None,
        "oi_up_strike": ou["strike"] if ou else None,
        "oi_up_oi": ou["oi"] if ou else None,
        "oi_up_dist": ou["dist"] if ou else None,
        "oi_dn_strike": od["strike"] if od else None,
        "oi_dn_oi": od["oi"] if od else None,
        "oi_dn_dist": od["dist"] if od else None,
        "vol_above": d["vol_above"], "vol_below": d["vol_below"],
        "ratio_up_dn": d["ratio_up_dn"], "total_vol": d["total_vol"],
        "table_json": str([[t["strike"], t["call_vol"], t["put_vol"],
                            t["call_oi"], t["put_oi"]] for t in d["table"]]),
    }


def debug(underlying="SPY"):
    """يعرض أول عقد خاماً كما يرجعه Tradier — للتحقق من أسماء الحقول."""
    q_sym = UNDERLYINGS.get(str(underlying).upper(), ("SPY",))[0]
    exp, _tag = pick_expiration(q_sym)
    js, err = _get("/markets/options/chains",
                   {"symbol": q_sym, "expiration": exp, "greeks": "false"})
    if err:
        return {"ok": False, "err": err}
    raw = _listify(js.get("options") if isinstance(js, dict) else None, "option")
    if not raw:
        return {"ok": False, "err": "سلسلة فارغة", "expiration": exp}
    return {"ok": True, "count": len(raw), "expiration": exp,
            "ny_now": datetime.now(NY).strftime("%Y-%m-%d %H:%M"),
            "expirations": _expirations(q_sym)[:6],
            "vix": _vix(),
            "fields": sorted(raw[0].keys()), "sample": raw[0]}






app = FastAPI()


@app.get("/health")
def health():
    return {"ok": True, "token": bool(TD_TOKEN),
            "symbols": list(UNDERLYINGS.keys()),
            "strikes": LIQ_STRIKES, "cache_sec": LIQ_CACHE_SEC,
            "delta_window": DELTA_WINDOW,
            "wall_range_pct": WALL_RANGE_PCT,
            "target_band_pct": [TARGET_LO_PCT, TARGET_HI_PCT],
            "vix": _vix(),
            "ny_now": datetime.now(NY).strftime("%Y-%m-%d %H:%M"),
            "spy_exp": pick_expiration("SPY"), "spx_exp": pick_expiration("SPX"),
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
    n = max(3, min(n or LIQ_STRIKES, 30))
    r = max(3, min(r, 300))
    picks = "".join(
        f'<a class="np{" on" if x == n else ""}" href="/?u={u}&n={x}&r={r}">{x}</a>'
        for x in (5, 8, 10, 12, 15, 20, 30))
    return (PAGE.replace("__U__", u).replace("__OTHER__", other)
                .replace("__PICKS__", picks)
                .replace("__N__", str(n)).replace("__R__", str(r)))


@app.get("/", response_class=HTMLResponse)
def dash(u: str = "SPY", n: int = 0, r: int = 5):
    return _page(u, n, r)


# مسار احتياطي: بعض إعدادات فيرسل تمرّر المسار الكامل للدالة.
# يلتقط أي مسار غير معروف ويوجّهه بحسب نهايته — يجب أن يبقى الأخير.
@app.get("/{full_path:path}", response_class=HTMLResponse)
def catch_all(full_path: str, u: str = "SPY", n: int = 0, r: int = 5):
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
<meta name="apple-mobile-web-app-capable" content="yes">
<title>سيولة __U__</title>
<style>
:root{--bg:#0a0d13;--c1:#121824;--c2:#171f2e;--ln:#212b3c;--tx:#e9eef6;
--dim:#7f8da5;--ft:#4e5c74;--up:#2dd4a0;--dn:#ff5c72;--ac:#4a90ff;--wr:#ffb547}
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{overflow-x:hidden}
body{margin:0;background:var(--bg);color:var(--tx);
 font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
 font-variant-numeric:tabular-nums;
 padding:calc(env(safe-area-inset-top,0px) + 14px) 10px
         calc(env(safe-area-inset-bottom,0px) + 26px);
 background-image:radial-gradient(760px 380px at 90% -10%,#16233a 0,transparent 60%),
                  radial-gradient(620px 340px at 4% 106%,#1b1527 0,transparent 56%);
 background-attachment:fixed}
.hd{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:12px}
.tabs{display:flex;gap:6px;flex:0 0 auto}
.tab{padding:9px 17px;border-radius:12px;font-size:14px;font-weight:600;text-decoration:none;
 background:var(--c1);color:var(--dim);border:1px solid var(--ln)}
.tab.on{background:var(--ac);color:#fff;border-color:var(--ac)}
.px{text-align:left;line-height:1.05;min-width:0}
.px b{font-size:27px;font-weight:700;letter-spacing:-.5px;display:block}
.px .chg{font-size:12px;font-weight:700;margin-top:3px;display:block}
.px .sub{font-size:10.5px;color:var(--dim);margin-top:4px;white-space:nowrap}
.px .vix{font-size:10px;color:var(--dim);margin-inline-start:5px}
.bdg{display:inline-block;padding:2px 7px;border-radius:6px;font-size:9.5px;font-weight:700;
 margin-inline-start:5px;vertical-align:1px}
.exp{background:var(--c1);border:1px solid var(--ln);border-radius:11px;
 padding:8px 11px;margin-bottom:8px;font-size:11.5px;color:var(--dim);
 display:flex;justify-content:space-between;align-items:center;gap:8px}
.exp b{color:var(--tx);font-weight:600}
.picks{display:flex;align-items:center;gap:4px;margin-bottom:9px;font-size:10px;color:var(--dim)}
.picks span{margin-inline-end:2px}
.np{flex:1;text-align:center;padding:6px 0;border-radius:8px;text-decoration:none;
 background:var(--c1);border:1px solid var(--ln);color:var(--dim);font-size:11.5px;font-weight:600}
.np.on{background:var(--ac);color:#fff;border-color:var(--ac)}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:8px}
.st{background:var(--c1);border:1px solid var(--ln);border-radius:12px;padding:9px 4px;text-align:center}
.st u{display:block;font-size:9.5px;color:var(--dim);text-decoration:none;margin-bottom:4px}
.st b{font-size:16px;font-weight:700}

/* ── شريط الجدران: OI فقط · نطاق ثابت مستقل عن عدد السترايكات ── */
.walls{margin-bottom:9px;border:1px solid var(--ln);border-radius:11px;overflow:hidden}
.wrow{display:flex;align-items:center;gap:5px;padding:5px 8px;overflow-x:auto;
 scrollbar-width:none;white-space:nowrap}
.wrow::-webkit-scrollbar{display:none}
.wrow.up{background:rgba(45,212,160,.10);border-bottom:1px solid var(--ln)}
.wrow.dn{background:rgba(255,92,114,.10)}
.wtag{flex:0 0 auto;font-size:11px;font-weight:700;opacity:.85}
.witem{flex:0 0 auto;font-size:10.5px;font-weight:600;
 background:rgba(255,255,255,.05);border-radius:7px;padding:3px 7px}
.witem u{text-decoration:none;font-weight:700}
.witem s{text-decoration:none;opacity:.75;font-size:9.5px;margin-inline-start:3px}
.witem s.hit{color:var(--dn);opacity:1;font-weight:700}

.tbl{background:var(--c1);border:1px solid var(--ln);border-radius:15px;overflow:hidden}
.hdr{display:grid;grid-template-columns:38px 1fr 32px 44px 36px;gap:4px;padding:6px 8px;
 font-size:8.5px;color:var(--dim);text-align:center;border-bottom:1px solid var(--ln)}
.rw{display:grid;grid-template-columns:38px 1fr 32px 44px 36px;gap:4px;padding:4px 8px;
 align-items:center;border-bottom:1px solid rgba(33,43,60,.5)}
.rw:last-child{border-bottom:none}
.rw.pin{background:rgba(255,181,71,.075)}
.sk{font-weight:700;font-size:12px;text-align:center}
.bw2{display:flex;flex-direction:column;gap:2px}
.bw{position:relative;height:11px;background:rgba(255,255,255,.032);border-radius:3px;overflow:hidden}
.bf{position:absolute;inset-inline-start:0;top:0;height:100%;border-radius:3px;transition:width .4s}
.bv{position:absolute;inset-inline-start:5px;top:0;line-height:11px;font-size:8.5px;font-weight:700}
.cp{text-align:center;font-size:9.5px;font-weight:700}
.pp{text-align:center;line-height:1.3;font-size:9.5px;font-weight:600}
.pp i{font-style:normal;display:block}
.rt{text-align:center;line-height:1.3;font-size:8.5px;color:var(--dim)}
.rt i{font-style:normal;display:block}
.rt .hot{color:var(--up);font-weight:700}
.rt .big{color:var(--wr);font-weight:700}
.spot{display:flex;align-items:center;justify-content:center;gap:8px;padding:9px 8px;
 font-size:13px;font-weight:700;color:#8ab6ff;
 background:linear-gradient(90deg,rgba(74,144,255,.09),rgba(74,144,255,.2),rgba(74,144,255,.09));
 border-top:1px solid rgba(74,144,255,.4);border-bottom:1px solid rgba(74,144,255,.4)}
.spot.dim{color:#8c96ab;background:rgba(255,255,255,.035);
 border-color:rgba(255,255,255,.13);border-style:dashed}
.ctitle{font-size:10.5px;color:var(--dim);margin:14px 3px 7px}
.crow{display:flex;gap:6px;overflow-x:auto;padding-bottom:6px;scrollbar-width:none}
.crow::-webkit-scrollbar{display:none}
.chip{flex:0 0 auto;min-width:64px;border-radius:12px;padding:9px;text-align:center;border:1px solid}
.chip b{display:block;font-size:14px;font-weight:700;line-height:1.15}
.chip s{display:block;font-size:10.5px;text-decoration:none;margin-top:3px;opacity:.9}
.foot{margin-top:14px;font-size:9.5px;color:var(--ft);line-height:1.85;text-align:center}
.err{padding:26px;text-align:center;color:var(--wr);font-size:13px}
</style></head><body>

<div class="hd">
 <div class="tabs">
  <a class="tab on" href="/?u=__U__&n=__N__&r=__R__">__U__</a>
  <a class="tab" href="/?u=__OTHER__&n=__N__&r=__R__">__OTHER__</a>
 </div>
 <div class="px"><b id="spot">—</b>
  <span class="chg" id="chg"></span>
  <div class="sub"><span id="ses" class="bdg">…</span> <span id="ts">…</span>
   <span class="vix" id="vix"></span></div></div>
</div>

<div class="exp"><span>سلسلة العقود</span><b id="exp">…</b></div>
<div class="picks"><span>سترايكات</span>__PICKS__</div>

<div class="stats">
 <div class="st"><u>كول</u><b id="cv" style="color:var(--up)">—</b></div>
 <div class="st"><u>بوت / كول</u><b id="pc">—</b></div>
 <div class="st"><u>بوت</u><b id="pv" style="color:var(--dn)">—</b></div>
</div>

<div class="walls">
 <div class="wrow up" id="wup"><span class="wtag" style="color:var(--up)">▲ OI</span></div>
 <div class="wrow dn" id="wdn"><span class="wtag" style="color:var(--dn)">▼ OI</span></div>
</div>

<div class="tbl">
 <div class="hdr"><span>سترايك</span><span>كول / بوت</span><span>نسبة</span>
  <span>السعر</span><span>OI · 5د</span></div>
 <div id="body"><div class="err">جارٍ التحميل…</div></div>
</div>

<div class="ctitle">أكبر التجمّعات — من الأكبر إلى الأصغر</div>
<div class="crow" id="chips"></div>

<div class="foot">
الشريطان = حجم اليوم للكول (أخضر) والبوت (أحمر) · <span style="color:var(--wr)">◆</span> أعلى OI في النطاق<br>
شريط OI = أعلى ثلاثة مراكز قائمة فوق وتحت · البُعد بالنقاط · أحمر = داخل مسار الهدف<br>
5د = نمو الحجم في آخر خمس دقائق · يُحسب في جهازك<br>
قراءة فقط · لا صلة بالبوت
</div>

<script>
const U="__U__",N=__N__,R=__R__;
const HK="liq_hist_"+U, WIN=300000, KEEP=1800000;
const K=v=>v==null?"—":(v>=1000?(v/1000).toFixed(v>=10000?0:1)+"k":String(v));
const P=v=>v==null?"—":Number(v).toFixed(2);
function hist(){try{return JSON.parse(localStorage.getItem(HK))||[]}catch(e){return[]}}
function push(snap){
 let h=hist(),now=Date.now();
 // الحفظ كل 8 ثوانٍ يكفي لدورة 5 ثوانٍ · النافذة تُحسب بالطابع الزمني لا بالعدّ
 if(!h.length||now-h[h.length-1].t>8000)h.push({t:now,s:snap});
 h=h.filter(x=>now-x.t<KEEP);
 try{localStorage.setItem(HK,JSON.stringify(h))}catch(e){}
 let ref=null;
 for(const x of h){if(now-x.t>=WIN)ref=x.s;else break;}
 return ref;
}
const SES={open:["var(--up)","rgba(45,212,160,.16)"],
           pre:["var(--wr)","rgba(255,181,71,.16)"],
           post:["var(--ac)","rgba(74,144,255,.16)"],
           closed:["#8c96ab","rgba(255,255,255,.09)"]};
function walls(el,list,col,tag){
 const head=`<span class="wtag" style="color:${col}">${tag}</span>`;
 if(!list||!list.length){el.innerHTML=head+`<span class="witem" style="opacity:.5">—</span>`;return;}
 el.innerHTML=head+list.map(w=>{
  const d=(w.dist>0?"+":"")+w.dist;
  return `<span class="witem"><u style="color:${col}">${w.strike}</u>
   <s>${K(w.oi)}</s><s class="${w.in_target?"hit":""}">${d}</s></span>`;
 }).join("");
}
async function load(){
 const B=document.getElementById("body");
 try{
  const d=await (await fetch(`/json?u=${U}&n=${N}`)).json();
  if(!d.ok){B.innerHTML=`<div class="err">⚠ ${d.err||"تعذّر الجلب"}</div>`;return;}
  // ── السعر ولونه ونسبة التغيّر ──
  const sp=document.getElementById("spot"),cg=document.getElementById("chg");
  sp.textContent=Number(d.spot).toFixed(2);
  const live=d.session==="open";
  const ref=d.day_open??d.prev_close;
  if(live&&ref){
   const upx=d.spot>=ref;
   sp.style.color=upx?"var(--up)":"var(--dn)";
   cg.style.color=upx?"var(--up)":"var(--dn)";
   cg.textContent=(upx?"▲ +":"▼ ")+(d.chg_pct??0)+"%";
  }else{
   sp.style.color="var(--tx)";
   cg.style.color="var(--dim)";
   cg.textContent=(d.chg_pct==null)?"":((d.chg_pct>0?"+":"")+d.chg_pct+"%");
  }
  document.getElementById("vix").textContent=d.vix?("VIX "+d.vix):"";
  document.getElementById("ts").textContent=d.ny_time+" نيويورك";
  const sb=document.getElementById("ses"),sc=SES[d.session]||SES.closed;
  sb.textContent=d.session_txt;sb.style.color=sc[0];sb.style.background=sc[1];
  document.getElementById("exp").textContent=`ينتهي ${d.exp_disp} · ${d.exp_tag}`;
  document.getElementById("cv").textContent=K(d.call_vol_total);
  document.getElementById("pv").textContent=K(d.put_vol_total);
  const pc=document.getElementById("pc");
  pc.textContent=d.pc_ratio??"—";
  pc.style.color=d.pc_ratio==null?"var(--tx)":(d.pc_ratio>1.15?"var(--dn)":(d.pc_ratio<.85?"var(--up)":"var(--tx)"));
  // ── شريط الجدران ──
  walls(document.getElementById("wup"),d.oi_up,"#2dd4a0","▲ OI");
  walls(document.getElementById("wdn"),d.oi_dn,"#ff5c72","▼ OI");
  // ── نمو 5د ──
  const rf=push(Object.fromEntries(d.table.map(t=>[t.side+t.strike,t.main_vol])));
  for(const t of d.table){const pv=rf?rf[t.side+t.strike]:null;
   t.dp=(pv&&pv>0)?Math.round((t.main_vol-pv)/pv*1000)/10:null;}
  const mx=Math.max(...d.table.map(t=>Math.max(t.call_vol,t.put_vol)),1);
  const pk=d.pin?d.pin.strike:null;
  let h="",placed=false;
  for(const t of d.table){
   if(!placed&&t.side==="below"){
    h+=`<div class="spot${live?"":" dim"}">${U} ${Number(d.spot).toFixed(2)}</div>`;
    placed=true;}
   const up=t.side==="above",c=up?"#2dd4a0":"#ff5c72";
   const wc=Math.max(6,Math.round(100*t.call_vol/mx));
   const wp=Math.max(6,Math.round(100*t.put_vol/mx));
   const hot=t.dp!=null&&t.dp>=8;
   const dt=t.dp==null?"—":(t.dp>0?"+":"")+t.dp+"%";
   // نسبة كول/بوت: القريب من 1 يعني توازناً ⇒ تحوّط لا رأي اتجاهي
   const cr=t.cp_ratio;
   const crc=(cr==null)?"var(--dim)":(cr>=1.6?"#2dd4a0":(cr<=0.62?"#ff5c72":"var(--dim)"));
   h+=`<div class="rw${t.strike===pk?" pin":""}">
    <span class="sk" style="color:${c}">${t.strike}</span>
    <span class="bw2">
     <span class="bw"><span class="bf" style="width:${wc}%;background:#2dd4a02e"></span>
      <span class="bv" style="color:#2dd4a0">${K(t.call_vol)}</span></span>
     <span class="bw"><span class="bf" style="width:${wp}%;background:#ff5c722e"></span>
      <span class="bv" style="color:#ff5c72">${K(t.put_vol)}</span></span>
    </span>
    <span class="cp" style="color:${crc}">${cr==null?"—":cr}</span>
    <span class="pp"><i style="color:#2dd4a0">${P(t.call_mid)}</i>
     <i style="color:#ff5c72">${P(t.put_mid)}</i></span>
    <span class="rt"><i class="${t.strike===pk?"big":""}">${K(t.main_oi)}</i>
     <i class="${hot?"hot":""}">${dt}</i></span></div>`;
  }
  if(!placed)h+=`<div class="spot dim">${U} ${Number(d.spot).toFixed(2)}</div>`;
  B.innerHTML=h;
  document.getElementById("chips").innerHTML=d.clusters.map(c=>{
   const up=c.side==="above",col=up?"#2dd4a0":"#ff5c72";
   const bg=up?"rgba(45,212,160,.13)":"rgba(255,92,114,.13)";
   return `<div class="chip" style="background:${bg};border-color:${col}55">
    <b style="color:${col}">${c.strike}</b><s style="color:${col}">${K(c.vol)}</s></div>`;
  }).join("");
 }catch(e){B.innerHTML=`<div class="err">⚠ ${e}</div>`;}
}
// ── دورة التحديث: تتوقف عند إخفاء الصفحة (توفير بطارية) ──
let TIMER=null;
function start(){if(TIMER)return;load();TIMER=setInterval(load,R*1000);}
function stop(){if(TIMER){clearInterval(TIMER);TIMER=null;}}
document.addEventListener("visibilitychange",()=>{document.hidden?stop():start();});
start();
</script></body></html>"""
