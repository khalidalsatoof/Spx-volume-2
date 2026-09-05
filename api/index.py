# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  لوحة سيولة العقود — تطبيق مستقل تماماً  (v1.4)
═══════════════════════════════════════════════════════════════════════════════
  خدمة منفصلة عن SPX Paper Bot. لا تتصل به ولا تشاركه قاعدة بيانات ولا حالة.
  ⇒ خطرها على المشروع = صفر. تُنشر وتُوقف وتُعدَّل بحرية تامة.

  ── الجديد في v1.3.2 ──
  ⑯ قائمة التجمّعات إلى ثمانية · عمود OI الخام بدل نسبة الحجم/OI

  ⚠⚠ لماذا حُذفت نسبة «الحجم ÷ OI» — نتيجة محاكاة زمنية على 25 لقطة حقيقية:
      الحجم يتراكم طوال اليوم وOI ثابت ⇒ النسبة تنزاح مع الساعة لا مع الأهمية.
      وسيط النسبة عبر اليوم: 09:35 = 1.0×  ·  11:30 = 3.3×  ·  15:45 = 6.9×
      ⇒ أي عتبة ثابتة (مثل ≥3× = جديد) تنطفئ صباحاً وتضيء على كل شيء عصراً.
      وحتى النسبة المطبّعة بوسيط اللحظة تنزاح: السترايك 7700 يوم 2 سبتمبر
      خام 1.3× ← 15.8× ومطبّع 1.17 ← 2.52 ⇒ لا تصلح كمقياس ثابت.

  ✅ البديل المُثبَت: «الحصة من الحجم الكلي» — قيست على 25 لقطة عبر ثلاثة أيام
      المدى 2.9%–9.0% والوسيط 5.0% بلا أي انزياح زمني. وهي معروضة أصلاً
      كطول الشريط ⇒ لا حاجة لعمود رقمي يكرّرها.
  ✅ وOI الخام هو مقياس الرسوخ: OI عالٍ = التزام قائم من أمس (مصدر آلية التثبيت)
      OI منخفض مع حجم عالٍ = نشاط اليوم بلا مخزون خلفه ⇒ تجمّع هشّ.
      ⚠ الرقم المنخفض في OI هو الضعيف — لا العكس. (تصحيح تلوين v1.3.1)

  ── v1.3 ──
  ⑩ قائمة التجمّعات المدمجة: كول وبوت في قائمة واحدة مرتّبة بالحجم
     مع البُعد بالنقاط والنمو — تحلّ محل الشريط الأفقي القديم
  ⑪ «تركّز ▲ 62% · 1.8×» في الرأس — وصف تركّز النشاط لا رأي اتجاهي
     ⚠ «فوق/تحت» لا «كول/بوت»: التجمّع فوق السعر يُحسب كولاً بحكم التعريف
  ⑫ المضاعف بوسيط متدحرج (نوافذ خمس دقائق داخل الجلسة) بدل عتبة ثابتة
     ⇒ 30k صباحاً ليست 30k عصراً · يُخفى قبل 10:00 NY (الأساس شبه صفر)
  ⑬ نسبة التغيّر من إغلاق الأمس لا من الافتتاح ⇒ الفجوة تُحتسب
     + شريط نطاق اليوم (أدنى · السعر · أعلى) — قراءة موقع السعر بنظرة
  ⑭ تاريخ منفصل تماماً لكل أداة + مؤشر جاهزية بدل رقم مضلّل
  ⑮ cache VIX إلى 60 ثانية · تباطؤ الدورة خارج الجلسة · حذف نص التذييل

  ── v1.2 ──
  ⑦ /snap — لقطة مفردة للتسجيل (JSON أو نص) · اتجاه واحد · بلا حفظ
  ⑧ VIX وVIX0D في سطر مستقل تحت الحالة (لا يُقصّ مهما طال) · VIX1D_SYMBOL
  ⑨ نسبة كول/بوت تُعرض رمادية باهتة إذا كان أضعف الجانبين < CP_MIN_SIDE

  ── v1.1 ──
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
  /snap?u=SPX       لقطة سيولة واحدة للتسجيل — نقطة الاتصال الوحيدة بالبوت
  /snap?u=SPX&fmt=txt   نفس اللقطة كنص عربي جاهز للنسخ
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
# VIX0D — تقلّب يوم واحد. اسم الرمز عند Tradier قد يختلف عن TradingView.
# جرّب VIX0D · VIX1D · $VIX0D عبر متغيّر البيئة، وراجع /health بعد النشر.
VIX1D_SYMBOL = os.getenv("VIX1D_SYMBOL", "VIX0D")

# دون هذا العدد من العقود على أضعف الجانبين تُعدّ نسبة كول/بوت بلا مضمون
CP_MIN_SIDE = int(os.getenv("CP_MIN_SIDE", "1000"))

_CACHE = {}
_EXPS = {}          # {underlying: (ts, [تواريخ])}
_VIX = {"ts": 0.0, "val": None}
_VIX1D = {"ts": 0.0, "val": None}
VIX_CACHE_SEC = 60.0
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
    """سعر الأداة + الافتتاح + إغلاق الأمس + أعلى وأدنى اليوم.

       يرجع (spot, src, open, prev_close, high, low).
       للمؤشرات قد يفشل الاستعلام المباشر ⇒ يرجع None ويُقدَّر لاحقاً."""
    js, err = _get("/markets/quotes", {"symbols": sym, "greeks": "false"})
    if err or not isinstance(js, dict):
        return None, err or "لا رد", None, None, None, None
    for q in _listify(js.get("quotes"), "quote"):
        op = _f(q.get("open")) or None
        pc = _f(q.get("prevclose")) or None
        hi = _f(q.get("high")) or None
        lo = _f(q.get("low")) or None
        for k in ("last", "close", "prevclose"):
            v = _f(q.get(k))
            if v > 0:
                return v, f"tradier:{k}", op, pc, hi, lo
    return None, "لا سعر في الرد", None, None, None, None


def _quote_last(sym, store):
    """آخر سعر لرمز مؤشر — مع cache قصير. يفشل بصمت ولا يعطّل اللوحة."""
    now = datetime.now().timestamp()
    if store["val"] is not None and (now - store["ts"]) < VIX_CACHE_SEC:
        return store["val"]
    js, err = _get("/markets/quotes", {"symbols": sym, "greeks": "false"})
    if err or not isinstance(js, dict):
        return store["val"]
    for q in _listify(js.get("quotes"), "quote"):
        for k in ("last", "close", "prevclose"):
            v = _f(q.get(k))
            if v > 0:
                store["ts"], store["val"] = now, round(v, 2)
                return store["val"]
    return store["val"]


def _vix():
    return _quote_last(VIX_SYMBOL, _VIX)


def _vix1d():
    return _quote_last(VIX1D_SYMBOL, _VIX1D)


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

    spot, spot_src, day_open, prev_close, day_high, day_low = _spot(
        UNDERLYINGS[underlying][1])
    if not spot:
        spot = _spot_by_parity(rows)
        spot_src, day_open, prev_close = "parity", None, None
        day_high = day_low = None
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
            # النسبة بلا مضمون إذا كان أضعف الجانبين صغيراً ⇒ تُعرض رمادية
            "cp_weak": (min(cv, pv) < CP_MIN_SIDE),
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

    # [v1.3] التغيّر اليومي يُقاس من **إغلاق الأمس** لا من الافتتاح،
    #        وإلا اختفت الفجوة من الرقم تماماً. ويُعرض تغيّر الافتتاح بجانبه
    #        لأنه يجيب سؤالاً مختلفاً: أين السعر من بداية الجلسة؟
    chg_pct = (round((spot - prev_close) / prev_close * 100, 2)
               if prev_close else None)
    chg_open_pct = (round((spot - day_open) / day_open * 100, 2)
                    if day_open else None)
    gap_pct = (round((day_open - prev_close) / prev_close * 100, 2)
               if day_open and prev_close else None)

    data = {
        "ok": True, "underlying": underlying, "expiration": exp,
        "exp_tag": exp_tag,
        "exp_disp": "-".join(reversed(exp.split("-"))),
        "session": session_state()[0], "session_txt": session_state()[1],
        "ny_time": datetime.now(NY).strftime("%H:%M"),
        "spot": round(spot, 2), "spot_src": spot_src, "spacing": spacing,
        "day_open": round(day_open, 2) if day_open else None,
        "prev_close": round(prev_close, 2) if prev_close else None,
        "chg_pct": chg_pct, "chg_open_pct": chg_open_pct, "gap_pct": gap_pct,
        "day_high": round(day_high, 2) if day_high else None,
        "day_low": round(day_low, 2) if day_low else None,
        "vix": _vix(), "vix1d": _vix1d(),
        "ts": datetime.now().strftime("%H:%M:%S"),
        "table": table,
        "wall_up": wall_up, "wall_dn": wall_dn,
        "oi_up": oi_up, "oi_dn": oi_dn, "wall_span": wall_span,
        "target_lo_pct": TARGET_LO_PCT, "target_hi_pct": TARGET_HI_PCT,
        "vol_above": vol_up, "vol_below": vol_dn,
        "ratio_up_dn": round(vol_up / vol_dn, 2) if vol_dn else None,
        # [v1.3] قائمة مدمجة: كول وبوت معاً مرتّبين بالحجم، مع البُعد والـOI
        "clusters": [{"strike": c["strike"], "vol": c["main_vol"],
                      "side": c["side"], "dist": c["dist"],
                      "oi": c["main_oi"],
                      "share": round(100.0 * c["main_vol"] / tot, 1)}
                     for c in clusters],
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


def snapshot_row(underlying="SPX", tag="", sig_key="", n=30):
    """لقطة سيولة مضغوطة للتسجيل — تُستدعى من البوت عبر /snap.

       ⚠ لا تحفظ شيئاً: دوال Vercel بلا حالة. الحفظ مسؤولية المُستدعي.
       ⚠ السيولة تُقرأ من SPX (أضخم وأوضح)، ويُحفظ سعر SPY في نفس الصف
         لأن صفقاتنا بوحدات SPY والنسبة تنزاح مع الأرباح الموزّعة."""
    d = fetch(underlying, n=n, force=True)
    if not d.get("ok"):
        return {"ok": False, "err": d.get("err", "تعذّر الجلب"),
                "ts_ny": datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S"),
                "sig_key": sig_key, "tag": tag}

    ou = (d.get("oi_up") or [None])[0]
    od = (d.get("oi_dn") or [None])[0]
    spot = d["spot"]

    # النسبة عند أقرب سترايك للسعر
    atm = min(d["table"], key=lambda t: abs(t["dist"])) if d["table"] else None

    # السعر المقابل للأداة الأخرى — للتحويل بين SPX وSPY لاحقاً
    other = "SPY" if underlying == "SPX" else "SPX"
    o_spot, _src, _op, _pc, _hi, _lo = _spot(UNDERLYINGS[other][1])
    ratio = round(spot / o_spot, 4) if o_spot else None

    return {
        "ok": True,
        "ts_ny": datetime.now(NY).strftime("%Y-%m-%d %H:%M:%S"),
        "sig_key": sig_key, "tag": tag,
        "underlying": underlying, "expiration": d["expiration"],
        "session": d["session"],
        # ── البيئة ──
        "spot": spot,
        "spot_other": round(o_spot, 2) if o_spot else None,
        "other_symbol": other,
        "px_ratio": ratio,
        "day_open": d.get("day_open"), "chg_pct": d.get("chg_pct"),
        "vix": d.get("vix"), "vix1d": d.get("vix1d"),
        # ── الجدران (OI · نطاق ثابت ±WALL_RANGE_PCT) ──
        "oi_up_strike": ou["strike"] if ou else None,
        "oi_up_oi": ou["oi"] if ou else None,
        "oi_up_dist": ou["dist"] if ou else None,
        "oi_up_in_target": ou["in_target"] if ou else None,
        "oi_dn_strike": od["strike"] if od else None,
        "oi_dn_oi": od["oi"] if od else None,
        "oi_dn_dist": od["dist"] if od else None,
        "oi_dn_in_target": od["in_target"] if od else None,
        "wall_span": d.get("wall_span"),
        # ── التدفّق ──
        "vol_above": d["vol_above"], "vol_below": d["vol_below"],
        "ratio_up_dn": d["ratio_up_dn"],
        "call_vol_total": d["call_vol_total"], "put_vol_total": d["put_vol_total"],
        "pc_ratio": d["pc_ratio"],
        "atm_strike": atm["strike"] if atm else None,
        "atm_cp_ratio": atm["cp_ratio"] if atm else None,
        "atm_cp_weak": atm["cp_weak"] if atm else None,
        # ── الخام: يسمح بإعادة الحساب بأي تعريف لاحق بلا جمع جديد ──
        "cols": "strike,call_vol,put_vol,call_oi,put_oi",
        "table_json": [[t["strike"], t["call_vol"], t["put_vol"],
                        t["call_oi"], t["put_oi"]] for t in d["table"]],
    }


def snap_text(row):
    """صياغة نصية مختصرة للصق في تيليجرام أو Excel."""
    if not row.get("ok"):
        return "⚠ تعذّر جلب السيولة: " + str(row.get("err"))
    L = []
    v = f"VIX {row['vix']}" if row.get("vix") else "VIX —"
    if row.get("vix1d"):
        v += f" · 0D {row['vix1d']}"
    L.append(f"📊 سيولة {row['underlying']} {row['spot']} · {v}")
    if row.get("spot_other"):
        L.append(f"{row['other_symbol']} {row['spot_other']} · النسبة {row['px_ratio']}")
    if row.get("oi_up_strike"):
        m = " ⚠ في مسار الهدف" if row.get("oi_up_in_target") else ""
        L.append(f"▲ {row['oi_up_strike']} · OI {row['oi_up_oi']} · "
                 f"{row['oi_up_dist']:+g}{m}")
    if row.get("oi_dn_strike"):
        m = " ⚠ في مسار الهدف" if row.get("oi_dn_in_target") else ""
        L.append(f"▼ {row['oi_dn_strike']} · OI {row['oi_dn_oi']} · "
                 f"{row['oi_dn_dist']:+g}{m}")
    L.append(f"تدفّق: فوق {row['vol_above']} · تحت {row['vol_below']} "
             f"· بوت/كول {row['pc_ratio']}")
    if row.get("atm_strike"):
        w = " (ضعيف)" if row.get("atm_cp_weak") else ""
        L.append(f"ATM {row['atm_strike']} · كول/بوت {row['atm_cp_ratio']}{w}")
    L.append(f"🕐 {row['ts_ny']} NY")
    return "\n".join(L)


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
            "vix": _vix(), "vix1d": _vix1d(),
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
            "vix": _vix(), "vix1d": _vix1d(),
            "vix_symbol": VIX_SYMBOL, "vix1d_symbol": VIX1D_SYMBOL,
            "cp_min_side": CP_MIN_SIDE,
            "ny_now": datetime.now(NY).strftime("%Y-%m-%d %H:%M"),
            "spy_exp": pick_expiration("SPY"), "spx_exp": pick_expiration("SPX"),
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.get("/json")
def as_json(u: str = "SPY", n: int = 0, exp: str = ""):
    return JSONResponse(fetch(u, expiration=exp or None, n=n or None, force=True))


@app.get("/debug")
def dbg(u: str = "SPY"):
    return JSONResponse(debug(u))


@app.get("/snap")
def snap(u: str = "SPX", n: int = 30, key: str = "", tag: str = "",
         fmt: str = "json"):
    """لقطة سيولة واحدة — نقطة الاتصال الوحيدة مع البوت.

       اتجاه واحد: البوت يستدعي ويقرأ. اللوحة لا تعرف بوجود البوت.
       /snap?u=SPX                          → JSON
       /snap?u=SPX&fmt=txt                  → نص عربي جاهز للنسخ
       /snap?u=SPX&key=2026-08-31_10:05_PUT_771&tag=executed
    """
    row = snapshot_row(u, tag=tag, sig_key=key, n=max(5, min(n, 40)))
    if fmt == "txt":
        return HTMLResponse("<pre style='font:14px/1.7 monospace;direction:rtl'>"
                            + snap_text(row) + "</pre>")
    return JSONResponse(row)


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
    if p.endswith("/snap"):
        return JSONResponse(snapshot_row(u if u != "SPY" else "SPX"))
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
.px .vix{display:block;font-size:10px;color:var(--dim);margin-top:2px;
 white-space:nowrap;line-height:1.3}
.px .conc{display:block;font-size:11px;font-weight:700;margin-top:3px;white-space:nowrap}
.px .conc s{text-decoration:none;font-weight:600;color:var(--dim);font-size:10px}

/* شريط نطاق اليوم — أدنى · السعر · أعلى */
.rng{margin:0 0 9px;padding:6px 10px 8px;background:var(--c1);
 border:1px solid var(--ln);border-radius:11px}
.rng .lbl{display:flex;justify-content:space-between;font-size:9px;
 color:var(--dim);margin-bottom:5px}
.rng .track{position:relative;height:5px;border-radius:3px;
 background:linear-gradient(90deg,rgba(255,92,114,.35),rgba(255,255,255,.12),
 rgba(45,212,160,.35))}
.rng .dot{position:absolute;top:-3px;width:11px;height:11px;border-radius:50%;
 background:var(--tx);border:2px solid var(--bg);transform:translateX(-50%);
 transition:inset-inline-start .5s}
.rng .op{position:absolute;top:-1px;width:2px;height:7px;background:var(--wr);
 opacity:.8;transform:translateX(-50%)}

/* القائمة المدمجة لأكبر التجمّعات */
.cl{background:var(--c1);border:1px solid var(--ln);border-radius:13px;overflow:hidden}
.clr{display:grid;grid-template-columns:12px 40px 1fr 34px 40px 38px;gap:5px;
 align-items:center;padding:6px 9px;border-bottom:1px solid rgba(33,43,60,.5)}
.clr:last-child{border-bottom:none}
.clr .dotc{width:8px;height:8px;border-radius:50%}
.clr .s{font-weight:700;font-size:12.5px}
.clr .bar{position:relative;height:13px;background:rgba(255,255,255,.03);
 border-radius:4px;overflow:hidden}
.clr .bar i{position:absolute;inset-inline-start:0;top:0;height:100%;
 border-radius:4px;transition:width .45s}
.clr .bar b{position:absolute;inset-inline-start:6px;top:0;line-height:13px;
 font-size:9.5px;font-weight:700}
.clr .d{text-align:center;font-size:10px;font-weight:600;color:var(--dim)}
.clr .d.hit{color:var(--dn);font-weight:700}
.clr .g{text-align:center;font-size:9.5px;color:var(--dim)}
.clr .g.hot{color:var(--up);font-weight:700;
 text-shadow:0 0 8px rgba(45,212,160,.55)}
/* OI = رسوخ التجمّع · العالي أقوى — عكس ما كان في v1.3.1 */
.clr .v{text-align:center;font-size:9.5px;font-weight:700;color:var(--dim)}
.clr .v.solid{color:var(--tx);text-shadow:0 0 9px rgba(233,238,246,.35)}
.clr .v.thin{opacity:.35}
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

/* ── [v1.4] لوحة تدفّق آخر 15 دقيقة ── */
.flow{background:var(--c1);border:1px solid var(--ln);border-radius:13px;
 padding:8px 9px 6px;margin-bottom:9px}
.fhd{display:flex;justify-content:space-between;align-items:center;gap:6px;
 font-size:10px;color:var(--dim);margin-bottom:7px}
.fhd s{text-decoration:none;font-size:9px}
.ftot{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:7px}
.ft1{background:rgba(255,255,255,.03);border-radius:9px;padding:6px 3px;text-align:center}
.ft1 u{display:block;font-size:9px;color:var(--dim);text-decoration:none;margin-bottom:2px}
.ft1 b{font-size:14px;font-weight:700}
.fr{display:grid;grid-template-columns:40px 1fr 1fr;gap:4px;align-items:center;
 margin-bottom:2px}
.fs{font-size:10.5px;font-weight:700;text-align:center}
.fb{position:relative;height:11px;background:rgba(255,255,255,.03);
 border-radius:3px;overflow:hidden}
.fb i{position:absolute;inset-inline-start:0;top:0;height:100%;border-radius:3px;
 transition:width .4s}
.fb b{position:absolute;inset-inline-start:5px;top:0;line-height:11px;
 font-size:8.5px;font-weight:700}
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
  <div class="sub"><span id="ses" class="bdg">…</span> <span id="ts">…</span></div>
  <span class="vix" id="vix"></span>
  <span class="conc" id="conc"></span></div>
</div>

<div class="rng" id="rng" style="display:none">
 <div class="lbl"><span id="rlo">—</span><span id="rmid">نطاق اليوم</span>
  <span id="rhi">—</span></div>
 <div class="track"><span class="op" id="rop" style="display:none"></span>
  <span class="dot" id="rdot"></span></div>
</div>

<div class="exp"><span>سلسلة العقود</span><b id="exp">…</b></div>
<div class="picks"><span>سترايكات</span>__PICKS__</div>

<div class="stats">
 <div class="st"><u>كول</u><b id="cv" style="color:var(--up)">—</b></div>
 <div class="st"><u>بوت / كول</u><b id="pc">—</b></div>
 <div class="st"><u>بوت</u><b id="pv" style="color:var(--dn)">—</b></div>
</div>

<div class="flow" id="flow">
 <div class="fhd"><span>تدفّق آخر 15 دقيقة · 8 سترايك فوق و8 تحت</span>
  <span id="fnote"><s style="color:var(--dim)">جارٍ بناء النافذة…</s></span></div>
 <div class="ftot">
  <div class="ft1"><u>كول</u><b id="fcall" style="color:var(--up)">—</b></div>
  <div class="ft1"><u>تسارع</u><b id="faccel">—</b></div>
  <div class="ft1"><u>بوت</u><b id="fput" style="color:var(--dn)">—</b></div>
 </div>
 <div id="fbars"></div>
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

<div class="ctitle">أكبر ثمانية تجمّعات — الشريط = الحصة · OI = الرسوخ</div>
<div class="cl" id="chips"></div>

<script>
const U="__U__",N=__N__,R=__R__;
// ⚠ المفتاح يحمل اسم الأداة ⇒ تاريخ SPX منفصل تماماً عن SPY.
//   عند التبديل يبدأ تاريخ الأداة الجديدة من الصفر — لهذا يوجد مؤشر جاهزية.
const HK="liq_hist_"+U;
const WIN=300000;        // نافذة 5 دقائق — بالطابع الزمني لا بعدّ اللقطات
const KEEP=7200000;      // ساعتان: يكفيان لوسيط متدحرج ذي معنى
const STEP=30000;        // لقطة محفوظة كل 30 ثانية (الدورة تبقى 5 ثوانٍ)
const MIN_BASE=6;        // أقل عدد نوافذ قبل عرض المضاعف
/* ═══ [v1.4] تدفّق آخر 15 دقيقة ═══
   المبدأ: حجم الخيارات تراكمي منذ ما قبل الافتتاح ولا ينخفض أبداً.
   ⇒ الفرق بين لقطتين = ما تُدووِل في تلك الفترة بالضبط.
   ⚠ الطرح يتم **لكل سترايك على حدة** لا على المجموع: السعر يتحرك
     فيدخل السترايك النافذة أو يخرج منها، والطرح على المجموع يقيس
     حركة السعر لا التدفّق. (خطأ وقعنا فيه وصحّحناه — 4 سبتمبر)
   ⚠ رصيد ما قبل الافتتاح يسقط تلقائياً في الفرح لأنه في اللقطتين معاً. */
const FK="liq_flow_"+U;
const FWIN=900000;       // نافذة 15 دقيقة
const FSTEP=60000;       // لقطة تدفّق كل دقيقة
const FKEEP=5400000;     // ساعة ونصف
const FSTRIKES=8;        // 8 سترايكات فوق السعر و8 تحته
/* عتبات مؤقتة — تُستبدل بمئينات حقيقية بعد أسبوعين من البيانات */
const F_STRONG=60, F_WEAK=55;
const K=v=>v==null?"—":(v>=1000?(v/1000).toFixed(v>=10000?0:1)+"k":String(v));
const P=v=>v==null?"—":Number(v).toFixed(2);
function hist(){try{return JSON.parse(localStorage.getItem(HK))||[]}catch(e){return[]}}
function median(a){if(!a.length)return null;const b=[...a].sort((x,y)=>x-y);
 const m=b.length>>1;return b.length%2?b[m]:(b[m-1]+b[m])/2;}
/* يحفظ اللقطة ويرجع {ref, mult, ready}
   ref  = خريطة الأحجام قبل 5 دقائق (لعمود النمو لكل سترايك)
   mult = نمو آخر 5 دقائق ÷ وسيط النوافذ السابقة داخل الجلسة
   ⚠ الوسيط المتدحرج بدل عتبة ثابتة: 30k صباحاً ليست 30k عصراً. */
function push(snap,tot){
 let h=hist(),now=Date.now();
 if(!h.length||now-h[h.length-1].t>STEP)h.push({t:now,s:snap,v:tot});
 h=h.filter(x=>now-x.t<KEEP);
 try{localStorage.setItem(HK,JSON.stringify(h))}catch(e){
   try{localStorage.setItem(HK,JSON.stringify(h.slice(-120)))}catch(e2){}}
 let ref=null;
 for(const x of h){if(now-x.t>=WIN)ref=x.s;else break;}
 // ── سلسلة نمو النوافذ: لكل لقطة، الفرق عن لقطة أقدم بـ5 دقائق ──
 const deltas=[];
 for(let i=0;i<h.length;i++){
  let j=-1;
  for(let k=i-1;k>=0;k--){if(h[i].t-h[k].t>=WIN){j=k;break;}}
  if(j>=0&&h[j].v!=null&&h[i].v!=null){
   const dv=h[i].v-h[j].v; if(dv>0)deltas.push(dv);
  }
 }
 let mult=null,ready=deltas.length>=MIN_BASE;
 if(ready){
  const cur=deltas[deltas.length-1];
  const base=median(deltas.slice(0,-1));
  if(base&&base>0)mult=Math.round(cur/base*10)/10;
 }
 return {ref:ref,mult:mult,ready:ready,n:deltas.length};
}
/* يحفظ لقطة تدفّق ويرجع مرجعين: قبل 15د وقبل 30د.
   الثاني يخدم التسارع: تدفّق آخر 15د ÷ تدفّق الـ15د التي تسبقها.
   ⚠ لا يقارن بمتوسط اليوم: في أول ساعة يكون المتوسط محسوباً على
     دقائق قليلة والافتتاح أنشط ما في اليوم ⇒ مقام مضخّم ونسبة كاذبة.
     المقارنة بالنافذة السابقة تعمل من أول ثلاث لقطات وأصدق مفهومياً. */
function pushFlow(cm,pm){
 let h; try{h=JSON.parse(localStorage.getItem(FK))||[]}catch(e){h=[]}
 const now=Date.now();
 if(!h.length||now-h[h.length-1].t>FSTEP)h.push({t:now,c:cm,p:pm});
 h=h.filter(x=>now-x.t<FKEEP);
 try{localStorage.setItem(FK,JSON.stringify(h))}catch(e){
   try{localStorage.setItem(FK,JSON.stringify(h.slice(-60)))}catch(e2){}}
 let r1=null,r2=null;
 for(const x of h){
  if(now-x.t>=FWIN)r1=x;
  if(now-x.t>=FWIN*2)r2=x;
  else if(now-x.t<FWIN)break;
 }
 return {cur:{t:now,c:cm,p:pm},r1:r1,r2:r2,n:h.length};
}
/* فرق الأحجام بين لقطتين لكل سترايك داخل نافذة FSTRIKES حول السعر.
   يرجع {call, put, per} — per = تدفّق كل سترايك للعرض البصري. */
function flowDiff(a,b,strikes){
 if(!a||!b)return null;
 let C=0,P2=0; const per=[];
 for(const k of strikes){
  const dc=Math.max(0,(a.c[k]||0)-(b.c[k]||0));
  const dp=Math.max(0,(a.p[k]||0)-(b.p[k]||0));
  C+=dc; P2+=dp; per.push({strike:+k,call:dc,put:dp});
 }
 return {call:C,put:P2,total:C+P2,per:per};
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
/* ══ [v1.4] لوحة تدفّق آخر 15 دقيقة ══
   ما تقوله: أين تُتداول العقود **الآن** — لا منذ الافتتاح.
   ⚠ لا تقول من المشتري ومن البائع (كل صفقة لها طرفان)، بل أين
     تتركّز الحرارة. ⚠ عتبات النص مؤقتة حتى تتوفر مئينات حقيقية. */
function renderFlow(d){
 const el=document.getElementById("flow"); if(!el)return;
 // النافذة: أقرب FSTRIKES فوق السعر وFSTRIKES تحته
 const ab=d.table.filter(t=>t.side==="above").sort((a,b)=>a.dist-b.dist).slice(0,FSTRIKES);
 const be=d.table.filter(t=>t.side==="below").sort((a,b)=>b.dist-a.dist).slice(0,FSTRIKES);
 const win=[...be,...ab];
 const cm={},pm={};
 for(const t of d.table){cm[t.strike]=t.call_vol;pm[t.strike]=t.put_vol;}
 const F=pushFlow(cm,pm);
 const strikes=win.map(t=>String(t.strike));
 const now=flowDiff(F.cur,F.r1,strikes);
 const prev=F.r2?flowDiff(F.r1,F.r2,strikes):null;
 const setTxt=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
 if(!now||now.total<=0){
  document.getElementById("fnote").innerHTML=
   F.r1?'<s style="color:var(--dim)">لا نشاط يُذكر في آخر 15 دقيقة</s>'
       :'<s style="color:var(--dim)">جارٍ بناء النافذة — '
        +Math.max(0,15-Math.round((F.n*FSTEP)/60000))+' دقيقة متبقية</s>';
  document.getElementById("fbars").innerHTML="";
  setTxt("fcall","—"); setTxt("fput","—"); setTxt("faccel","—");
  return;
 }
 const cp=now.call/now.total*100;
 setTxt("fcall",K(now.call)); setTxt("fput",K(now.put));
 // التسارع: نافذة الآن ÷ النافذة السابقة لها مباشرة
 let acc=null;
 if(prev&&prev.total>0)acc=Math.round(now.total/prev.total*10)/10;
 setTxt("faccel",acc==null?"—":acc+"×");
 const ae=document.getElementById("faccel");
 if(ae)ae.style.color=acc==null?"var(--dim)":(acc>=2?"var(--wr)":(acc>=1.3?"var(--tx)":"var(--dim)"));
 // الملاحظة النصية — الاتجاه بصرياً قبل قراءة الأرقام
 let note,col;
 if(cp>=F_STRONG){note="نشاط CALL";col="var(--up)";}
 else if(100-cp>=F_STRONG){note="نشاط PUT";col="var(--dn)";}
 else if(Math.max(cp,100-cp)>=F_WEAK){
  note=(cp>50?"ميل CALL":"ميل PUT")+" · تركيز منخفض";
  col=cp>50?"rgba(45,212,160,.65)":"rgba(255,92,114,.65)";
 }else{note="نشاط متوازن";col="var(--dim)";}
 const dom=Math.max(cp,100-cp).toFixed(0);
 const burst=(acc!=null&&acc>=2&&cp>=F_STRONG)||(acc!=null&&acc>=2&&(100-cp)>=F_STRONG);
 document.getElementById("fnote").innerHTML=
  `<span style="color:${col};font-weight:700">${burst?"⚡ ":""}${note} ${dom}%</span>`
  +`<s style="color:var(--ft);font-weight:600"> · مؤقتة</s>`;
 // الأشرطة لكل سترايك
 const mx=Math.max(...now.per.map(x=>Math.max(x.call,x.put)),1);
 document.getElementById("fbars").innerHTML=now.per
  .slice().sort((a,b)=>b.strike-a.strike).map(x=>{
   const above=x.strike>d.spot;
   const wc=Math.round(100*x.call/mx),wp=Math.round(100*x.put/mx);
   return `<div class="fr">
    <span class="fs" style="color:${above?"#2dd4a0":"#ff5c72"}">${x.strike}</span>
    <span class="fb"><i style="width:${wc}%;background:#2dd4a055"></i>
     <b style="color:#2dd4a0">${x.call?K(x.call):""}</b></span>
    <span class="fb"><i style="width:${wp}%;background:#ff5c7255"></i>
     <b style="color:#ff5c72">${x.put?K(x.put):""}</b></span></div>`;
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
  // [v1.3] التغيّر من إغلاق الأمس ⇒ الفجوة محتسبة. وبجانبه تغيّر الافتتاح.
  const ch=d.chg_pct;
  if(ch!=null){
   const upx=ch>=0;
   sp.style.color=live?(upx?"var(--up)":"var(--dn)"):"var(--tx)";
   cg.style.color=upx?"var(--up)":"var(--dn)";
   let t=(upx?"▲ +":"▼ ")+ch+"%";
   if(d.chg_open_pct!=null)
    t+=`<s style="color:var(--dim);font-weight:600;font-size:10px;
        text-decoration:none"> · من الفتح ${d.chg_open_pct>0?"+":""}${d.chg_open_pct}%</s>`;
   cg.innerHTML=t;
  }else{sp.style.color="var(--tx)";cg.textContent="";}
  // ── شريط نطاق اليوم ──
  const rg=document.getElementById("rng");
  if(d.day_high&&d.day_low&&d.day_high>d.day_low){
   rg.style.display="";
   document.getElementById("rlo").textContent=d.day_low.toFixed(2);
   document.getElementById("rhi").textContent=d.day_high.toFixed(2);
   const pos=Math.max(0,Math.min(100,
     (d.spot-d.day_low)/(d.day_high-d.day_low)*100));
   document.getElementById("rdot").style.insetInlineStart=pos+"%";
   document.getElementById("rmid").textContent=
     "نطاق اليوم "+(d.day_high-d.day_low).toFixed(2)+" · موقع "+pos.toFixed(0)+"%";
   const op=document.getElementById("rop");
   if(d.day_open&&d.day_open>=d.day_low&&d.day_open<=d.day_high){
    op.style.display="";
    op.style.insetInlineStart=
      ((d.day_open-d.day_low)/(d.day_high-d.day_low)*100)+"%";
   }else op.style.display="none";
  }else rg.style.display="none";
  let vtx=d.vix?("VIX "+d.vix):"";
  if(d.vix1d)vtx+=(vtx?" · ":"")+"0D "+d.vix1d;
  document.getElementById("vix").textContent=vtx;
  document.getElementById("ts").textContent=d.ny_time+" نيويورك";
  const sb=document.getElementById("ses"),sc=SES[d.session]||SES.closed;
  sb.textContent=d.session_txt;sb.style.color=sc[0];sb.style.background=sc[1];
  pace(d.session);
  document.getElementById("exp").textContent=`ينتهي ${d.exp_disp} · ${d.exp_tag}`;
  document.getElementById("cv").textContent=K(d.call_vol_total);
  document.getElementById("pv").textContent=K(d.put_vol_total);
  const pc=document.getElementById("pc");
  pc.textContent=d.pc_ratio??"—";
  pc.style.color=d.pc_ratio==null?"var(--tx)":(d.pc_ratio>1.15?"var(--dn)":(d.pc_ratio<.85?"var(--up)":"var(--tx)"));
  // ── شريط الجدران ──
  walls(document.getElementById("wup"),d.oi_up,"#2dd4a0","▲ OI");
  walls(document.getElementById("wdn"),d.oi_dn,"#ff5c72","▼ OI");
  // ── نمو 5د + المضاعف المتدحرج ──
  const H=push(Object.fromEntries(d.table.map(t=>[t.side+t.strike,t.main_vol])),
               d.total_vol);
  const rf=H.ref;
  for(const t of d.table){const pv=rf?rf[t.side+t.strike]:null;
   t.dp=(pv&&pv>0)?Math.round((t.main_vol-pv)/pv*1000)/10:null;}
  // ══════ [v1.4] تدفّق آخر 15 دقيقة — 8 سترايكات فوق و8 تحت ══════
  renderFlow(d);
  // ── تركّز النشاط: نسبة حجم أكبر خمسة تجمّعات فوق السعر إلى مجموعها ──
  // ⚠ «فوق/تحت» لا «كول/بوت»: التجمّع فوق السعر يُحسب كولاً بحكم التعريف
  //   لا باختيار السوق ⇒ هذا وصف تركّز نشاط، لا رأي اتجاهي.
  const top5=(d.clusters||[]).slice(0,5);
  const vu=top5.filter(c=>c.side==="above").reduce((a,c)=>a+c.vol,0);
  const vd=top5.filter(c=>c.side==="below").reduce((a,c)=>a+c.vol,0);
  const cel=document.getElementById("conc");
  const totTop=vu+vd;
  if(totTop>=50000){
   const pu=vu/totTop*100;
   // حدود مؤقتة معايرة على أول 25 لقطة (وسيط ~62%) — تُعاد المعايرة عند 50
   const strong=pu>=75||pu<=38;
   const arrow=pu>=50?"▲":"▼", shown=pu>=50?pu:100-pu;
   const col=pu>=62?"var(--up)":(pu<=50?"var(--dn)":"var(--dim)");
   let txt=`<span style="color:${col}">${arrow} ${shown.toFixed(0)}%`
          +(strong?" ⬤":"")+`</span>`;
   // ⚠ المضاعف يُخفى قبل 10:00 NY: الأساس شبه صفر فيعطي أرقاماً بلا معنى
   const hh=parseInt((d.ny_time||"00:00").split(":")[0],10);
   const mm=parseInt((d.ny_time||"00:00").split(":")[1],10);
   const after10=(hh>10)||(hh===10&&mm>=0);
   if(H.mult!=null&&after10&&live)
    txt+=`<s> · ${H.mult}×</s>`;
   else if(live)
    txt+=`<s> · —</s>`;
   cel.innerHTML=txt;
  }else cel.innerHTML=`<s>تركّز — نشاط منخفض</s>`;
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
   // جانب ضعيف ⇒ النسبة بلا مضمون ⇒ رمادي باهت مهما بلغت قيمتها
   const crc=(cr==null)?"var(--dim)":(t.cp_weak?"#4e5c74":
    (cr>=1.6?"#2dd4a0":(cr<=0.62?"#ff5c72":"var(--dim)")));
   const cro=t.cp_weak?";opacity:.45":"";
   h+=`<div class="rw${t.strike===pk?" pin":""}">
    <span class="sk" style="color:${c}">${t.strike}</span>
    <span class="bw2">
     <span class="bw"><span class="bf" style="width:${wc}%;background:#2dd4a02e"></span>
      <span class="bv" style="color:#2dd4a0">${K(t.call_vol)}</span></span>
     <span class="bw"><span class="bf" style="width:${wp}%;background:#ff5c722e"></span>
      <span class="bv" style="color:#ff5c72">${K(t.put_vol)}</span></span>
    </span>
    <span class="cp" style="color:${crc}${cro}">${cr==null?"—":cr}</span>
    <span class="pp"><i style="color:#2dd4a0">${P(t.call_mid)}</i>
     <i style="color:#ff5c72">${P(t.put_mid)}</i></span>
    <span class="rt"><i class="${t.strike===pk?"big":""}">${K(t.main_oi)}</i>
     <i class="${hot?"hot":""}">${dt}</i></span></div>`;
  }
  if(!placed)h+=`<div class="spot dim">${U} ${Number(d.spot).toFixed(2)}</div>`;
  B.innerHTML=h;
  // ── القائمة المدمجة: كول وبوت معاً مرتّبين بالحجم ──
  const cmx=Math.max(...(d.clusters||[]).map(c=>c.vol),1);
  const band=[d.target_lo_pct,d.target_hi_pct];
  const gmap={}; for(const t of d.table) gmap[t.side+t.strike]=t.dp;
  document.getElementById("chips").innerHTML=(d.clusters||[]).map(c=>{
   const up=c.side==="above",col=up?"#2dd4a0":"#ff5c72";
   const w=Math.max(8,Math.round(100*c.vol/cmx));
   const dp=Math.abs(c.dist)/d.spot*100;
   const hit=dp>=band[0]&&dp<=band[1];   // داخل شريحة الهدف
   const g=gmap[c.side+c.strike];
   const gt=(g==null)?"—":((g>0?"+":"")+g+"%");
   const hot=g!=null&&g>=8;
   return `<div class="clr">
    <span class="dotc" style="background:${col}"></span>
    <span class="s" style="color:${col}">${c.strike}</span>
    <span class="bar"><i style="width:${w}%;background:${col}33"></i>
     <b style="color:${col}">${K(c.vol)}</b></span>
    <span class="d ${hit?"hit":""}">${c.dist>0?"+":""}${c.dist.toFixed(1)}</span>
    <span class="v ${c.oi>=2000?"solid":(c.oi<500?"thin":"")}">${K(c.oi)}</span>
    <span class="g ${hot?"hot":""}">${gt}</span></div>`;
  }).join("");
 }catch(e){B.innerHTML=`<div class="err">⚠ ${e}</div>`;}
}
// ── دورة التحديث: تتوقف عند إخفاء الصفحة (توفير بطارية) ──
let TIMER=null,CUR=null;
// [v1.3] خارج الجلسة لا شيء يتحرك ⇒ دورة بطيئة (60 ثانية) بدل 5 ثوانٍ.
//        يوفّر بطارية واستدعاءات بلا أي فقد في المعلومة.
function arm(sec){
 if(TIMER&&CUR===sec)return;
 if(TIMER)clearInterval(TIMER);
 CUR=sec; TIMER=setInterval(load,sec*1000);
}
function stop(){if(TIMER){clearInterval(TIMER);TIMER=null;CUR=null;}}
function start(){load();arm(R);}
function pace(session){arm(session==="open"?R:60);}
document.addEventListener("visibilitychange",()=>{document.hidden?stop():start();});
start();
</script></body></html>"""
