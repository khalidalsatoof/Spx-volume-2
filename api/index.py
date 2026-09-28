# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  liq.py — التقاط السيولة وقياس التدفّق  (v3.0.1)
═══════════════════════════════════════════════════════════════════════════════
  ⚠ v3.0.1 (28 سبتمبر) — إصلاح عاجل: v3.0 أضافت أعمدة lb_* إلى LIQ_COLS ولم
    تُضِف لها قيماً فارغة في حفظ اللقطات ⇒ فشل كل INSERT للّقطات (cron ·
    executed · rejected) منذ النشر ⇒ لوحة التدفّق عالقة على لقطة الجمعة.
    الإصلاح: قيم فارغة لأعمدة القرار والبوت معاً. بوت السيولة نفسه لم يتأثر
    (تدفّقه من سلسلة الجامع لا من اللقطات).
  ★★ الجديد في v3.0 — «بوت السيولة»: مشروع مستقل عن إشارة TradingView ★★
  (طلب خالد 27 سبتمبر: قرار منفصل تماماً، آلي بلا تدخّل، قياس لا تنفيذ)

  ① الإشارة — الثلاثة معاً:
       المسيطرون ≥55% صعودي (CALL) أو ≤45% (PUT) ثابتاً 60 ثانية
     + التدفّق مشبع عكسها: ميل النطاق النشط ≤−0.20 للـCALL · ≥+0.20 للـPUT
     + مساحة ≥10 نقاط حتى أقرب منطقة عرض/طلب صالحة أو حدّ VIX1D
     النافذة 09:45–15:00 · 15 د بين إشارتين في نفس الاتجاه · الصفقات تتداخل.
  ② مناطق العرض والطلب: شموع SPX بفاصل 5 د (نداء واحد كل 5 دقائق) — مساعدة
     لا أساسية: تحدد المساحة، وتصنيف A إن انطلقت الإشارة من داخل منطقة.
  ③ العقد: أول سترايك في الاتجاه منتصفه $3.90–$4.50 · وقف −40% · متحرك
     يُسلَّح عند +30% ويخرج عند −25% من الذروة · إغلاق إجباري 15:45.
  ④ يُقاس: أول بلوغ 10/15/20 نقطة SPX وأسوأ نزول قبل كلٍّ منها (60 د) ·
     المسار كل 30 ث · كل الصفوف tag = liq_bot (أعمدة lb_*) في /liq.csv.
  ⑤ قرار v2.9 القديم (الانقلاب والجدران) موقوف: DEC_LEGACY=1 يعيده.
     مدخلات /json (VIX1D · VWAP · الغاما) باقية — يحتاجها البوت.
  ⑥ عدّاد نداءات Tradier لهذه الوحدة (آخر 60 ث) في /liq_agg و/health.
  ⚠ LB_ENABLED=0 يوقف البوت كاملاً بلا تعديل كود. صفر أوامر.

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.9 — قرار اللوحة يُحسب ويُحفظ في الخادم ★★
  (طلب خالد 23 سبتمبر: البيانات تبقى حتى لو أُغلق المتصفح أو حُدّثت الصفحة)

  ① منطق القرار في index v2.3.1 منقول حرفياً إلى هنا: decide + تخلّف الضغط +
     تأكيد 60 ثانية للدخول و20 للتراجع. يعمل في خيط الجامع كل 5 ثوانٍ طوال
     الجلسة بلا أي متصفح. التطابق مُثبت: 20,000 مدخل عشوائي (1,176 قرار
     دخول) و30,000 خطوة تخلّف/تأكيد ⇒ صفر اختلاف مع نسخة المتصفح.
  ② كل قرار مؤكَّد يُرقَّم يومياً (#1، #2…) ويُحفظ صفاً في liq_snaps
     (tag = dash_dec · أعمدة dec_*) لحظة ولادته، ويُحدَّث كل دقيقة وعند
     نهاية ساعته. العقد المرشّح = الأعلى تداولاً في الاتجاه وسعره ≤ $4.50.
     يُتتبَّع: سعر العقد الآن/الأعلى/الأدنى ووقتها · لمس الهدف والإبطال.
  ③ إعادة تشغيل Render: قرارات اليوم تُستعاد من القاعدة، والفجوة تُسدّ
     بشموع الدقيقة من Tradier (timesales) للعقد وللأداة. وعند نهاية كل
     قرار تُجلب الشموع مرة أخيرة ⇒ الأعلى والأدنى مكتملان.
  ④ تصل اللوحة عبر /liq_agg (حقل dec) بلا تعديل في server.py.
  ⑤ المدخلات: السعر كل 10 ثوانٍ (بدل 30) + /json من اللوحة كل 20 ثانية
     في خيط مستقل (VWAP والانقلاب والجداران وحدّا اليوم).
     ⚠ النداءات: +3/د لـTradier (السعر) و+3/د لـVercel. المجموع بلوحة
       مفتوحة ~70/د والحدّ 120. DEC_ENABLED=0 يوقفه كاملاً.
  ⚠⚠ صفر قرارات على البوت. تسجيل وعرض فقط.

  ─────────────────────────────────────────────────────────────────────────
  وحدة مستقلة تماماً. تُستدعى من server.py عند وصول أي إشارة — منفَّذة كانت
  أم مرفوضة — ومن /liq_cron كل ثلاث دقائق لبناء سلسلة متصلة.

  ★★ الجديد في v2.8 — سلسلة المسيطر + حفظ القرار + نطاق اليوم ★★

  ① سلسلة المسيطر دقيقة بدقيقة (AGG_SERIES_MAX=420 نقطة = جلسة كاملة)
     تُبنى في الجامع نفسه بلا نداء إضافي، وتخرج ضمن agg_window() ⇒ تصل
     اللوحة عبر /liq_agg بلا تعديل في server. هكذا يظهر خط اليوم كاملاً
     حتى لو لم تُفتح الصفحة إطلاقاً.
     ⚠ إعادة تشغيل Render تمسح الذاكرة، فتُعاد السلسلة من liq_snaps
       (عمود agg_bull_pct · دقّة 3 دقائق) مرة واحدة لكل يوم.
     ⚠ الذاكرة: 420 زوجاً من الأرقام (~20KB أقصى حد) — سقف ثابت لا يكبر.

  ② حفظ قرار اللوحة في كل لقطة (نقل حرفي لمنطق index v2.1.x):
       verdict · verdict_regime · verdict_tgt · verdict_inv · verdict_rr
     ⇒ بعد أسابيع نقيس: بعد كل STRONG CALL كم تحرّك SPX وخلال كم دقيقة،
       وكم مرة بلغ الهدف قبل الإبطال.
     ⚠ بلا تخلّف ولا تأكيد 60 ثانية — القرار المحفوظ هو الخام لحظة اللقطة.

  ③ نطاق اليوم حتى لحظة الإشارة: day_high · day_low · day_range
     لاختبار فرضية 22 سبتمبر: هل تخسر الإشارات المولودة داخل نطاق ميت؟
     ⚠ يتطلب index v2.2 (يُخرجها في /snap). مع index أقدم تبقى فارغة.

  ⚠⚠ صفر قرارات على البوت. تسجيل وعرض فقط.

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.7 — المسيطر من الخادم + حفظ «قراءة اللحظة» ★★

  ① جامع خلفي كل AGG_SEC (5) ثوانٍ طوال الجلسة (09:30–16:00 NY)
     يجلب سلسلة SPX 0DTE مباشرة من Tradier (عميل server المشترك — لا عميل
     جديد) ويصنّف الحجم الجديد بين كل لقطتين بقاعدة لي-ريدي، بنفس منطق
     اللوحة حرفياً: آخر صفقة ≥60% من الفارق نحو الطلب = مشترٍ · ≤40% =
     بائع · بينهما لا يُصنَّف. فجوة >30 ثانية ⇒ لا نسب.
     السبب: الحساب في المتصفح يحتاج صفحة مفتوحة، والجوال يُقفل.
     ⚠ الذاكرة: آخر لقطة (~60 عقداً) + 200 حدث صغير كحدّ أقصى. لا تراكم.
     ⚠ النداءات: 12/د للسلسلة + 2/د للسعر. الحدّ 120/د.
  ② /liq_agg (في server) يعيد نافذة آخر 5 دقائق للوحة.
  ③ أعمدة جديدة في liq_snaps (تسجيل فقط):
       agg_cb · agg_cs · agg_pb · agg_ps · agg_unc · agg_cov_sec ·
       agg_buy_pct · agg_bull_pct       ← المسيطر لحظة اللقطة
       vwap_spy · vwap_dist_spy · vwap_dist_und · vwap_call_ok ·
       vwap_put_ok · em_pts · em_hi · em_lo · em_src  ← من /snap (index v1.9.3)
  ⚠⚠ صفر قرارات. لا بوابة ولا فلتر. سطر وصفي في تيليجرام عند الإشارة فقط.

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.6 — كشف انطلاق التدفّق ★★

  ── لماذا ──
  محاكاة 18 سبتمبر على 1,364 لقطة (31 أغسطس–17 سبتمبر) أعطت:
    • الميل وحده لا يتنبّأ بحركة 15/30/60 دقيقة — 47–50% اتجاه صحيح
      مقابل خط أساس 48–49%. صفر حافة.
    • «انطلاق» الميل وحده (حياد ⇒ ≥0.15) كذلك: 47–50%. صفر حافة.
    • لكن **الانطلاق مع تسارع ≥2.0** أعطى 69.2% اتجاه صحيح عند +15د
      و+60د، بمتوسط +2.71 و+4.22 نقطة SPX. وعند تسارع ≥1.5: 64.0%.
      الأثر يشتدّ مع العتبة ويثبت عبر الآفاق الثلاثة.
    ⚠ على 13 حدثاً فقط عند العتبة 2.0. مرشّح لا نتيجة.

  ── اكتشاف جانبي يقلب ما كنا نفترضه ──
  الحركة السابقة للانطلاق في اتجاه الميل: 25% عند −5د و31% عند −15د.
  أي أن السعر يتحرك **عكس** الميل قبل ظهوره في ~70–75% من الحالات.
  التدفّق لا يتأخّر عن الحركة — يظهر بعد حركة معاكسة. سلوك ارتدادي.
  ⇒ يفسّر لماذا AGREE ضعيف: الإشارة توافق تدفّقاً وُلد من ارتداد.

  ── ما أُضيف (خمسة أعمدة) ──
    flow_prev_bias    ميل اللقطة السابقة — أساس الكشف
    flow_prev_age     عمرها بالدقائق (تُرفض إن تجاوزت FLOW_PREV_MAX)
    flow_onset        1 عند الانتقال من حياد إلى ميل واضح
    flow_onset_dir    CALL أو PUT — جهة الميل الجديد
    flow_onset_hot    1 إن رافق الانطلاق تسارع ≥ FLOW_ONSET_ACCEL

  ⚠⚠ صفر قرارات. تسجيل فقط. لا بوابة ولا فلتر ولا أثر على دخول أو
     خروج. الغرض: بناء عدّاد يحسم السؤال بعد 3–4 أسابيع بدل الحدس.
  ⚠ استعلام واحد إضافي خفيف لكل لقطة (صف واحد بـLIMIT 1).

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.5 — عميل HTTP مشترك ★★
  إصلاح تسرّب ذاكرة Render. التفاصيل في كتلة العميل أدناه.
  ⚠ صفر تغيير في أي منطق — نفس النداء بنفس المهلة ونفس المعالجة.

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.4 — حفظ أرقام التموضع ★★

  ── المشكلة ──
  اللوحة تحسب GEX والفانّا والتشارم ومستوى الانقلاب كل خمس ثوانٍ منذ
  index v1.8، وتعرضها، ثم تُرمى. لا يصل منها رقم واحد إلى liq_snaps.
  ⇒ سؤال «هل بُعد السعر عن الانقلاب يفصل الرابح من الخاسر؟» بلا بيانات،
    وسؤال «هل تغيّر vex يسبق حركة SPY أم يتبعها؟» يحتاج سلسلة زمنية
    ثم ارتباطاً متقاطعاً بإزاحة — ولا سلسلة بلا حفظ.

  ── لماذا لا يكفي تعديل index وحده ──
  save() يبني جملة INSERT من LIQ_COLS **حرفياً**. أي مفتاح يرسله index
  وليس في القائمة يُرمى بصمت بلا رسالة خطأ. فالتعديلان حزمة واحدة.

  ── ما أُضيف (تسعة أعمدة) ──
    gex          نظام الحركة: سالب يمدّها · موجب يبتلعها
    vex          تعرّض الفانّا — اتجاهي · يعمل حين يتحرّك VIX0D
    chex         تعرّض التشارم — اتجاهي · أثره آخر 90 دقيقة
    flip         مستوى انقلاب الغاما
    flip_dist    بُعد السعر عنه (موجب = فوقه)
    call_wall    جدار الكول بوزن GEX — غير جدار OI المحفوظ أصلاً
    put_wall     جدار البوت بوزن GEX
    atm_iv       التقلّب الضمني عند السعر — يلزم لقياس تغيّره لاحقاً
    hours_left   ساعات حتى الانتهاء — وزن التشارم يتبعها

  ⚠ صفر تغيير في المنطق: لا حساب جديد ولا نداء جديد ولا قرار.
    الأرقام تصل جاهزة من /snap وتُحفظ كما هي.
  ⚠ تبقى فارغة إن غابت الإغريق — كبقية الحقول الاختيارية.
  ⚠ لا تظهر في رسالة تيليجرام — تُقرأ من /liq.csv عند التحليل.
  ⚠ يتطلب index v1.8.2. مع index أقدم تُحفظ فارغة ولا ينكسر شيء.

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.3 — حفظ الأرقام الخام للنافذة القصيرة ★★

  ── المشكلة ──
  v2.2 يحسب flow_edge = معدّل آخر ~5 دقائق ÷ معدّل الـ15 دقيقة، ثم يحفظ
  النسبة **ويهمل البسط**. النسبة تجيب «أين وقع النشاط داخل النافذة» ولا
  تجيب «كم كان النشاط في تلك الدقائق». والرقم الخام لا يمكن اشتقاقه
  لاحقاً من النسبة — يُفقد نهائياً إن لم يُحفظ.

  ── لماذا يهمّ ──
  السؤال المطروح: هل نافذة 15 دقيقة هي الأنسب لاستراتيجية إشارتها على
  فاصل 5 دقائق؟ لا يُجاب بالحدس. بحفظ كول/بوت الخامين للنافذة القصيرة
  مع عمرها الفعلي، نستطيع بعد 30 إشارة قياس النافذتين على **البيانات
  نفسها** ومقارنة أيّهما يفصل الرابح من الخاسر.

  ── ما أُضيف ──
    flow_edge_call   كول النافذة القصيرة — النطاق active (رتبة 3–8)
    flow_edge_put    بوت النافذة القصيرة — النطاق نفسه
    flow_edge_win    عمر لقطة الحافة الفعلي بالدقائق (ليس 5 دائماً)

  ⚠ النطاق active نفسه المستخدم في flow_bias_active — فالمقارنة عادلة.
  ⚠ صفر تغيير في المنطق: flow_bias · flow_accel · flow_edge · flow_align
    كلها كما هي حرفياً. الإضافة حفظ فقط.
  ⚠ لا تظهر في رسالة تيليجرام — تُقرأ من /liq.csv عند التحليل.

  ─────────────────────────────────────────────────────────────────────────
  ★★ v2.0 — تدفّق آخر 15 دقيقة ★★

  ── المبدأ ──
  حجم الخيارات **تراكمي** منذ ما قبل الافتتاح ولا ينخفض أبداً.
  ⇒ الفرق بين لقطتين = ما تُدووِل في تلك الفترة بالضبط.

  ⚠ الطرح يتم **لكل سترايك على حدة** لا على المجموع.
    السبب: السعر يتحرك، فالسترايك يدخل النافذة أو يخرج منها. الطرح على
    مجموع «فوق/تحت» يقيس حركة السعر لا التدفّق — وهذا خطأ وقعنا فيه
    فعلاً في 4 سبتمبر 2026 وصحّحناه: بين لقطتَي 12:50 و13:10 «انخفض»
    حجم ما تحت السعر من 749k إلى 676k، وهو مستحيل في رقم تراكمي.
    السبب أن السعر نزل فانتقلت سترايكات من خانة «تحت» إلى «فوق».

  ⚠ رصيد ما قبل الافتتاح يسقط تلقائياً في الفرق لأنه موجود في اللقطتين
    بالتساوي. لا حاجة لتعطيله ولا لطرحه يدوياً.

  ── النطاقات الثلاثة (رتبة السترايك من السعر) ──
    near    رتبة 1–4   (~5–20 نقطة)  ATM وحوله — تحوّط وإغلاق ودفاع
    active  رتبة 3–8   (~15–40 نقطة) منطقة الرهان الاتجاهي ⭐ المرشّح الأقوى
    wide    رتبة 1–10  (~50 نقطة)    مرجع عام
  ثلاثتها تُحسب وتُسجَّل. بعد 30 إشارة تخبرنا البيانات أيها يفصل الرابح
  من الخاسر — وحينها يُحذف الاثنان الآخران.

  ── الميل ──
    flow_bias = (تدفّق الكول − تدفّق البوت) ÷ مجموعهما     من −1 إلى +1
  ⚠ لا يقول من المشتري ومن البائع — كل صفقة لها طرفان. يقول أين تتركّز
    الحرارة. الإشارة احتمالية لا قاطعة.

  ── التسارع ──
    flow_accel = تدفّق آخر 15د ÷ تدفّق الـ15د التي تسبقها
  ⚠ لا يُقارن بمتوسط اليوم: في الساعة الأولى يكون المتوسط محسوباً على
    دقائق قليلة معظمها افتتاح (أنشط ما في اليوم) ⇒ مقام مضخّم ونسبة
    كاذبة. المقارنة بالنافذة السابقة تعمل من ثلاث لقطات وأصدق مفهومياً.

  ── الموافقة ──
    flow_align = هل flow_bias_active يوافق اتجاه الإشارة؟
      CALL مع ميل موجب ⇒ AGREE · CALL مع ميل سالب ⇒ DISAGREE
      |ميل| < FLOW_NEUTRAL ⇒ NEUTRAL
  الاختبار بعد 30 إشارة: نسبة الفوز في AGREE مقابل DISAGREE.

  ⚠⚠ صفر قرارات. تسجيل فقط. لا بوابة ولا فلتر ولا تأثير على دخول أو
     خروج أو أهداف أو أوقات. لن يدخل أي قرار قبل 30 إشارة على الأقل.

  ⚠ اختبار إبطال مسبق: قبل أي تحليل للفوز والخسارة يُحسب ارتباط
    flow_bias بحركة السعر في الدقائق الخمس السابقة. إن تجاوز 0.7 فهو
    يعيد قراءة الشارت لا أكثر ⇒ يُغلق الملف بلا إضاعة 30 عينة.

  ─────────────────────────────────────────────────────────────────────────
  v1.0 — التقاط لقطة السيولة عند كل إشارة

  ── مبدأ العزل (بلا تغيير) ──
  • اتجاه واحد: البوت يقرأ من اللوحة. اللوحة لا تعرف بوجود البوت.
  • لا تمسّ trades_v3 ولا quotes_v3 ولا reverse_test_v1 — جدول liq_snaps.
  • كل دالة ملفوفة بـtry/except شاملة. أي فشل يرجع فارغاً والبوت يمضي.
  • مهلة قصيرة (LIQ_TIMEOUT) فلا تؤخّر أي مسار.

  ── الحقل الأثمن ──
  table_json = السلّم كاملاً [سترايك, حجم كول, حجم بوت, OI كول, OI بوت]
  كل حقول التدفّق تُشتق منه. لو غيّرنا أي تعريف لاحقاً نعيد الحساب على
  المحفوظ بلا جمع جديد. الحقول المشتقة قد تصبح خاطئة؛ اللقطة الخام لا.

  ── الإعداد ──
  LIQ_URL          رابط اللوحة (بلا شرطة أخيرة)
  LIQ_ENABLED      1 تفعيل · 0 إيقاف بلا تعديل كود
  LIQ_TIMEOUT      مهلة الطلب بالثواني (3)
  LIQ_UND          أداة السيولة (SPX)
  LIQ_STRIKES      عدد السترايكات في اللقطة الخام (30)
  FLOW_WINDOW_MIN  نافذة التدفّق بالدقائق (15)
  FLOW_MAX_AGE_MIN أقصى عمر مقبول للقطة المرجعية (25)
  FLOW_NEUTRAL     عتبة الحياد في الميل (0.15)
  FLOW_EDGE_MIN    أدنى عمر مقبول للقطة الحافة (4)
  FLOW_EDGE_MAX    أقصى عمر مقبول للقطة الحافة (9)
═══════════════════════════════════════════════════════════════════════════════
"""

import json
import os
import threading
import time
from collections import deque
from datetime import datetime, timedelta

import httpx

LIQ_URL      = os.getenv("LIQ_URL", "https://spxvolumekhalid.vercel.app").rstrip("/")
LIQ_ENABLED  = os.getenv("LIQ_ENABLED", "1") == "1"
LIQ_TIMEOUT  = float(os.getenv("LIQ_TIMEOUT", "3"))
LIQ_UND      = os.getenv("LIQ_UND", "SPX").strip().upper()
LIQ_STRIKES  = int(os.getenv("LIQ_STRIKES", "30"))

# ── [v2.0] إعدادات التدفّق ──
FLOW_WINDOW_MIN  = float(os.getenv("FLOW_WINDOW_MIN", "15"))
FLOW_MAX_AGE_MIN = float(os.getenv("FLOW_MAX_AGE_MIN", "25"))
FLOW_NEUTRAL     = float(os.getenv("FLOW_NEUTRAL", "0.15"))

# ── [v2.2] نافذة الحافة — أين وقع النشاط داخل الـ15 دقيقة ──
#  المشكلة: 16k بوت قد تكون كلها في الدقيقة الأولى (حركة انتهت) أو
#  في الأخيرة (حركة تبدأ). النافذة الكاملة تعطي الرقم نفسه في الحالتين،
#  وflow_accel لا يحلّها لأنه يقارن نافذتين كاملتين لا داخل الحالية.
#    flow_edge = (تدفّق آخر 5د ÷ دقائقها) ÷ (تدفّق الـ15د ÷ دقائقها)
#    ~1.0 موزّع · >1.6 يحدث الآن · <0.5 حدث في أول النافذة (منتهٍ)
FLOW_EDGE_MIN    = float(os.getenv("FLOW_EDGE_MIN", "4"))
FLOW_EDGE_MAX    = float(os.getenv("FLOW_EDGE_MAX", "9"))
FLOW_EDGE_HOT    = float(os.getenv("FLOW_EDGE_HOT", "1.6"))

# ── [v2.6] كشف انطلاق التدفّق ──
#  الانطلاق = الميل كان دون FLOW_NEUTRAL وصار ≥ FLOW_ONSET_MIN.
#  «الساخن» = انطلاق يرافقه تسارع ≥ FLOW_ONSET_ACCEL — وهو وحده ما
#  أظهر حافة في المحاكاة (69% عند 2.0 · 64% عند 1.5 · خط أساس 48%).
FLOW_ONSET_MIN   = float(os.getenv("FLOW_ONSET_MIN", "0.15"))
FLOW_ONSET_ACCEL = float(os.getenv("FLOW_ONSET_ACCEL", "1.5"))
#  أقصى عمر مقبول للقطة السابقة. أكبر منه = فجوة، فلا يُحكم بانطلاق
#  (فتح جلسة جديدة أو انقطاع cron) — وإلا صار كل صباح «انطلاقاً» كاذباً.
FLOW_PREV_MAX    = float(os.getenv("FLOW_PREV_MAX", "10"))

# النطاقات برتبة السترايك من السعر (1 = الأقرب)
FLOW_RANGES = {
    "near":   (1, 4),
    "active": (3, 8),
    "wide":   (1, 10),
}

VERSION = "3.0.1"

# ── [v2.8] سلسلة المسيطر ──
AGG_SERIES_MAX = int(os.getenv("AGG_SERIES_MAX", "420"))   # دقائق الجلسة
# عتبات القرار — مطابقة index v2.1.x حرفياً
VD_GATE   = float(os.getenv("VWAP_GATE_SPY", "0.40"))
VD_BULL   = 55.0
VD_BEAR   = 45.0

# ── [v2.7] المسيطر — جامع خلفي ──
AGG_ENABLED  = os.getenv("AGG_ENABLED", "1") == "1"
AGG_SEC      = float(os.getenv("AGG_SEC", "5"))       # دورة الجمع
AGG_STRIKES  = int(os.getenv("AGG_STRIKES", "15"))    # سترايكات فوق وتحت
AGG_WIN_SEC  = 300.0                                  # نافذة القراءة
AGG_GAP_SEC  = 30.0                                   # فجوة أكبر ⇒ لا نسب
AGG_MIN_CLS  = 200                                    # أقل حجم مصنّف للقراءة
AGG_BUY, AGG_SELL = 0.6, 0.4
_AGG = {"prev": None, "prev_t": 0.0, "exp": None,
        "ev": deque(maxlen=200), "spot": None, "spot_t": 0.0,
        "thread": None, "ticks": 0, "errs": 0, "last_err": None,
        "last_ok": None,
        # [v2.8] سلسلة اليوم: {دقيقة NY: نسبة الضغط الصعودي}
        "series": {}, "series_day": None, "series_restored": False}
_AGG_LOCK = threading.Lock()


# ═══════════════════════════════════════════════════════════════════════════
#  [v2.5] عميل HTTP مشترك — إصلاح تسرّب الذاكرة
# ═══════════════════════════════════════════════════════════════════════════
#  العطل (17 سبتمبر 2026): منحنى ذاكرة Render سنّ منشار — يتسلّق من 15%
#  إلى 100% ثم يسقط، سبع مرات في 12 ساعة. السقوط ليس تحريراً بل قتل
#  العملية عند 512MB وإعادة تشغيلها.
#  السبب: كل نداء بصيغة httpx.get(...) يبني عميلاً **وسياق SSL** جديدين
#  ويتركهما للـGC. سياق SSL يزن مئات الكيلوبايتات، والاتصال لا يُعاد
#  استخدامه. القياس: ~1.4MB لكل دورة استطلاع، والتسرّب يتناسب مع عدد
#  الطلبات لا عدد الصفقات — وهو ما يفسّر تسارع المنحنى بعد الافتتاح.
#  ⚠ الخطر تداولي لا تقني فقط: إعادة التشغيل تقتل مؤقّت الدورة الفرعية،
#    فيتوقّف تتبّع الوقف المتحرك حتى وصول /poll التالي.
#
#  الإصلاح: عميل واحد يُبنى مرة ويُعاد استخدامه. الذاكرة تستقر، ومصافحة
#  TLS تسقط من كل نداء (keep-alive) فتقلّ زمن الاستجابة أيضاً.
#  ⚠ صفر تغيير في السلوك: المهلة تبقى تُمرَّر لكل نداء على حدة، والردود
#    ومعالجة الأخطاء كما هي حرفياً.

_HTTP_LIMITS = httpx.Limits(max_keepalive_connections=2,
                            max_connections=4,
                            keepalive_expiry=30.0)
_HTTP = {"c": None}
_HTTP_LOCK = threading.Lock()


def _http():
    """العميل المشترك — يُبنى عند أول نداء فقط."""
    c = _HTTP["c"]
    if c is None:
        with _HTTP_LOCK:
            if _HTTP["c"] is None:
                _HTTP["c"] = httpx.Client(timeout=LIQ_TIMEOUT,
                                          limits=_HTTP_LIMITS,
                                          headers={"User-Agent": "spx-liq/2.7"})
            c = _HTTP["c"]
    return c


def _http_reset():
    """يغلق العميل ويُجبر بناء واحد جديد عند النداء التالي.

       يُستدعى عند خطأ نقل (اتصال مقطوع · مهلة · TLS) حتى لا يعلق البوت
       على عميل تالف. الإغلاق يحرّر الاتصالات فوراً بدل انتظار الـGC."""
    with _HTTP_LOCK:
        c = _HTTP["c"]
        _HTTP["c"] = None
    if c is not None:
        try:
            c.close()
        except Exception:
            pass


# ── خطّافات من server.py (تُضبط عند الإقلاع) ──
_H = {"tg_send": None, "db_execute": None, "db_query": None, "ny_now": None}


def set_hooks(tg_send=None, db_execute=None, db_query=None, ny_now=None):
    """يستقبل دوال server.py. لا يستورد liq.py أي شيء من server.py.

       [v2.0] db_query جديد — لازم لقراءة اللقطة المرجعية من liq_snaps.
       بدونه تعمل الوحدة كاملة لكن حقول التدفّق تبقى فارغة."""
    if tg_send is not None:
        _H["tg_send"] = tg_send
    if db_execute is not None:
        _H["db_execute"] = db_execute
    if db_query is not None:
        _H["db_query"] = db_query
    if ny_now is not None:
        _H["ny_now"] = ny_now


LIQ_COLS = [
    "id", "sig_key", "tag", "captured_ny",
    "bot_und", "bot_side", "bot_strike", "reject_reason",
    "liq_und", "expiration", "session", "spot", "spot_other", "px_ratio",
    "chg_pct", "vix", "vix1d",
    "oi_up_strike", "oi_up_oi", "oi_up_dist", "oi_up_in_target",
    "oi_dn_strike", "oi_dn_oi", "oi_dn_dist", "oi_dn_in_target",
    "wall_span", "vol_above", "vol_below", "ratio_up_dn",
    "call_vol_total", "put_vol_total", "pc_ratio",
    "atm_strike", "atm_cp_ratio", "atm_cp_weak",
    # ── [v2.0] حقول التدفّق ──
    "flow_window_min", "flow_call_15m", "flow_put_15m",
    "flow_bias_near", "flow_bias_active", "flow_bias_wide",
    "flow_accel", "flow_edge",
    # ── [v2.3] الأرقام الخام للنافذة القصيرة ──
    "flow_edge_call", "flow_edge_put", "flow_edge_win",
    "flow_align", "flow_ref_ny",
    # ── [v2.6] انطلاق التدفّق ──
    "flow_prev_bias", "flow_prev_age", "flow_onset",
    "flow_onset_dir", "flow_onset_hot",
    # ── [v2.4] التموضع — من /snap مباشرة، لا يُحسب هنا ──
    "gex", "vex", "chex", "flip", "flip_dist",
    "call_wall", "put_wall", "atm_iv", "hours_left",
    # ── [v2.7] المسيطر + قراءة اللحظة ──
    "agg_cb", "agg_cs", "agg_pb", "agg_ps", "agg_unc", "agg_cov_sec",
    "agg_buy_pct", "agg_bull_pct",
    "vwap_spy", "vwap_dist_spy", "vwap_dist_und", "vwap_call_ok",
    "vwap_put_ok", "em_pts", "em_hi", "em_lo", "em_src",
    # ── [v2.8] القرار ونطاق اليوم ──
    "verdict", "verdict_regime", "verdict_tgt", "verdict_inv", "verdict_rr",
    "day_high", "day_low", "day_range",
    "table_json", "ok", "err",
]

# ── [v2.9] قرار اللوحة من الخادم — صف لكل قرار (tag = dash_dec) ──
DEC_COLS = [
    "dec_id", "dec_side", "dec_t", "dec_tk", "dec_why", "dec_tgt_n", "dec_inv_n",
    "dec_csym", "dec_ck", "dec_ca", "dec_cv", "dec_c0", "dec_cnow",
    "dec_hi", "dec_hi_t", "dec_lo", "dec_lo_t", "dec_tgt_t", "dec_inv_t",
    "dec_mfe", "dec_mae", "dec_spnow", "dec_end", "dec_bars",
]
_DEC_TXT = {"dec_side", "dec_t", "dec_tk", "dec_why", "dec_tgt_n", "dec_inv_n",
            "dec_csym", "dec_hi_t", "dec_lo_t", "dec_tgt_t", "dec_inv_t", "dec_end"}
LIQ_COLS = LIQ_COLS + DEC_COLS

# ── [v3.0] بوت السيولة — صف لكل صفقة (tag = liq_bot) ──
LB_COLS = [
    "lb_id", "lb_side", "lb_t", "lb_tk", "lb_grade", "lb_why", "lb_room",
    "lb_obst", "lb_bull", "lb_bias", "lb_fcall", "lb_fput", "lb_fage",
    "lb_in_zone", "lb_zone_lo", "lb_zone_hi", "lb_zones", "lb_open",
    "lb_move_open", "lb_hi15", "lb_lo15", "lb_hi30", "lb_lo30",
    "lb_csym", "lb_ck", "lb_cband", "lb_c0", "lb_ca0", "lb_cb0",
    "lb_state", "lb_peak", "lb_arm_t", "lb_exit_t", "lb_exit_mid",
    "lb_exit_bid", "lb_reason", "lb_pnl_mid", "lb_pnl_real",
    "lb_chi", "lb_chi_t", "lb_clo", "lb_clo_t",
    "lb_t10", "lb_t15", "lb_t20", "lb_mae10", "lb_mae15", "lb_mae20",
    "lb_mfe", "lb_mfe_t", "lb_mae", "lb_end", "lb_gap", "lb_path",
]
_LB_TXT = {"lb_side", "lb_t", "lb_tk", "lb_grade", "lb_why", "lb_obst",
           "lb_in_zone", "lb_zones", "lb_csym", "lb_cband", "lb_state",
           "lb_arm_t", "lb_exit_t", "lb_reason", "lb_chi_t", "lb_clo_t",
           "lb_t10", "lb_t15", "lb_t20", "lb_mfe_t", "lb_end", "lb_path"}
LIQ_COLS = LIQ_COLS + LB_COLS

# الأعمدة المضافة بعد v1.0 — تُرحَّل بـALTER آمن للتكرار
_V2_COLS = [
    ("flow_window_min",  "num"), ("flow_call_15m",   "num"),
    ("flow_put_15m",     "num"), ("flow_bias_near",  "num"),
    ("flow_bias_active", "num"), ("flow_bias_wide",  "num"),
    ("flow_accel",       "num"), ("flow_edge",       "num"),
    # [v2.3]
    ("flow_edge_call",   "num"), ("flow_edge_put",   "num"),
    ("flow_edge_win",    "num"),
    ("flow_align",       "txt"),
    ("flow_ref_ny",      "txt"),
    # [v2.6]
    ("flow_prev_bias",   "num"), ("flow_prev_age",   "num"),
    ("flow_onset",       "num"), ("flow_onset_hot",  "num"),
    ("flow_onset_dir",   "txt"),
    # [v2.4]
    ("gex",              "num"), ("vex",             "num"),
    ("chex",             "num"), ("flip",            "num"),
    ("flip_dist",        "num"), ("call_wall",       "num"),
    ("put_wall",         "num"), ("atm_iv",          "num"),
    ("hours_left",       "num"),
    # [v2.7]
    ("agg_cb", "num"), ("agg_cs", "num"), ("agg_pb", "num"),
    ("agg_ps", "num"), ("agg_unc", "num"), ("agg_cov_sec", "num"),
    ("agg_buy_pct", "num"), ("agg_bull_pct", "num"),
    ("vwap_spy", "num"), ("vwap_dist_spy", "num"), ("vwap_dist_und", "num"),
    ("vwap_call_ok", "txt"), ("vwap_put_ok", "txt"),
    ("em_pts", "num"), ("em_hi", "num"), ("em_lo", "num"),
    ("em_src", "txt"),
    # [v2.8]
    ("verdict", "txt"), ("verdict_regime", "txt"), ("verdict_tgt", "num"),
    ("verdict_inv", "num"), ("verdict_rr", "num"),
    ("day_high", "num"), ("day_low", "num"), ("day_range", "num"),
] + [(c, "txt" if c in _DEC_TXT else "num") for c in DEC_COLS] \
  + [(c, "txt" if c in _LB_TXT else "num") for c in LB_COLS]       # [v2.9 · v3.0]


def db_init_liq(db_execute=None, use_pg=False):
    """ينشئ جدول liq_snaps ويرحّل أعمدة v2.x. آمن للتكرار."""
    ex = db_execute or _H["db_execute"]
    if ex is None:
        return False
    num = "DOUBLE PRECISION" if use_pg else "REAL"
    pk = "BIGSERIAL PRIMARY KEY" if use_pg else "INTEGER PRIMARY KEY AUTOINCREMENT"
    try:
        ex(f"""CREATE TABLE IF NOT EXISTS liq_snaps(
            id {pk},
            sig_key TEXT, tag TEXT, captured_ny TEXT,
            bot_und TEXT, bot_side TEXT, bot_strike {num}, reject_reason TEXT,
            liq_und TEXT, expiration TEXT, session TEXT,
            spot {num}, spot_other {num}, px_ratio {num},
            chg_pct {num}, vix {num}, vix1d {num},
            oi_up_strike {num}, oi_up_oi {num}, oi_up_dist {num},
            oi_up_in_target TEXT,
            oi_dn_strike {num}, oi_dn_oi {num}, oi_dn_dist {num},
            oi_dn_in_target TEXT,
            wall_span {num}, vol_above {num}, vol_below {num}, ratio_up_dn {num},
            call_vol_total {num}, put_vol_total {num}, pc_ratio {num},
            atm_strike {num}, atm_cp_ratio {num}, atm_cp_weak TEXT,
            flow_window_min {num}, flow_call_15m {num}, flow_put_15m {num},
            flow_bias_near {num}, flow_bias_active {num}, flow_bias_wide {num},
            flow_accel {num}, flow_edge {num},
            flow_edge_call {num}, flow_edge_put {num}, flow_edge_win {num},
            flow_align TEXT, flow_ref_ny TEXT,
            flow_prev_bias {num}, flow_prev_age {num},
            flow_onset {num}, flow_onset_dir TEXT, flow_onset_hot {num},
            gex {num}, vex {num}, chex {num},
            flip {num}, flip_dist {num},
            call_wall {num}, put_wall {num},
            atm_iv {num}, hours_left {num},
            agg_cb {num}, agg_cs {num}, agg_pb {num}, agg_ps {num},
            agg_unc {num}, agg_cov_sec {num},
            agg_buy_pct {num}, agg_bull_pct {num},
            vwap_spy {num}, vwap_dist_spy {num}, vwap_dist_und {num},
            vwap_call_ok TEXT, vwap_put_ok TEXT,
            em_pts {num}, em_hi {num}, em_lo {num}, em_src TEXT,
            verdict TEXT, verdict_regime TEXT,
            verdict_tgt {num}, verdict_inv {num}, verdict_rr {num},
            day_high {num}, day_low {num}, day_range {num},
            table_json TEXT, ok TEXT, err TEXT)""")
    except Exception as e:
        print("liq db_init err:", e)
        return False

    # ترحيل الأعمدة الجديدة على الجداول القائمة من نسخ أقدم
    for col, kind in _V2_COLS:
        typ = num if kind == "num" else "TEXT"
        try:
            if use_pg:
                ex(f"ALTER TABLE liq_snaps ADD COLUMN IF NOT EXISTS {col} {typ}")
            else:
                ex(f"ALTER TABLE liq_snaps ADD COLUMN {col} {typ}")
        except Exception:
            pass
    return True


def make_key(ny_dt, side, strike=None):
    """مفتاح ربط اللقطة بصفها: YYYY-MM-DD_HHMM_SIDE_STRIKE."""
    try:
        stamp = ny_dt.strftime("%Y-%m-%d_%H%M")
    except Exception:
        stamp = "unknown"
    k = f"{stamp}_{str(side or '?').upper()}"
    if strike:
        try:
            k += f"_{float(strike):.0f}"
        except (TypeError, ValueError):
            pass
    return k


def fetch(sig_key="", tag=""):
    """يجلب لقطة واحدة من اللوحة. يرجع dict دائماً — لا يرمي أبداً."""
    if not LIQ_ENABLED:
        return {"ok": False, "err": "LIQ_ENABLED=0"}
    try:
        r = _http().get(f"{LIQ_URL}/snap", timeout=LIQ_TIMEOUT,
                        params={"u": LIQ_UND, "n": LIQ_STRIKES,
                                "key": sig_key, "tag": tag})
        if r.status_code != 200:
            return {"ok": False, "err": f"HTTP {r.status_code}"}
        js = r.json()
        if not isinstance(js, dict):
            return {"ok": False, "err": "رد غير متوقع"}
        return js
    except Exception as e:
        # [v2.5] اتصال تالف ⇒ ابنِ عميلاً جديداً للنداء التالي
        if isinstance(e, getattr(httpx, "TransportError", Exception)):
            _http_reset()
        return {"ok": False, "err": f"{type(e).__name__}: {e}"}


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _yn(x):
    if x is None:
        return None
    return "YES" if x else "NO"


# ═══════════════════════════════════════════════════════════════════════════
#  [v2.0] حساب التدفّق
# ═══════════════════════════════════════════════════════════════════════════

def _parse_ny(s):
    """يقرأ captured_ny بصيغة 'YYYY-MM-DD HH:MM:SS'. يرجع datetime أو None."""
    try:
        return datetime.strptime(str(s)[:19], "%Y-%m-%d %H:%M:%S")
    except Exception:
        try:
            return datetime.fromisoformat(str(s)[:19])
        except Exception:
            return None


def _as_maps(table_json):
    """يحوّل السلّم إلى {سترايك: حجم} للكول والبوت.

       يقبل قائمة أو نصاً JSON. الصف: [سترايك, كول_حجم, بوت_حجم, ...]"""
    try:
        tj = table_json
        if isinstance(tj, str):
            tj = json.loads(tj)
        if not isinstance(tj, list):
            return None, None
        cm, pm = {}, {}
        for row in tj:
            if not isinstance(row, (list, tuple)) or len(row) < 3:
                continue
            k = _num(row[0])
            if k is None:
                continue
            cm[k] = _num(row[1]) or 0.0
            pm[k] = _num(row[2]) or 0.0
        return (cm, pm) if cm else (None, None)
    except Exception as e:
        print("liq _as_maps err:", e)
        return None, None


def _ranked(strikes, spot):
    """يرتّب السترايكات برتبتها من السعر لكل جهة على حدة.

       يرجع {سترايك: رتبة} حيث 1 = الأقرب للسعر. الرتبة تُحسب داخل
       الجهة (فوق/تحت) فتبقى النافذة متوازنة مهما كان توزيع السلّم."""
    out = {}
    if spot is None:
        return out
    above = sorted([k for k in strikes if k > spot], key=lambda k: k - spot)
    below = sorted([k for k in strikes if k <= spot], key=lambda k: spot - k)
    for i, k in enumerate(above, 1):
        out[k] = i
    for i, k in enumerate(below, 1):
        out[k] = i
    return out


def _flow_between(cur_tj, ref_tj, spot):
    """تدفّق كل نطاق بين لقطتين — الطرح لكل سترايك على حدة.

       يرجع dict فيه لكل نطاق (call, put, total, bias) أو None."""
    c1, p1 = _as_maps(cur_tj)
    c0, p0 = _as_maps(ref_tj)
    if not c1 or not c0:
        return None
    rank = _ranked(set(c1) & set(c0), spot)
    if not rank:
        return None

    out = {}
    for name, (lo, hi) in FLOW_RANGES.items():
        C = P = 0.0
        for k, r in rank.items():
            if not (lo <= r <= hi):
                continue
            # الحجم تراكمي ⇒ الفرق لا يكون سالباً إلا بخطأ بيانات
            C += max(0.0, (c1.get(k, 0.0) - c0.get(k, 0.0)))
            P += max(0.0, (p1.get(k, 0.0) - p0.get(k, 0.0)))
        tot = C + P
        out[name] = {
            "call": round(C, 1), "put": round(P, 1), "total": round(tot, 1),
            "bias": (round((C - P) / tot, 3) if tot > 0 else None),
        }
    return out


def _per_strike(cur_tj, ref_tj, spot, limit=8):
    """[v2.1] تدفّق كل سترايك على حدة — للعرض البصري في اللوحة.

       يرجع قائمة [{strike, call, put}] لأقرب limit سترايك فوق وتحت."""
    c1, p1 = _as_maps(cur_tj)
    c0, p0 = _as_maps(ref_tj)
    if not c1 or not c0 or spot is None:
        return None
    common = set(c1) & set(c0)
    ab = sorted([k for k in common if k > spot])[:limit]
    be = sorted([k for k in common if k <= spot], reverse=True)[:limit]
    out = []
    for k in sorted(set(ab) | set(be), reverse=True):
        out.append({"strike": k,
                    "call": round(max(0.0, c1.get(k, 0) - c0.get(k, 0)), 1),
                    "put":  round(max(0.0, p1.get(k, 0) - p0.get(k, 0)), 1)})
    return out


def _recent_rows(liq_und, now_ny, db_query=None):
    """آخر لقطات نفس الأداة خلال ساعة — للبحث عن المرجع.

       يرجع قائمة [(datetime, table_json)] مرتّبة من الأحدث للأقدم."""
    q = db_query or _H["db_query"]
    if q is None:
        return []
    try:
        since = (now_ny - timedelta(minutes=70)).strftime("%Y-%m-%d %H:%M:%S")
        rows = q("SELECT captured_ny, table_json FROM liq_snaps "
                 "WHERE liq_und = ? AND captured_ny >= ? AND table_json IS NOT NULL "
                 "ORDER BY id DESC LIMIT 40", (liq_und, since))
        out = []
        for ts, tj in rows:
            dt = _parse_ny(ts)
            if dt is not None and tj:
                out.append((dt, tj))
        return out
    except Exception as e:
        print("liq _recent_rows err:", e)
        return []


def _prev_flow(liq_und, now_ny, db_query=None):
    """[v2.6] ميل اللقطة السابقة مباشرة — أساس كشف الانطلاق.

       صف واحد بـLIMIT 1: أحدث لقطة لنفس الأداة تحمل ميلاً محسوباً.
       يرجع (bias, age_min) أو (None, None).

       ⚠ عمداً لا تشترط تاريخ اليوم: الشرط الزمني يُطبَّق في المستدعي
         عبر FLOW_PREV_MAX، فلو كانت السابقة أمس صار العمر بالمئات
         ورُفضت تلقائياً. هذا يمنع «انطلاقاً» كاذباً كل صباح."""
    q = db_query or _H["db_query"]
    if q is None:
        return None, None
    try:
        rows = q("SELECT captured_ny, flow_bias_active FROM liq_snaps "
                 "WHERE liq_und = ? AND flow_bias_active IS NOT NULL "
                 "ORDER BY id DESC LIMIT 1", (liq_und,))
        if not rows:
            return None, None
        ts, b = rows[0]
        dt = _parse_ny(ts)
        if dt is None or b is None:
            return None, None
        age = (now_ny - dt).total_seconds() / 60.0
        if age <= 0:
            return None, None
        return float(b), round(age, 1)
    except Exception as e:
        print("liq _prev_flow err:", e)
        return None, None


def compute_flow(row, side=None, db_query=None):
    """يحسب حقول التدفّق للقطة الحالية. يرجع dict — فارغاً عند التعذّر.

       المرجع: أقرب لقطة عمرها ≥ FLOW_WINDOW_MIN و≤ FLOW_MAX_AGE_MIN.
       المرجع الثاني (للتسارع): أقرب لقطة عمرها ≥ ضعف النافذة.
       لقطة الحافة: أحدث لقطة عمرها بين FLOW_EDGE_MIN وFLOW_EDGE_MAX.

       ⚠ يُستدعى **بعد** حفظ اللقطة الحالية؟ لا — قبله. اللقطة الحالية
         تأتي من الرد لا من الجدول، فلا تُحسب مرجعاً لنفسها."""
    empty = {"flow_window_min": None, "flow_call_15m": None,
             "flow_put_15m": None, "flow_bias_near": None,
             "flow_bias_active": None, "flow_bias_wide": None,
             "flow_accel": None, "flow_edge": None,
             "flow_edge_call": None, "flow_edge_put": None,
             "flow_edge_win": None,
             "flow_align": None, "flow_ref_ny": None,
             "flow_prev_bias": None, "flow_prev_age": None,
             "flow_onset": None, "flow_onset_dir": None,
             "flow_onset_hot": None}
    try:
        if not isinstance(row, dict) or not row.get("ok"):
            return empty
        cur_tj = row.get("table_json")
        if not cur_tj:
            return empty
        now_ny = _parse_ny(row.get("ts_ny"))
        if now_ny is None:
            return empty
        spot = _num(row.get("spot"))
        if spot is None:
            return empty

        hist = _recent_rows(row.get("underlying") or LIQ_UND, now_ny,
                            db_query=db_query)
        if not hist:
            return empty

        # ── المرجع الأول: أحدث لقطة عمرها ≥ النافذة ──
        ref1 = ref2 = None
        for dt, tj in hist:                     # مرتّبة من الأحدث للأقدم
            age = (now_ny - dt).total_seconds() / 60.0
            if age <= 0:
                continue
            if ref1 is None and age >= FLOW_WINDOW_MIN:
                if age > FLOW_MAX_AGE_MIN:
                    break                       # الفجوة أكبر من المقبول
                ref1 = (dt, tj, age)
                continue
            if ref1 is not None and ref2 is None and age >= FLOW_WINDOW_MIN * 2:
                if age > FLOW_MAX_AGE_MIN * 2:
                    break
                ref2 = (dt, tj, age)
                break
        if ref1 is None:
            return empty

        cur = _flow_between(cur_tj, ref1[1], spot)
        if cur is None:
            return empty

        act = cur.get("active", {})
        res = {
            "flow_window_min": round(ref1[2], 1),
            "flow_call_15m": act.get("call"),
            "flow_put_15m": act.get("put"),
            "flow_bias_near": (cur.get("near") or {}).get("bias"),
            "flow_bias_active": act.get("bias"),
            "flow_bias_wide": (cur.get("wide") or {}).get("bias"),
            "flow_accel": None, "flow_edge": None,
            "flow_edge_call": None, "flow_edge_put": None,
            "flow_edge_win": None,
            "flow_align": None,
            "flow_ref_ny": ref1[0].strftime("%Y-%m-%d %H:%M:%S"),
            "flow_prev_bias": None, "flow_prev_age": None,
            "flow_onset": 0, "flow_onset_dir": None, "flow_onset_hot": 0,
        }

        # ── التسارع: النافذة الحالية ÷ النافذة السابقة لها ──
        if ref2 is not None:
            prev = _flow_between(ref1[1], ref2[1], spot)
            if prev:
                pt = (prev.get("active") or {}).get("total") or 0.0
                ct = act.get("total") or 0.0
                if pt > 0:
                    res["flow_accel"] = round(ct / pt, 2)

        # ── [v2.2] الحافة: نصيب آخر ~5 دقائق من تدفّق النافذة ──
        #  يفرّق بين نشاط يحدث الآن ونشاط انتهى في أول النافذة.
        #
        #  [v2.3] تُحفظ الأرقام الخام أيضاً لا النسبة وحدها.
        #  السبب: النسبة تجيب «أين وقع النشاط» ولا تجيب «كم كان».
        #  بحفظ الخام نستطيع بعد 30 إشارة قياس نافذة الخمس دقائق
        #  كمؤشر مستقل ومقارنتها بنافذة الـ15 على البيانات نفسها،
        #  بدل اختيار طول النافذة بالحدس. المعلومة تُفقد نهائياً
        #  إن لم تُحفظ — لا يمكن اشتقاقها لاحقاً من النسبة.
        #  ⚠ flow_edge_win هو العمر الفعلي للقطة لا 5 دائماً — الـcron
        #    كل 3 دقائق فالمدى العملي 4–9.
        try:
            edge = None
            for dt, tj in hist:
                age = (now_ny - dt).total_seconds() / 60.0
                if FLOW_EDGE_MIN <= age <= FLOW_EDGE_MAX:
                    edge = (dt, tj, age)
                    break                      # الأحدث ضمن المدى
            wtot = act.get("total") or 0.0
            if edge is not None and wtot > 0 and ref1[2] > 0:
                e = _flow_between(cur_tj, edge[1], spot)
                ea = (e.get("active") or {}) if e else {}
                etot = ea.get("total")
                if etot is not None and edge[2] > 0:
                    res["flow_edge_call"] = ea.get("call")
                    res["flow_edge_put"]  = ea.get("put")
                    res["flow_edge_win"]  = round(edge[2], 1)
                    rate_edge = etot / edge[2]
                    rate_win = wtot / ref1[2]
                    if rate_win > 0:
                        res["flow_edge"] = round(rate_edge / rate_win, 2)
        except Exception as ex:
            print("liq edge err:", ex)

        # ── [v2.6] كشف الانطلاق ──
        #  الانطلاق = الميل كان دون FLOW_NEUTRAL وصار ≥ FLOW_ONSET_MIN.
        #  «الساخن» = انطلاق مع تسارع ≥ FLOW_ONSET_ACCEL — وهو وحده ما
        #  أظهر حافة في محاكاة 18 سبتمبر (69% عند 2.0 · 64% عند 1.5 ·
        #  خط أساس 48%). الانطلاق وحده = 47–50%، أي صفر.
        #  ⚠ تسجيل بحت. لا يمنع صفقة ولا يفتحها.
        try:
            cur_b = res["flow_bias_active"]
            if cur_b is not None:
                pb, page = _prev_flow(row.get("underlying") or LIQ_UND,
                                      now_ny, db_query=db_query)
                res["flow_prev_bias"] = pb
                res["flow_prev_age"] = page
                # فجوة كبيرة ⇒ لا حكم (فتح جلسة أو انقطاع cron)
                if pb is not None and page is not None and page <= FLOW_PREV_MAX:
                    if abs(pb) < FLOW_NEUTRAL and abs(cur_b) >= FLOW_ONSET_MIN:
                        res["flow_onset"] = 1
                        res["flow_onset_dir"] = "CALL" if cur_b > 0 else "PUT"
                        acc = res.get("flow_accel")
                        res["flow_onset_hot"] = (
                            1 if (acc is not None and acc >= FLOW_ONSET_ACCEL)
                            else 0)
        except Exception as ex:
            print("liq onset err:", ex)

        # ── الموافقة مع اتجاه الإشارة ──
        b = res["flow_bias_active"]
        sd = str(side or "").upper()
        if b is not None and sd in ("CALL", "PUT"):
            if abs(b) < FLOW_NEUTRAL:
                res["flow_align"] = "NEUTRAL"
            elif (b > 0 and sd == "CALL") or (b < 0 and sd == "PUT"):
                res["flow_align"] = "AGREE"
            else:
                res["flow_align"] = "DISAGREE"
        return res
    except Exception as e:
        print("liq compute_flow err:", e)
        return empty


# ═══════════════════════════════════════════════════════════════════════════
#  الحفظ والعرض
# ═══════════════════════════════════════════════════════════════════════════

def save(row, sig_key, tag, bot_und=None, bot_side=None, bot_strike=None,
         reject_reason=None, db_execute=None, flow=None, agg=None,
         verdict=None):
    """يحفظ اللقطة في liq_snaps. يفشل بصمت ولا يعطّل شيئاً."""
    ex = db_execute or _H["db_execute"]
    if ex is None or not isinstance(row, dict):
        return False
    f = flow or {}
    g = agg or {}
    vd = verdict or {}
    try:
        tj = row.get("table_json")
        vals = (
            sig_key, tag, row.get("ts_ny"),
            bot_und, bot_side, _num(bot_strike), reject_reason,
            row.get("underlying"), row.get("expiration"), row.get("session"),
            _num(row.get("spot")), _num(row.get("spot_other")),
            _num(row.get("px_ratio")), _num(row.get("chg_pct")),
            _num(row.get("vix")), _num(row.get("vix1d")),
            _num(row.get("oi_up_strike")), _num(row.get("oi_up_oi")),
            _num(row.get("oi_up_dist")), _yn(row.get("oi_up_in_target")),
            _num(row.get("oi_dn_strike")), _num(row.get("oi_dn_oi")),
            _num(row.get("oi_dn_dist")), _yn(row.get("oi_dn_in_target")),
            _num(row.get("wall_span")), _num(row.get("vol_above")),
            _num(row.get("vol_below")), _num(row.get("ratio_up_dn")),
            _num(row.get("call_vol_total")), _num(row.get("put_vol_total")),
            _num(row.get("pc_ratio")),
            _num(row.get("atm_strike")), _num(row.get("atm_cp_ratio")),
            _yn(row.get("atm_cp_weak")),
            # [v2.0] التدفّق
            f.get("flow_window_min"), f.get("flow_call_15m"),
            f.get("flow_put_15m"), f.get("flow_bias_near"),
            f.get("flow_bias_active"), f.get("flow_bias_wide"),
            f.get("flow_accel"), f.get("flow_edge"),
            # [v2.3] الأرقام الخام للنافذة القصيرة
            f.get("flow_edge_call"), f.get("flow_edge_put"),
            f.get("flow_edge_win"),
            f.get("flow_align"), f.get("flow_ref_ny"),
            # [v2.6] الانطلاق
            f.get("flow_prev_bias"), f.get("flow_prev_age"),
            f.get("flow_onset"), f.get("flow_onset_dir"),
            f.get("flow_onset_hot"),
            # [v2.4] التموضع — من الرد لا من flow
            _num(row.get("gex")), _num(row.get("vex")),
            _num(row.get("chex")), _num(row.get("flip")),
            _num(row.get("flip_dist")), _num(row.get("call_wall")),
            _num(row.get("put_wall")), _num(row.get("atm_iv")),
            _num(row.get("hours_left")),
            # [v2.7] المسيطر — من الجامع لا من الرد
            g.get("cb"), g.get("cs"), g.get("pb"), g.get("ps"),
            g.get("u"), g.get("cov_sec"),
            g.get("buy_pct"), g.get("bull_pct"),
            # [v2.7] قراءة اللحظة — من /snap
            _num(row.get("vwap_spy")), _num(row.get("vwap_dist_spy")),
            _num(row.get("vwap_dist_und")), _yn(row.get("vwap_call_ok")),
            _yn(row.get("vwap_put_ok")),
            _num(row.get("em_pts")), _num(row.get("em_hi")),
            _num(row.get("em_lo")), row.get("em_src"),
            # [v2.8] القرار ونطاق اليوم
            vd.get("v"), vd.get("regime"), _num(vd.get("tgt")),
            _num(vd.get("inv")), _num(vd.get("rr")),
            _num(row.get("day_high")), _num(row.get("day_low")),
            _num(row.get("day_range")),
            json.dumps(tj, separators=(",", ":")) if tj is not None else None,
            "YES" if row.get("ok") else "NO",
            str(row.get("err"))[:300] if row.get("err") else None,
        ) + (None,) * (len(DEC_COLS) + len(LB_COLS))   # [v2.9 · v3.0.1] أعمدة القرار والبوت فارغة في اللقطات
        ex("INSERT INTO liq_snaps(" + ",".join(LIQ_COLS[1:]) + ") VALUES(" +
           ",".join(["?"] * (len(LIQ_COLS) - 1)) + ")", vals)
        return True
    except Exception as e:
        print("liq save err:", e)
        return False


def _fmt_k(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "—"
    return f"{v/1000:.0f}k" if abs(v) >= 1000 else f"{v:.0f}"


def flow_line(flow, side=None):
    """[v2.0] سطر التدفّق لرسالة تيليجرام. يرجع "" إن لم تتوفر بيانات.

       ⚠ وصف لا حكم. لا يدخل أي قرار.
       ⚠ [v2.3] الأرقام الخام للنافذة القصيرة لا تظهر هنا عمداً —
         تُقرأ من /liq.csv عند التحليل حتى لا تطول الرسالة."""
    if not flow or flow.get("flow_bias_active") is None:
        return ""
    b = flow["flow_bias_active"]
    c = flow.get("flow_call_15m") or 0
    p = flow.get("flow_put_15m") or 0
    w = flow.get("flow_window_min")
    dom = abs(b) * 100.0
    if abs(b) < FLOW_NEUTRAL:
        tag = "متوازن"
    else:
        tag = ("نشاط CALL" if b > 0 else "نشاط PUT") + f" {dom:.0f}%"
    acc = flow.get("flow_accel")
    burst = "⚡ " if (acc is not None and acc >= 2.0 and abs(b) >= 0.30) else ""
    al = flow.get("flow_align")
    al_txt = {"AGREE": " ✅ يوافق الإشارة", "DISAGREE": " ⚠️ يخالف الإشارة",
              "NEUTRAL": ""}.get(al, "")
    line = (f"تدفّق {w:.0f}د: كول {_fmt_k(c)} · بوت {_fmt_k(p)} ⇒ "
            f"{burst}{tag}{al_txt}")
    eg = flow.get("flow_edge")
    extra = []
    if acc is not None:
        extra.append(f"تسارع {acc:.1f}×")
    if eg is not None:
        if eg >= FLOW_EDGE_HOT:
            extra.append(f"⚡ يحدث الآن ({eg:.1f}×)")
        elif eg <= 0.5:
            extra.append(f"⏳ حدث في أول النافذة ({eg:.1f}×)")
        else:
            extra.append(f"موزّع ({eg:.1f}×)")
    # [v2.6] وسم الانطلاق — عرض فقط، لا يدخل أي قرار
    if flow.get("flow_onset"):
        d = flow.get("flow_onset_dir") or "?"
        extra.append("🚀 انطلاق " + d + (" (ساخن)" if flow.get("flow_onset_hot")
                                          else ""))
    if extra:
        line += "\n   " + " · ".join(extra)
    return line


def agg_line(agg):
    """[v2.7] سطر المسيطر لرسالة الإشارة. "" إن لم يكتمل. وصف لا حكم."""
    try:
        # أقل من دقيقة تغطية = عيّنة لا تمثّل «آخر 5 دقائق»
        if not agg or not agg.get("ready") or (agg.get("cov_sec") or 0) < 60:
            return ""
        bu = agg.get("bull_pct") or 0
        d = ("صعودي" if bu >= 55 else "هبوطي" if bu <= 45 else "متوازن")
        return (f"المسيطر 5د: مشترون {agg.get('buy_pct', 0):.0f}% · "
                f"{agg.get('lead', '?')} يقودون · {d} "
                f"{max(bu, 100 - bu):.0f}% (مغطّى "
                f"{agg.get('cov_sec', 0) / 60:.1f}د · غير مختبَر)")
    except Exception:
        return ""


def lines(row, compact=True, flow=None, side=None, agg=None):
    """كتلة نصية قصيرة لرسالة تيليجرام. ترجع "" عند أي فشل.

       ⚠ ما تقوله: أين تتركّز المراكز القائمة (OI)، وأين تُتداول العقود
         الآن (التدفّق). لا تقول اتجاهاً — الحجم لا يميّز الشراء من البيع."""
    try:
        if not isinstance(row, dict) or not row.get("ok"):
            return ""
        und = row.get("underlying", "SPX")
        spot = _num(row.get("spot"))
        L = []
        head = f"📊 {und} {spot:.2f}" if spot else f"📊 {und}"
        vx = []
        if row.get("vix"):
            vx.append(f"VIX {row['vix']}")
        if row.get("vix1d"):
            vx.append(f"0D {row['vix1d']}")
        if vx:
            head += " · " + " · ".join(vx)
        L.append(head)

        for pre, sk, oi, ds, tg in (
                ("▲", "oi_up_strike", "oi_up_oi", "oi_up_dist", "oi_up_in_target"),
                ("▼", "oi_dn_strike", "oi_dn_oi", "oi_dn_dist", "oi_dn_in_target")):
            s = _num(row.get(sk))
            if s is None:
                continue
            o = _num(row.get(oi)) or 0
            d = _num(row.get(ds)) or 0
            ov = f"{o/1000:.1f}k" if o >= 1000 else f"{o:.0f}"
            mark = " ⚠ في مسار الهدف" if row.get(tg) else ""
            L.append(f"{pre} {s:.0f} · OI {ov} · {d:+.2f}{mark}")

        # [v2.0] التدفّق الحيّ يسبق التراكمي — هو الأحدث معلومةً
        fl = flow_line(flow, side)
        if fl:
            L.append(fl)
        al = agg_line(agg)                               # [v2.7]
        if al:
            L.append(al)

        va, vb = _num(row.get("vol_above")), _num(row.get("vol_below"))
        if va is not None and vb is not None:
            L.append(f"تراكمي: فوق {va/1000:.0f}k · تحت {vb/1000:.0f}k"
                     + (f" · ب/ك {row['pc_ratio']}" if row.get("pc_ratio") else ""))
        if not compact and row.get("atm_strike"):
            w = " (ضعيف)" if row.get("atm_cp_weak") else ""
            L.append(f"ATM {_num(row['atm_strike']):.0f} · "
                     f"كول/بوت {row.get('atm_cp_ratio')}{w}")
        return "\n".join(L)
    except Exception as e:
        print("liq lines err:", e)
        return ""


def capture(ny_dt, side, tag, bot_und=None, bot_strike=None,
            reject_reason=None, db_execute=None, db_query=None,
            return_flow=False):
    """الدالة الوحيدة التي يستدعيها server.py.

       تجلب اللقطة، تحسب التدفّق، تحفظ، وترجع (نص_تيليجرام, sig_key).
       لا ترمي أبداً — عند أي فشل ترجع ("", sig_key).

       ترتيب مقصود: الحساب **قبل** الحفظ، وإلا صارت اللقطة مرجعاً لنفسها."""
    sig_key = ""
    try:
        sig_key = make_key(ny_dt, side, bot_strike)
        if not LIQ_ENABLED:
            return ("", sig_key, None) if return_flow else ("", sig_key)
        row = fetch(sig_key, tag)
        try:
            flow = compute_flow(row, side=side, db_query=db_query)
        except Exception as e:
            print("liq flow err:", e)
            flow = None
        try:
            agg = agg_window()                            # [v2.7]
        except Exception as e:
            print("liq agg err:", e)
            agg = None
        try:
            vd = decide(row, (agg or {}).get("bull_pct"))      # [v2.8]
        except Exception as e:
            print("liq verdict err:", e)
            vd = None
        save(row, sig_key, tag, bot_und=bot_und, bot_side=side,
             bot_strike=bot_strike, reject_reason=reject_reason,
             db_execute=db_execute, flow=flow, agg=agg, verdict=vd)
        # الوسم cron لا يُنتج نصاً — يُستدعى عشرات المرات يومياً
        txt = "" if str(tag) == "cron" else lines(row, flow=flow, side=side,
                                                  agg=agg)
        return (txt, sig_key, flow) if return_flow else (txt, sig_key)
    except Exception as e:
        print("liq capture err:", e)
        return ("", sig_key, None) if return_flow else ("", sig_key)


# ═══════════════════════════════════════════════════════════════════════════
#  [v2.7] المسيطر — جامع خلفي كل AGG_SEC ثوانٍ
# ═══════════════════════════════════════════════════════════════════════════

def decide(row, bull):
    """[v2.8] قرار اللوحة — نقل حرفي لمنطق index v2.1.x (بلا تخلّف ولا تأكيد).

       يرجع {v, regime, tgt, inv, rr} — و v = "انتظر" عند أي نقص."""
    out = {"v": "انتظر", "regime": None, "tgt": None, "inv": None, "rr": None}
    try:
        sp = _num(row.get("spot"))
        ext = _num(row.get("vwap_dist_spy"))
        if sp is None or ext is None:
            return out
        flip = _num(row.get("flip"))
        cw, pw = _num(row.get("call_wall")), _num(row.get("put_wall"))
        em_hi, em_lo = _num(row.get("em_hi")), _num(row.get("em_lo"))
        ratio = _num(row.get("px_ratio")) or 1.0
        vw = sp - ext * (ratio if str(row.get("underlying")) != "SPY" else 1.0)
        near, min_tgt = sp * 0.0007, sp * 0.0004
        flow = 0 if bull is None else (1 if bull >= VD_BULL
                                       else -1 if bull <= VD_BEAR else 0)
        trend = flip is not None and sp < flip
        out["regime"] = "ترند" if trend else "تذبذب"

        def fin(side, strong, tgt, inv):
            if tgt is None or inv is None:
                return out
            rew, risk = abs(tgt - sp), abs(sp - inv)
            out["tgt"], out["inv"] = round(tgt, 2), round(inv, 2)
            out["rr"] = round(rew / risk, 2) if risk > 0 else None
            if rew < min_tgt or rew < risk:
                return out
            out["v"] = ("STRONG " + side) if (strong and rew >= 1.5 * risk) else side
            return out

        if not trend:
            if ext <= -VD_GATE and flow > 0:
                blk = cw is not None and sp < cw < vw
                if blk and (cw - sp) < min_tgt:
                    return out
                at_w = pw is not None and 0 <= sp - pw <= near
                inv = pw if (pw is not None and pw < sp) else em_lo
                return fin("CALL", ext <= -2 * VD_GATE or at_w,
                           cw if blk else vw, inv)
            if ext >= VD_GATE and flow < 0:
                blk = pw is not None and vw < pw < sp
                if blk and (sp - pw) < min_tgt:
                    return out
                at_w = cw is not None and 0 <= cw - sp <= near
                inv = cw if (cw is not None and cw > sp) else em_hi
                return fin("PUT", ext >= 2 * VD_GATE or at_w,
                           pw if blk else vw, inv)
            return out
        d = -1 if ext < 0 else 1
        if flow == 0 or flow != d:
            return out
        strong = (bull <= 40 if d < 0 else bull >= 60) and abs(ext) <= 2 * VD_GATE
        nx = ((pw if (pw is not None and pw < sp) else em_lo) if d < 0
              else (cw if (cw is not None and cw > sp) else em_hi))
        return fin("PUT" if d < 0 else "CALL", strong, nx, vw)
    except Exception as e:
        print("liq decide err:", e)
        return out


def _series_restore(db_query=None):
    """[v2.8] يعيد بناء سلسلة اليوم من liq_snaps بعد إعادة تشغيل Render.

       دقّة 3 دقائق (وتيرة الـcron) — أخشن من الحيّة لكنها تملأ الفراغ."""
    q = db_query or _H["db_query"]
    if q is None:
        return 0
    try:
        day = datetime.now().strftime("%Y-%m-%d")
        rows = q("SELECT captured_ny, agg_bull_pct FROM liq_snaps "
                 "WHERE liq_und = ? AND captured_ny >= ? "
                 "AND agg_bull_pct IS NOT NULL ORDER BY id", (LIQ_UND, day))
        n = 0
        with _AGG_LOCK:
            for ts, b in rows:
                dt = _parse_ny(ts)
                if dt is None or b is None:
                    continue
                _AGG["series"].setdefault(dt.hour * 60 + dt.minute,
                                          round(float(b), 1))
                n += 1
        return n
    except Exception as e:
        print("liq series restore err:", e)
        return 0


def agg_parse_chain(js, spot, n=None):
    """سلسلة Tradier ⇒ {"c7650": (vol, bid, ask, last), "p…": …} لأقرب n
       سترايك فوق السعر وn تحته. يرجع {} عند أي تعذّر."""
    n = n or AGG_STRIKES
    try:
        node = js.get("options") if isinstance(js, dict) else None
        raw = node.get("option") if isinstance(node, dict) else None
        if raw is None:
            return {}
        if not isinstance(raw, list):
            raw = [raw]
        by = {}
        for o in raw:
            k = _num(o.get("strike"))
            typ = str(o.get("option_type", "")).lower()
            if k is None or typ not in ("call", "put"):
                continue
            by.setdefault(k, {})[typ[0]] = (
                _num(o.get("volume")) or 0.0, _num(o.get("bid")),
                _num(o.get("ask")), _num(o.get("last")))
        if not by or spot is None:
            return {}
        ks = sorted(by)
        ab = [k for k in ks if k > spot][:n]
        be = [k for k in ks if k <= spot][-n:]
        out = {}
        for k in ab + be:
            for t, q in by[k].items():
                out[f"{t}{k:g}"] = q
        return out
    except Exception as e:
        print("liq agg parse err:", e)
        return {}


def agg_classify(prev, cur):
    """الحجم الجديد بين لقطتين موزّعاً على الجهات الأربع (لي-ريدي).

       نفس قاعدة اللوحة حرفياً: العرض والطلب من اللقطة السابقة (السعر
       قبل الصفقة) وإلا الحالية · آخر صفقة من الحالية."""
    e = {"cb": 0.0, "cs": 0.0, "pb": 0.0, "ps": 0.0, "u": 0.0}
    for k, c in cur.items():
        p = prev.get(k)
        if not p:
            continue
        dv = (c[0] or 0.0) - (p[0] or 0.0)
        if dv <= 0:
            continue
        b, a = p[1], p[2]
        if not (a is not None and b is not None and a > b >= 0):
            b, a = c[1], c[2]
        last = c[3]
        if not (a is not None and b is not None and a > b >= 0) or last is None:
            e["u"] += dv
            continue
        x = (last - b) / (a - b)
        sd = k[0]
        if x >= AGG_BUY:
            e[sd + "b"] += dv
        elif x <= AGG_SELL:
            e[sd + "s"] += dv
        else:
            e["u"] += dv
    return e


def agg_window(now=None, sec=AGG_WIN_SEC):
    """نافذة آخر sec ثانية. يرجع الأرقام الخام والنسب وready."""
    now = now or time.time()
    with _AGG_LOCK:
        evs = [x for x in _AGG["ev"] if now - x["t"] <= sec]
    r = {"cb": 0.0, "cs": 0.0, "pb": 0.0, "ps": 0.0, "u": 0.0}
    cov = 0.0
    for x in evs:
        for k in r:
            r[k] += x[k]
        cov += x["dt"]
    cls = r["cb"] + r["cs"] + r["pb"] + r["ps"]
    out = {k: round(v) for k, v in r.items()}
    with _AGG_LOCK:
        series = sorted(_AGG["series"].items())
    out = dict(out)
    out["series"] = [[k, v] for k, v in series]
    out["series_day"] = _AGG["series_day"]
    try:
        out.update(dec_public())                          # [v2.9]
    except Exception as e:
        print("liq dec public err:", e)
    try:
        out.update(lb_public())                           # [v3.0]
    except Exception as e:
        print("liq lb public err:", e)
    out.update({"cov_sec": round(min(cov, sec), 1), "events": len(evs),
                "cls": round(cls), "ready": cls >= AGG_MIN_CLS,
                "buy_pct": None, "bull_pct": None, "lead": None,
                "underlying": LIQ_UND})
    if cls >= AGG_MIN_CLS:
        out["buy_pct"] = round((r["cb"] + r["pb"]) / cls * 100, 1)
        out["bull_pct"] = round((r["cb"] + r["ps"]) / cls * 100, 1)
        names = {"cb": "مشترو CALL", "pb": "مشترو PUT",
                 "ps": "بائعو PUT", "cs": "بائعو CALL"}
        out["lead"] = names[max(("cb", "pb", "ps", "cs"), key=lambda k: r[k])]
    return out


def _agg_in_session(ny):
    if ny.weekday() >= 5:
        return False
    hm = ny.hour * 60 + ny.minute
    return 9 * 60 + 30 <= hm < 16 * 60


def agg_tick(td_get, ny, now=None):
    """دورة جمع واحدة. ترجع وصفاً نصياً — لا ترمي أبداً."""
    now = now or time.time()
    if not _agg_in_session(ny):
        with _AGG_LOCK:
            _AGG["prev"] = None          # لا حمل بين الجلسات
        return "closed"
    exp = ny.strftime("%Y-%m-%d")
    # السعر كل 30 ثانية — يكفي لاختيار نافذة السترايكات
    # [v2.9] كل 10 ثوانٍ حين يعمل قرار الخادم (لمس الهدف والإبطال أدق)
    if _AGG["spot"] is None or now - _AGG["spot_t"] > (DEC_SPOT_SEC if DEC_ENABLED else 30):
        js, err = td_get("/markets/quotes", {"symbols": LIQ_UND,
                                             "greeks": "false"})
        if not err and isinstance(js, dict):
            q = (js.get("quotes") or {}).get("quote")
            q = q[0] if isinstance(q, list) and q else q
            v = _num((q or {}).get("last")) if isinstance(q, dict) else None
            if v:
                _AGG["spot"], _AGG["spot_t"] = v, now
    js, err = td_get("/markets/options/chains",
                     {"symbol": LIQ_UND, "expiration": exp,
                      "greeks": "false"})
    if err:
        _AGG["errs"] += 1
        _AGG["last_err"] = str(err)[:160]
        return "err"
    cur = agg_parse_chain(js, _AGG["spot"])
    del js                                  # السلسلة كاملة لا تبقى في الذاكرة
    if not cur:
        return "empty"
    with _AGG_LOCK:
        P, pt = _AGG["prev"], _AGG["prev_t"]
        if P is not None and _AGG["exp"] == exp and 0 < now - pt <= AGG_GAP_SEC:
            e = agg_classify(P, cur)
            e["t"], e["dt"] = now, now - pt
            _AGG["ev"].append(e)
        _AGG["prev"], _AGG["prev_t"], _AGG["exp"] = cur, now, exp
        _AGG["ticks"] += 1
        _AGG["last_ok"] = ny.strftime("%H:%M:%S")
    # [v2.8] نقطة السلسلة لهذه الدقيقة — من نافذة الخمس دقائق نفسها
    try:
        day = ny.strftime("%Y-%m-%d")
        w = agg_window(now=now)
        with _AGG_LOCK:
            if _AGG["series_day"] != day:
                _AGG["series"] = {}
                _AGG["series_day"] = day
                _AGG["series_restored"] = False
            if w.get("bull_pct") is not None:
                _AGG["series"][ny.hour * 60 + ny.minute] = w["bull_pct"]
                if len(_AGG["series"]) > AGG_SERIES_MAX:
                    for k in sorted(_AGG["series"])[:-AGG_SERIES_MAX]:
                        _AGG["series"].pop(k, None)
    except Exception as e:
        print("liq series err:", e)
    return "ok"


def _agg_loop(td_get, ny_now):
    while True:
        if not _AGG["series_restored"] and _H["db_query"] is not None:
            try:
                _AGG["series_day"] = datetime.now().strftime("%Y-%m-%d")
                _series_restore()
            except Exception as e:
                print("liq restore err:", e)
            _AGG["series_restored"] = True
        t0 = time.time()
        try:
            ny = ny_now()
            st = agg_tick(td_get, ny)
            if st == "ok":
                dec_tick(td_get, ny)                     # [v2.9] (موقوف ما لم DEC_LEGACY=1)
                lb_tick(td_get, ny)                      # [v3.0] بوت السيولة
        except Exception as e:
            st = "err"
            _AGG["errs"] += 1
            _AGG["last_err"] = f"{type(e).__name__}: {e}"[:160]
        wait = AGG_SEC if st != "closed" else 30.0
        time.sleep(max(1.0, wait - (time.time() - t0)))


def agg_start(td_get, ny_now):
    """يشغّل الجامع مرة واحدة. td_get = _td_get من server (العميل المشترك)."""
    if not AGG_ENABLED or td_get is None or ny_now is None:
        return False
    if _AGG["thread"] is not None and _AGG["thread"].is_alive():
        return True
    td_get = counted(td_get)                              # [v3.0] عدّ النداءات
    th = threading.Thread(target=_agg_loop, args=(td_get, ny_now),
                          daemon=True, name="liq-agg")
    _AGG["thread"] = th
    th.start()
    dec_start(ny_now)                                     # [v2.9]
    return True


# ═══════════════════════════════════════════════════════════════════════════
#  [v2.9] قرار اللوحة من الخادم — يعمل والمتصفح مغلق
# ═══════════════════════════════════════════════════════════════════════════
#  نقل حرفي لمنطق index v2.3.1 (decide + تخلّف الضغط + تأكيد 60/20 ثانية +
#  سجلّ القرارات النشطة) إلى خيط الجامع نفسه كل 5 ثوانٍ. المدخلات:
#    • السعر وسلسلة العقود والضغط ← الجامع (Tradier مباشرة، كل 5 ثوانٍ)
#    • VWAP والانقلاب والجداران وحدّا اليوم ← /json من اللوحة كل 20 ثانية
#      في خيط مستقل (لا يعطّل الجامع). بين التحديثين يُعاد حساب بُعد VWAP
#      من السعر الحيّ: dist_spy = (spot − vwap_und) ÷ ratio.
#  كل قرار مؤكَّد يُحفظ صفاً في liq_snaps (tag = dash_dec) لحظة ولادته ويُحدَّث
#  كل دقيقة وعند نهاية ساعته ⇒ لا يضيع بإغلاق المتصفح ولا بإعادة تشغيل Render.
#  عند النهاية وعند الاستعادة تُجلب شموع الدقيقة من Tradier (timesales) للعقد
#  وللأداة ⇒ الأعلى والأدنى ولمس الهدف والإبطال مكتملة حتى لو فات شيء.
#  ⚠⚠ صفر قرارات على البوت. تسجيل وعرض فقط.
DEC_ENABLED   = os.getenv("DEC_ENABLED", "1") == "1"
DEC_LEGACY    = os.getenv("DEC_LEGACY", "0") == "1"      # [v3.0] قرار v2.9 القديم — موقوف افتراضياً
DEC_IN_SEC    = float(os.getenv("DEC_IN_SEC", "20"))     # تحديث مدخلات /json
DEC_IN_TIMEOUT = float(os.getenv("DEC_IN_TIMEOUT", "8"))
DEC_CONFIRM   = 60.0                                     # تأكيد الدخول (ث)
DEC_BACK      = 20.0                                     # التراجع إلى «انتظر»
DEC_WIN_MIN   = 60                                       # عمر القرار (د)
DEC_MAX_ASK   = float(os.getenv("DEC_MAX_ASK", "4.5"))   # سقف سعر العقد المرشّح
DEC_SAVE_SEC  = 60.0                                     # تحديث الصف في القاعدة
DEC_SPOT_SEC  = 10.0                                     # السعر كل 10 ثوانٍ بدل 30
DEC_WAIT = "انتظر"
_DEC = {"day": None, "n": 0, "list": [], "in": None, "in_t": 0.0,
        "in_err": None, "in_ok": None, "f": 0, "cur": None, "cand": None,
        "since": 0.0, "raw": None, "restored_day": None, "errs": 0,
        "last_err": None, "thread": None, "ticks": 0}
_DEC_LOCK = threading.RLock()


def _hm(mn):
    return f"{int(mn) // 60:02d}:{int(mn) % 60:02d}"


def _hm_mn(hm):
    try:
        h, m = str(hm).split(":")[:2]
        return int(h) * 60 + int(m)
    except Exception:
        return None


def _ksa_hm(ny):
    """وقت السعودية لنفس اللحظة — من المنطقة الزمنية لا بفارق ثابت (التوقيت الصيفي)."""
    try:
        from zoneinfo import ZoneInfo
        return ny.astimezone(ZoneInfo("Asia/Riyadh")).strftime("%H:%M")
    except Exception:
        return _hm((ny.hour * 60 + ny.minute + 7 * 60) % 1440)


def dec_decide(sp, w, pos, em, bull, fstate=None):
    """قرار اللوحة — نقل حرفي لـdecide() في index v2.3.1.

       w = {gate, dist_spy, vwap_und} · pos = {flip, call_wall, put_wall} ·
       em = {lo, hi}. يرجع v · why · side · tgtP · invP · tgtN · invN · rr."""
    def R(v, why):
        return {"v": v, "why": why, "side": None, "tgtP": None, "invP": None,
                "tgtN": "", "invN": "", "rr": None}
    if not w or sp is None or w.get("dist_spy") is None or w.get("vwap_und") is None:
        return R(DEC_WAIT, "بانتظار VWAP")
    pos, em = pos or {}, em or {}
    g, ext, vw = float(w.get("gate") or VD_GATE), float(w["dist_spy"]), float(w["vwap_und"])
    flip, cw, pw = _num(pos.get("flip")), _num(pos.get("call_wall")), _num(pos.get("put_wall"))
    elo, ehi = _num(em.get("lo")), _num(em.get("hi"))
    near, min_t = sp * 0.0007, sp * 0.0004
    if fstate is not None:
        flow = fstate
    else:
        flow = 0 if bull is None else (1 if bull >= VD_BULL else -1 if bull <= VD_BEAR else 0)
    if bull is None:
        f_txt = "الضغط لم يكتمل"
    elif flow > 0:
        f_txt = f"الضغط صعودي {round(bull)}%"
    elif flow < 0:
        f_txt = f"الضغط هبوطي {round(100 - bull)}%"
    else:
        f_txt = "الضغط متوازن"
    trend = flip is not None and sp < flip
    ext_s = f"${abs(ext):.2f}"

    def fin(side, strong, why, tgt, tgt_n, inv, inv_n):
        if tgt is None or inv is None:
            return R(DEC_WAIT, why + " · لا هدف أو إبطال محدَّد")
        rew, risk = abs(tgt - sp), abs(sp - inv)
        if rew < min_t:
            o = R(DEC_WAIT, why + " · الهدف قريب جداً")
            o["rr"] = round(rew / risk, 2) if risk > 0 else None
            return o
        if rew < risk:
            o = R(DEC_WAIT, why + " · الخطر أكبر من الربح")
            o["rr"] = round(rew / risk, 2) if risk > 0 else None
            return o
        o = R(("STRONG " if (strong and rew >= 1.5 * risk) else "") + side, why)
        o.update({"side": side, "tgtP": float(tgt), "invP": float(inv),
                  "tgtN": tgt_n, "invN": inv_n,
                  "rr": round(rew / risk, 2) if risk > 0 else None})
        return o

    if not trend:
        rg = "تذبذب" + (f" (فوق الانقلاب {round(flip)})" if flip is not None else "") \
             + " — يميل للارتداد نحو VWAP"
        if ext <= -g:
            if flow <= 0:
                return R(DEC_WAIT, f"{rg} · تحت VWAP بـ{ext_s} لكن {f_txt} — انتظر تحوّله صعودياً")
            at_w = pw is not None and 0 <= sp - pw <= near
            inv = pw if (pw is not None and pw < sp) else elo
            blk = cw is not None and sp < cw < vw
            if blk and cw - sp < min_t:
                return R(DEC_WAIT, f"{rg} · تحت VWAP بـ{ext_s} · {f_txt} · لكن جدار CALL فوقك مباشرة")
            return fin("CALL", ext <= -2 * g or at_w,
                       f"{rg} · تحت VWAP بـ{ext_s} · {f_txt}" + (" · عند جدار PUT" if at_w else ""),
                       cw if blk else vw, "جدار CALL" if blk else "VWAP", inv,
                       "كسر جدار PUT" if (pw is not None and pw < sp) else "كسر حدّ اليوم")
        if ext >= g:
            if flow >= 0:
                return R(DEC_WAIT, f"{rg} · فوق VWAP بـ{ext_s} لكن {f_txt} — انتظر تحوّله هبوطياً")
            at_w = cw is not None and 0 <= cw - sp <= near
            inv = cw if (cw is not None and cw > sp) else ehi
            blk = pw is not None and vw < pw < sp
            if blk and sp - pw < min_t:
                return R(DEC_WAIT, f"{rg} · فوق VWAP بـ{ext_s} · {f_txt} · لكن جدار PUT تحتك مباشرة")
            return fin("PUT", ext >= 2 * g or at_w,
                       f"{rg} · فوق VWAP بـ{ext_s} · {f_txt}" + (" · عند جدار CALL" if at_w else ""),
                       pw if blk else vw, "جدار PUT" if blk else "VWAP", inv,
                       "اختراق جدار CALL" if (cw is not None and cw > sp) else "اختراق حدّ اليوم")
        return R(DEC_WAIT, f"{rg} · قريب من VWAP — لا ميزة، انتظر ابتعاده")
    rt = f"ترند (تحت الانقلاب {round(flip)}) — الحركة تميل للامتداد"
    d = -1 if ext < 0 else 1
    if flow == 0 or flow != d:
        return R(DEC_WAIT, f"{rt} · {'تحت' if d < 0 else 'فوق'} VWAP لكن {f_txt} — لا تأكيد")
    st = bull is not None and (bull <= 40 if d < 0 else bull >= 60) and abs(ext) <= 2 * g
    if d < 0:
        nx = pw if (pw is not None and pw < sp) else elo
        nx_n = "جدار PUT" if (pw is not None and pw < sp) else "حدّ اليوم"
    else:
        nx = cw if (cw is not None and cw > sp) else ehi
        nx_n = "جدار CALL" if (cw is not None and cw > sp) else "حدّ اليوم"
    return fin("PUT" if d < 0 else "CALL", st,
               f"{rt} · {'تحت' if d < 0 else 'فوق'} VWAP · {f_txt}",
               nx, nx_n, vw, "عودة فوق VWAP" if d < 0 else "عودة تحت VWAP")


def dec_flow_hyst(bull):
    """تخلّف الضغط — نقل حرفي لـflowHyst (v2.3.1: null لا يمسح الحالة)."""
    if bull is None:
        return 0
    f = _DEC["f"]
    if f == 1:
        if bull < 50:
            f = -1 if bull <= VD_BEAR else 0
    elif f == -1:
        if bull > 50:
            f = 1 if bull >= VD_BULL else 0
    else:
        f = 1 if bull >= VD_BULL else -1 if bull <= VD_BEAR else 0
    _DEC["f"] = f
    return f


def dec_stable(raw, now):
    """ثبات القرار — دخول بعد 60 ثانية متصلة · تراجع بعد 20.

       ⚠ عند الإقلاع الحالة «انتظر» (لا قرار يولد بلا تأكيد بعد إعادة تشغيل)."""
    if _DEC["cur"] is None:
        _DEC["cur"] = {"v": DEC_WAIT, "side": None}
    cur = _DEC["cur"]
    if raw["v"] == cur["v"]:
        _DEC["cur"], _DEC["cand"] = raw, None
        return raw, None
    cand = _DEC["cand"]
    if cand is None or cand["v"] != raw["v"]:
        _DEC["cand"], _DEC["since"] = raw, now
    else:
        _DEC["cand"] = raw
    need = DEC_BACK if raw["v"] == DEC_WAIT else DEC_CONFIRM
    if now - _DEC["since"] >= need:
        _DEC["cur"], _DEC["cand"] = raw, None
        return raw, None
    return cur, {"v": raw["v"], "left": int(need - (now - _DEC["since"]) + 0.999)}


def _occ(exp, side, k):
    """رمز OCC: SPXW للمؤشر اليومي · SPY كما هو."""
    root = "SPXW" if LIQ_UND == "SPX" else LIQ_UND
    try:
        yymmdd = exp[2:4] + exp[5:7] + exp[8:10]
        return f"{root}{yymmdd}{'C' if side == 'CALL' else 'P'}{int(round(float(k) * 1000)):08d}"
    except Exception:
        return None


def dec_pick(chain, side, sp):
    """العقد المرشّح — الأعلى تداولاً في الاتجاه وسعره ≤ DEC_MAX_ASK · التعادل ⇒ الأقرب."""
    if not chain or side not in ("CALL", "PUT") or sp is None:
        return None
    t = "c" if side == "CALL" else "p"
    best = None
    for key, q in chain.items():
        if not key.startswith(t):
            continue
        try:
            k = float(key[1:])
        except ValueError:
            continue
        vol, _bid, ask = (q[0] or 0.0), q[1], q[2]
        if ask is None or not (ask > 0) or ask > DEC_MAX_ASK:
            continue
        if (best is None or vol > best["v"]
                or (vol == best["v"] and abs(k - sp) < abs(best["k"] - sp))):
            best = {"k": k, "ask": float(ask), "v": float(vol)}
    return best


def dec_mid(chain, side, k):
    q = (chain or {}).get(f"{'c' if side == 'CALL' else 'p'}{float(k):g}")
    if not q:
        return None
    b, a = q[1], q[2]
    if a is not None and a > 0 and b is not None and b > 0:
        return round((a + b) / 2.0, 4)
    if a is not None and a > 0:
        return round(float(a), 4)
    return None


def dec_update(ny, sp, chain, conf, now):
    """سجلّ القرارات النشطة — نقل لـlsUpdate. يرجع قائمة ما تغيّر ويحتاج حفظاً."""
    mn = ny.hour * 60 + ny.minute
    hm = _hm(mn)
    changed = []
    for x in _DEC["list"]:
        if x["done"]:
            continue
        if mn - x["mn"] >= DEC_WIN_MIN:
            x["done"] = True
            changed.append(x)
            continue
        d = -1 if x["side"] == "PUT" else 1
        mv = d * (sp - x["sp"])
        x["spNow"] = sp
        x["mfe"] = max(x.get("mfe") or 0.0, mv)
        x["mae"] = min(x.get("mae") or 0.0, mv)
        if not x.get("tgtT") and d * (sp - x["tgt"]) >= 0:
            x["tgtT"] = hm
            changed.append(x)
        if not x.get("invT") and d * (sp - x["inv"]) <= 0:
            x["invT"] = hm
            changed.append(x)
        if x.get("ck") is not None:
            m = dec_mid(chain, x["side"], x["ck"])
            if m is not None:
                x["cNow"] = m
                if x.get("c0") is None:
                    x["c0"] = m
                if x.get("cHi") is None or m > x["cHi"]:
                    x["cHi"], x["cHiT"] = m, hm
                if x.get("cLo") is None or m < x["cLo"]:
                    x["cLo"], x["cLoT"] = m, hm
            else:
                x["cOut"] = True
    o = conf
    if o and o.get("side") and o.get("tgtP") is not None and o.get("invP") is not None:
        if not any((not x["done"]) and x["side"] == o["side"] for x in _DEC["list"]):
            c = dec_pick(chain, o["side"], sp)
            c0 = dec_mid(chain, o["side"], c["k"]) if c else None
            _DEC["n"] += 1
            x = {"id": _DEC["n"], "v": o["v"], "side": o["side"], "t": hm,
                 "tk": _ksa_hm(ny), "mn": mn, "sp": sp,
                 "tgt": o["tgtP"], "inv": o["invP"], "tgtN": o.get("tgtN") or "",
                 "invN": o.get("invN") or "", "why": o.get("why") or "",
                 "rr": o.get("rr"),
                 "ck": c["k"] if c else None, "ca": c["ask"] if c else None,
                 "cv": c["v"] if c else None,
                 "csym": _occ(ny.strftime("%Y-%m-%d"), o["side"], c["k"]) if c else None,
                 "c0": c0, "cNow": c0, "cHi": c0, "cLo": c0,
                 "cHiT": hm if c0 is not None else None,
                 "cLoT": hm if c0 is not None else None,
                 "spNow": sp, "mfe": 0.0, "mae": 0.0, "done": False,
                 "tgtT": None, "invT": None, "bN": 0, "src": "server",
                 "bOK": False, "fin": False, "cOut": False, "restored": False,
                 "in": dict(_DEC.get("in_snap") or {}), "_saved": False, "_st": 0.0}
            _DEC["list"].append(x)
            if len(_DEC["list"]) > 40:
                _DEC["list"] = _DEC["list"][-40:]
            changed.append(x)
    return changed


def dec_merge_bars(x, opt_bars, und_bars):
    """دمج شموع الدقيقة — نقل لـlsMerge (الأشد يفوز)."""
    t0, t1 = x["mn"], x["mn"] + DEC_WIN_MIN

    def in_w(b):
        m = _hm_mn(b[0])
        return m is not None and t0 <= m < t1
    nb = 0
    for b in opt_bars or []:
        if not in_w(b):
            continue
        nb += 1
        if x.get("cHi") is None or b[1] > x["cHi"]:
            x["cHi"], x["cHiT"] = b[1], b[0]
        if x.get("cLo") is None or b[2] < x["cLo"]:
            x["cLo"], x["cLoT"] = b[2], b[0]
    x["bN"] = nb
    d = -1 if x["side"] == "PUT" else 1
    for b in und_bars or []:
        if not in_w(b):
            continue
        best, worst = (b[1], b[2]) if d > 0 else (b[2], b[1])
        if d * (best - x["tgt"]) >= 0 and (not x.get("tgtT") or _hm_mn(b[0]) < _hm_mn(x["tgtT"])):
            x["tgtT"] = b[0]
        if d * (worst - x["inv"]) <= 0 and (not x.get("invT") or _hm_mn(b[0]) < _hm_mn(x["invT"])):
            x["invT"] = b[0]
        x["mfe"] = max(x.get("mfe") or 0.0, d * (best - x["sp"]))
        x["mae"] = min(x.get("mae") or 0.0, d * (worst - x["sp"]))
    return nb


def _dec_bars(td_get, sym, ny, start_hm):
    """شموع الدقيقة من Tradier — [[HH:MM, high, low, close], …] أو None."""
    try:
        day = ny.strftime("%Y-%m-%d")
        js, err = td_get("/markets/timesales",
                         {"symbol": sym, "interval": "1min",
                          "start": f"{day} {start_hm}",
                          "end": ny.strftime("%Y-%m-%d %H:%M"),
                          "session_filter": "open"})
        if err or not isinstance(js, dict):
            return None
        ser = js.get("series")
        data = ser.get("data") if isinstance(ser, dict) else None
        if data is None:
            return []
        if not isinstance(data, list):
            data = [data]
        out = []
        for b in data:
            hm = str(b.get("time", ""))[11:16]
            h, l, c = _num(b.get("high")), _num(b.get("low")), _num(b.get("close"))
            if _hm_mn(hm) is not None and h and l:
                out.append([hm, h, l, c])
        return out
    except Exception as e:
        print("liq dec bars err:", e)
        return None


def dec_backfill(td_get, x, ny):
    ob = _dec_bars(td_get, x["csym"], ny, x["t"]) if x.get("csym") else []
    ub = _dec_bars(td_get, LIQ_UND, ny, x["t"])
    if ob is None and ub is None:
        return False
    dec_merge_bars(x, ob or [], ub or [])
    x["bOK"] = True
    return True


# ── الحفظ في liq_snaps (tag = dash_dec) · DEC_COLS معرَّفة مع LIQ_COLS ──


def _dec_vals(x):
    return {
        "dec_id": x["id"], "dec_side": x["side"], "dec_t": x["t"], "dec_tk": x["tk"],
        "dec_why": (x.get("why") or "")[:300], "dec_tgt_n": x.get("tgtN"),
        "dec_inv_n": x.get("invN"), "dec_csym": x.get("csym"),
        "dec_ck": x.get("ck"), "dec_ca": x.get("ca"), "dec_cv": x.get("cv"),
        "dec_c0": x.get("c0"), "dec_cnow": x.get("cNow"),
        "dec_hi": x.get("cHi"), "dec_hi_t": x.get("cHiT"),
        "dec_lo": x.get("cLo"), "dec_lo_t": x.get("cLoT"),
        "dec_tgt_t": x.get("tgtT"), "dec_inv_t": x.get("invT"),
        "dec_mfe": x.get("mfe"), "dec_mae": x.get("mae"),
        "dec_spnow": x.get("spNow"), "dec_end": "done" if x["done"] else "open",
        "dec_bars": x.get("bN") or 0,
    }


def dec_persist(x, day, now, force=False):
    """صف القرار: INSERT عند الولادة · UPDATE كل دقيقة وعند النهاية."""
    ex = _H["db_execute"]
    if ex is None:
        return False
    if x["_saved"] and not force and now - x.get("_st", 0.0) < DEC_SAVE_SEC:
        return True
    key = f"dash_{day}_{x['id']}"
    dv = _dec_vals(x)
    try:
        if not x["_saved"]:
            inp = x.get("in") or {}
            base = {"sig_key": key, "tag": "dash_dec",
                    "captured_ny": f"{day} {x['t']}:00", "liq_und": LIQ_UND,
                    "expiration": day, "session": "open", "spot": x["sp"],
                    "flip": inp.get("flip"), "call_wall": inp.get("call_wall"),
                    "put_wall": inp.get("put_wall"),
                    "vwap_dist_spy": inp.get("dist_spy"),
                    "em_hi": inp.get("em_hi"), "em_lo": inp.get("em_lo"),
                    "agg_bull_pct": inp.get("bull"),
                    "verdict": x["v"], "verdict_regime": inp.get("regime"),
                    "verdict_tgt": x["tgt"], "verdict_inv": x["inv"],
                    "verdict_rr": x.get("rr"), "ok": "YES"}
            base.update(dv)
            cols = list(base.keys())
            ex("INSERT INTO liq_snaps(" + ",".join(cols) + ") VALUES(" +
               ",".join(["?"] * len(cols)) + ")", tuple(base[c] for c in cols))
            x["_saved"] = True
        else:
            cols = [c for c in DEC_COLS if c != "dec_id"]
            ex("UPDATE liq_snaps SET " + ",".join(f"{c} = ?" for c in cols) +
               " WHERE sig_key = ? AND tag = ?",
               tuple(dv[c] for c in cols) + (key, "dash_dec"))
        x["_st"] = now
        return True
    except Exception as e:
        _DEC["errs"] += 1
        _DEC["last_err"] = f"persist: {type(e).__name__}: {e}"[:160]
        print("liq dec persist err:", e)
        return False


def dec_restore(day, td_get=None, ny=None):
    """بعد إعادة تشغيل Render: قرارات اليوم من القاعدة + سدّ الفجوة بالشموع."""
    q = _H["db_query"]
    if q is None:
        return 0
    try:
        rows = q("SELECT verdict, spot, verdict_tgt, verdict_inv, verdict_rr, " +
                 ",".join(DEC_COLS) + " FROM liq_snaps WHERE tag = ? AND "
                 "sig_key LIKE ? ORDER BY id", ("dash_dec", f"dash_{day}_%"))
    except Exception as e:
        print("liq dec restore err:", e)
        return 0
    lst, n = [], 0
    for r in rows:
        v, sp, tgt, inv, rr = r[:5]
        d = dict(zip(DEC_COLS, r[5:]))
        try:
            i = int(d["dec_id"])
        except Exception:
            continue
        n = max(n, i)
        mn = _hm_mn(d["dec_t"])
        if mn is None or sp is None or tgt is None or inv is None:
            continue
        lst.append({"id": i, "v": v, "side": d["dec_side"], "t": d["dec_t"],
                    "tk": d["dec_tk"], "mn": mn, "sp": float(sp), "tgt": float(tgt),
                    "inv": float(inv), "tgtN": d["dec_tgt_n"] or "",
                    "invN": d["dec_inv_n"] or "", "why": d["dec_why"] or "", "rr": rr,
                    "ck": d["dec_ck"], "ca": d["dec_ca"], "cv": d["dec_cv"],
                    "csym": d["dec_csym"], "c0": d["dec_c0"], "cNow": d["dec_cnow"],
                    "cHi": d["dec_hi"], "cHiT": d["dec_hi_t"], "cLo": d["dec_lo"],
                    "cLoT": d["dec_lo_t"], "tgtT": d["dec_tgt_t"],
                    "invT": d["dec_inv_t"], "mfe": d["dec_mfe"] or 0.0,
                    "mae": d["dec_mae"] or 0.0, "spNow": d["dec_spnow"],
                    "done": d["dec_end"] == "done", "bN": d["dec_bars"] or 0,
                    "src": "server", "restored": True, "in": {},
                    "bOK": False, "fin": d["dec_end"] == "done", "cOut": False,
                    "_saved": True, "_st": 0.0})
    with _DEC_LOCK:
        _DEC["list"], _DEC["n"] = lst[-40:], n
    if td_get is not None and ny is not None:
        for x in lst:
            if not x["done"]:
                dec_backfill(td_get, x, ny)
    return len(lst)


def _dec_inputs_once():
    """مدخلات بطيئة من /json اللوحة: VWAP والانقلاب والجداران وحدّا اليوم."""
    try:
        r = _http().get(f"{LIQ_URL}/json", timeout=DEC_IN_TIMEOUT,
                        params={"u": LIQ_UND, "n": AGG_STRIKES})
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}")
        js = r.json()
        if not isinstance(js, dict) or not js.get("ok"):
            raise RuntimeError(str((js or {}).get("err") or "رد غير متوقع")[:100])
        w, p, em = js.get("vwap") or {}, js.get("pos") or {}, js.get("em") or {}
        spot = _num(js.get("spot"))
        vu, dist = _num(w.get("vwap_und")), _num(w.get("dist_spy"))
        ratio = _num(w.get("ratio"))
        if not ratio and dist and spot and vu is not None:
            ratio = (spot - vu) / dist
        inp = {"t": time.time(), "vwap_und": vu, "ratio": ratio or 1.0,
               "gate": _num(w.get("gate")) or VD_GATE,
               "flip": _num(p.get("flip")), "call_wall": _num(p.get("call_wall")),
               "put_wall": _num(p.get("put_wall")),
               "em_lo": _num(em.get("lo")), "em_hi": _num(em.get("hi")),
               "gex": _num(p.get("gex"))}                     # [v3.0]
        with _DEC_LOCK:
            _DEC["in"], _DEC["in_t"], _DEC["in_err"] = inp, time.time(), None
            _DEC["in_ok"] = datetime.now().strftime("%H:%M:%S")
        return True
    except Exception as e:
        if isinstance(e, getattr(httpx, "TransportError", Exception)):
            _http_reset()
        with _DEC_LOCK:
            _DEC["in_err"] = f"{type(e).__name__}: {e}"[:160]
        return False


def _dec_in_loop(ny_now):
    while True:
        t0 = time.time()
        try:
            if _agg_in_session(ny_now()):
                _dec_inputs_once()
        except Exception as e:
            print("liq dec input err:", e)
        time.sleep(max(2.0, DEC_IN_SEC - (time.time() - t0)))


def dec_tick(td_get, ny, now=None):
    """دورة القرار — بعد agg_tick الناجح. لا ترمي أبداً."""
    if not DEC_ENABLED or not DEC_LEGACY:
        return "off"
    now = now or time.time()
    try:
        day = ny.strftime("%Y-%m-%d")
        if _DEC["day"] != day:
            with _DEC_LOCK:
                _DEC.update({"day": day, "n": 0, "list": [], "cur": None,
                             "cand": None, "since": 0.0, "f": 0})
            if _DEC["restored_day"] != day:
                _DEC["restored_day"] = day
                dec_restore(day, td_get, ny)
        inp = _DEC["in"]
        with _AGG_LOCK:
            chain, sp = _AGG["prev"], _AGG["spot"]
        if sp is None or not chain:
            return "no-data"
        if not inp or now - inp["t"] > 120:          # مدخلات أقدم من دقيقتين ⇒ لا قرار
            raw = {"v": DEC_WAIT, "why": "بانتظار مدخلات اللوحة", "side": None}
            w = None
        else:
            w = {"gate": inp["gate"], "vwap_und": inp["vwap_und"],
                 "dist_spy": ((sp - inp["vwap_und"]) / inp["ratio"])
                 if inp["vwap_und"] is not None and inp["ratio"] else None}
            aw = agg_window(now=now)
            bull = aw["bull_pct"] if aw.get("ready") else None
            fs = dec_flow_hyst(bull)
            raw = dec_decide(sp, w, {"flip": inp["flip"], "call_wall": inp["call_wall"],
                                     "put_wall": inp["put_wall"]},
                             {"lo": inp["em_lo"], "hi": inp["em_hi"]}, bull, fs)
            _DEC["in_snap"] = {"flip": inp["flip"], "call_wall": inp["call_wall"],
                               "put_wall": inp["put_wall"], "dist_spy": w["dist_spy"],
                               "em_hi": inp["em_hi"], "em_lo": inp["em_lo"], "bull": bull,
                               "regime": ("ترند" if inp["flip"] is not None and sp < inp["flip"]
                                          else "تذبذب")}
        with _DEC_LOCK:
            conf, pend = dec_stable(raw, now)
            _DEC["raw"], _DEC["pend"] = raw, pend
            changed = dec_update(ny, sp, chain, conf, now)
            _DEC["ticks"] += 1
            items = list(_DEC["list"])
        for x in items:
            if x["done"] and not x.get("fin"):
                dec_backfill(td_get, x, ny)
                x["fin"] = True
                dec_persist(x, day, now, force=True)
            elif not x["done"]:
                dec_persist(x, day, now, force=(x in changed))
        return "ok"
    except Exception as e:
        _DEC["errs"] += 1
        _DEC["last_err"] = f"{type(e).__name__}: {e}"[:160]
        print("liq dec tick err:", e)
        return "err"


def dec_public():
    """للوحة عبر /liq_agg: القرارات النشطة (≤60 د) + القرار الحالي."""
    with _DEC_LOCK:
        pub = []
        for x in _DEC["list"]:
            if x["done"]:
                continue
            pub.append({k: v for k, v in x.items()
                        if not k.startswith("_") and k not in ("in",)})
        cur = _DEC["cur"] or {}
        return {"dec": pub, "dec_day": _DEC["day"],
                "dec_cur": cur.get("v"), "dec_raw": (_DEC["raw"] or {}).get("v"),
                "dec_why": (_DEC["raw"] or {}).get("why"),
                "dec_pend": _DEC.get("pend"), "dec_on": DEC_ENABLED,
                "dec_in_ok": _DEC["in_ok"], "dec_in_err": _DEC["in_err"]}


def dec_start(ny_now):
    if not DEC_ENABLED or ny_now is None:
        return False
    if _DEC["thread"] is not None and _DEC["thread"].is_alive():
        return True
    th = threading.Thread(target=_dec_in_loop, args=(ny_now,), daemon=True,
                          name="liq-dec-in")
    _DEC["thread"] = th
    th.start()
    return True


# ═══════════════════════════════════════════════════════════════════════════
#  [v3.0] بوت السيولة — مشروع مستقل تماماً عن إشارة TradingView
# ═══════════════════════════════════════════════════════════════════════════
#  يقرّر بنفسه من بيانات اللوحة، ويقيس فقط (لا أوامر إطلاقاً).
#
#  الإشارة (الثلاثة معاً، ثم انتظار 15 د قبل إشارة جديدة في نفس الاتجاه):
#    ① المسيطرون (آخر 5 د): صعودي ≥55% للـCALL · ≤45% للـPUT — ثابت 60 ث
#    ② عكس التدفّق المشبع (النطاق النشط، آخر ~15 د):
#         CALL ⇐ ميل ≤ −0.20 (بوت مشبع) · PUT ⇐ ميل ≥ +0.20 (كول مشبع)
#    ③ مساحة ≥10 نقاط حتى أقرب عائق: منطقة عرض/طلب صالحة أو حدّ VIX1D
#  التصنيف: A إن انطلقت من داخل منطقة في اتجاهها (±2 نقطة) · وإلا B
#  العقد: أول سترايك في الاتجاه منتصفه بين $3.90 و$4.50 (قاعدة خالد)
#  الخروج: وقف −40% · متحرك يُسلَّح عند +30% ويخرج عند −25% من الذروة ·
#          إغلاق إجباري 15:45 · الشرط يثبت لقطتين متتاليتين (حماية من سعر شاذ)
#  يُقاس بعد الخروج: أول بلوغ 10/15/20 نقطة SPX وأسوأ نزول قبل كلٍّ منها،
#  حتى 60 د من الدخول. المسار (SPX + منتصف العقد) كل 30 ث.
#  الحفظ: liq_snaps · tag = liq_bot · صف لكل صفقة (أعمدة lb_*) ⇒ /liq.csv
#  ⚠ النداءات الإضافية: شموع 5 د مرة كل 5 دقائق · سعر العقد يأتي من سلسلة
#    الجامع نفسها (صفر نداء) إلا إن خرج من نافذة ±15 سترايك (نداء كل 30 ث).
LB_ENABLED    = os.getenv("LB_ENABLED", "1") == "1"
LB_FROM, LB_TO = 9 * 60 + 45, 15 * 60          # نافذة الإشارات
LB_CLOSE      = 15 * 60 + 45                   # إغلاق إجباري
LB_BULL, LB_BEAR = 55.0, 45.0
LB_HOLD       = 60.0                           # ثبات المسيطرين (ث)
LB_FLOW       = 0.20                           # تشبّع التدفّق
LB_ROOM       = 10.0                           # أقل مساحة (نقاط SPX)
LB_COOL       = 900.0                          # 15 د بين إشارتين في نفس الاتجاه
LB_C_LO, LB_C_HI = 3.90, 4.50                  # نطاق سعر العقد
LB_SL         = 0.40                           # وقف −40%
LB_ARM        = 0.30                           # تسليح عند +30%
LB_TRAIL      = 0.25                           # خروج عند −25% من الذروة
LB_TRACK_MIN  = 60                             # قياس أهداف SPX
LB_PATH_SEC   = 30.0
LB_SAVE_SEC   = 60.0
LB_ZONE_NEAR  = 2.0                            # «داخل المنطقة» ± نقطتان
LB_BARS_SEC   = 300.0
LB_TGTS       = (10, 15, 20)
_LB = {"day": None, "n": 0, "trades": [], "vols": deque(maxlen=40),
       "spots": deque(maxlen=500), "open": None, "bars": [], "bars_t": 0.0,
       "bars_err": None, "zones": [], "hold": {"CALL": None, "PUT": None},
       "last": {"CALL": 0.0, "PUT": 0.0}, "cond": None, "flow": None,
       "restored_day": None, "ticks": 0, "errs": 0, "last_err": None}
_LB_LOCK = threading.RLock()
_CALLS = deque(maxlen=2000)                    # طوابع نداءات Tradier من هذه الوحدة


def counted(td_get):
    """يغلّف td_get لعدّ النداءات — العدد في آخر 60 ثانية يظهر في اللوحة."""
    if td_get is None or getattr(td_get, "_counted", False):
        return td_get

    def f(path, params):
        _CALLS.append(time.time())
        return td_get(path, params)
    f._counted = True
    return f


def calls_per_min(now=None):
    now = now or time.time()
    return sum(1 for t in list(_CALLS) if now - t <= 60.0)


def _hms(ny):
    return ny.strftime("%H:%M:%S")


# ── التدفّق من سلسلة الجامع (نفس تعريف flow_bias_active: رتبة 3–8) ──
def lb_vol_maps(chain):
    cm, pm = {}, {}
    for key, q in (chain or {}).items():
        try:
            k = float(key[1:])
        except ValueError:
            continue
        (cm if key[0] == "c" else pm)[k] = float(q[0] or 0.0)
    return cm, pm


def lb_flow(now, chain, spot):
    """يحفظ لقطة حجم كل دقيقة ويحسب ميل النطاق النشط مقابل لقطة ~15 د."""
    cm, pm = lb_vol_maps(chain)
    if cm and (not _LB["vols"] or now - _LB["vols"][-1][0] >= 60.0):
        _LB["vols"].append((now, cm, pm))
    ref, best = None, None
    for t, c0, p0 in _LB["vols"]:
        age = (now - t) / 60.0
        if 10.0 <= age <= 20.0 and (best is None or abs(age - FLOW_WINDOW_MIN) < best):
            ref, best = (t, c0, p0), abs(age - FLOW_WINDOW_MIN)
    if ref is None or not cm or spot is None:
        return None
    _t, c0, p0 = ref
    rank = _ranked(set(cm) & set(c0), spot)
    lo, hi = FLOW_RANGES["active"]
    C = P = 0.0
    for k, r in rank.items():
        if lo <= r <= hi:
            C += max(0.0, cm.get(k, 0.0) - c0.get(k, 0.0))
            P += max(0.0, pm.get(k, 0.0) - p0.get(k, 0.0))
    tot = C + P
    return {"bias": round((C - P) / tot, 3) if tot > 0 else None,
            "call": round(C), "put": round(P), "age": round((now - _t) / 60.0, 1)}


# ── مناطق العرض والطلب على 5 دقائق ──
def lb_parse_bars(js):
    ser = js.get("series") if isinstance(js, dict) else None
    data = ser.get("data") if isinstance(ser, dict) else None
    if data is None:
        return []
    if not isinstance(data, list):
        data = [data]
    out = []
    for b in data:
        hm = str(b.get("time", ""))[11:16]
        o, h, l, c = (_num(b.get(x)) for x in ("open", "high", "low", "close"))
        if _hm_mn(hm) is not None and o and h and l and c:
            out.append([hm, o, h, l, c])
    return out


def lb_zones(bars):
    """قاعدة (1–3 شموع هادئة) قبل شمعة اندفاع ⇒ منطقة.

       الاندفاع: جسم ≥ 1.5× متوسط مدى آخر 12 شمعة، وجسم ≥ 60% من مداها.
       القاعدة: حتى 3 شموع قبلها مداها ≤ 0.8× المتوسط (وإلا الشمعة السابقة وحدها).
       طلب (اندفاع صاعد): [أدنى قاع القاعدة، أعلى جسم فيها].
       عرض (اندفاع هابط): [أدنى جسم فيها، أعلى قمة القاعدة].
       تنكسر بإغلاق 5 د خلف طرفها البعيد (طلب تحت أدناها · عرض فوق أعلاها)."""
    zones = []
    for i in range(1, len(bars)):
        hist = bars[max(0, i - 12):i]
        A = sum(b[2] - b[3] for b in hist) / len(hist)
        hm, o, h, l, c = bars[i]
        body, rng = abs(c - o), h - l
        if A <= 0 or rng <= 0 or body < 1.5 * A or body < 0.6 * rng:
            continue
        base = []
        for j in range(i - 1, max(-1, i - 4), -1):
            if bars[j][2] - bars[j][3] <= 0.8 * A:
                base.append(bars[j])
            else:
                break
        if not base:
            base = [bars[i - 1]]
        if c > o:
            z = {"kind": "demand", "lo": min(b[3] for b in base),
                 "hi": max(max(b[1], b[4]) for b in base)}
        else:
            z = {"kind": "supply", "lo": min(min(b[1], b[4]) for b in base),
                 "hi": max(b[2] for b in base)}
        if z["hi"] - z["lo"] < 0.25:
            z["hi"] += 0.25
        z.update({"t": hm, "broken": None})
        for b in bars[i + 1:]:
            if (z["kind"] == "demand" and b[4] < z["lo"]) or \
               (z["kind"] == "supply" and b[4] > z["hi"]):
                z["broken"] = b[0]
                break
        z["lo"], z["hi"] = round(z["lo"], 2), round(z["hi"], 2)
        zones.append(z)
    return zones


def lb_bars_tick(td, ny, now):
    """شموع 5 د لـSPX مرة كل 5 دقائق (بعد إغلاق الشمعة بـ15 ثانية)."""
    mn = ny.hour * 60 + ny.minute
    due = (now - _LB["bars_t"] >= LB_BARS_SEC) or \
          (mn % 5 == 0 and ny.second >= 15 and now - _LB["bars_t"] >= 60.0)
    if not due or mn < 9 * 60 + 35:
        return
    _LB["bars_t"] = now
    day = ny.strftime("%Y-%m-%d")
    js, err = td("/markets/timesales", {"symbol": LIQ_UND, "interval": "5min",
                                        "start": f"{day} 09:30",
                                        "end": ny.strftime("%Y-%m-%d %H:%M"),
                                        "session_filter": "open"})
    if err or not isinstance(js, dict):
        _LB["bars_err"] = str(err or "رد غير متوقع")[:120]
        return
    bars = [b for b in lb_parse_bars(js) if _hm_mn(b[0]) + 5 <= mn]   # المكتملة فقط
    _LB["bars"], _LB["bars_err"] = bars, None
    _LB["zones"] = lb_zones(bars)


# ── قراءة الشروط ──
def lb_room(side, sp, zones, em_hi, em_lo):
    """المسافة إلى أقرب عائق في الاتجاه + اسمه."""
    obs = []
    for z in zones:
        if z["broken"]:
            continue
        if side == "CALL" and z["kind"] == "supply" and z["lo"] > sp:
            obs.append((z["lo"] - sp, f"عرض {z['lo']:.0f}–{z['hi']:.0f}"))
        if side == "PUT" and z["kind"] == "demand" and z["hi"] < sp:
            obs.append((sp - z["hi"], f"طلب {z['lo']:.0f}–{z['hi']:.0f}"))
    if side == "CALL" and em_hi is not None and em_hi > sp:
        obs.append((em_hi - sp, f"حدّ VIX1D {em_hi:.0f}"))
    if side == "PUT" and em_lo is not None and em_lo < sp:
        obs.append((sp - em_lo, f"حدّ VIX1D {em_lo:.0f}"))
    if not obs:
        return None, None
    d, n = min(obs)
    return round(d, 1), n


def lb_zone_at(side, sp, zones):
    want = "demand" if side == "CALL" else "supply"
    for z in reversed(zones):
        if not z["broken"] and z["kind"] == want and \
           z["lo"] - LB_ZONE_NEAR <= sp <= z["hi"] + LB_ZONE_NEAR:
            return z
    return None


def lb_eval(now, sp, bull, flow, zones, em_hi, em_lo, mn):
    """الشروط الثلاثة لكل اتجاه. يرجع (الحالة للعرض، الاتجاه الجاهز أو None)."""
    bias = flow["bias"] if flow else None
    st, ready = {}, None
    for side in ("CALL", "PUT"):
        p_ok = bull is not None and (bull >= LB_BULL if side == "CALL" else bull <= LB_BEAR)
        if p_ok:
            _LB["hold"][side] = _LB["hold"][side] or now
        else:
            _LB["hold"][side] = None
        held = round(now - _LB["hold"][side]) if _LB["hold"][side] else 0
        f_ok = bias is not None and (bias <= -LB_FLOW if side == "CALL" else bias >= LB_FLOW)
        room, obst = lb_room(side, sp, zones, em_hi, em_lo)
        r_ok = room is not None and room >= LB_ROOM
        cool = max(0, int(LB_COOL - (now - _LB["last"][side])))
        st[side] = {"p": p_ok, "held": held, "f": f_ok, "room": room, "obst": obst,
                    "r": r_ok, "cool": cool}
        if p_ok and held >= LB_HOLD and f_ok and r_ok and cool == 0 and \
                LB_FROM <= mn < LB_TO and ready is None:
            ready = side
    return st, ready


# ── العقد ──
def lb_quote(chain, side, k):
    q = (chain or {}).get(f"{'c' if side == 'CALL' else 'p'}{float(k):g}")
    if not q:
        return None
    b, a = q[1], q[2]
    if a is None or b is None or not (a > 0) or b < 0 or a < b:
        return None
    return {"bid": float(b), "ask": float(a), "mid": round((a + b) / 2.0, 4)}


def lb_pick(chain, side, sp):
    """أول سترايك خارج السعر في الاتجاه منتصفه داخل النطاق · وإلا الأقرب للنطاق."""
    t = "c" if side == "CALL" else "p"
    ks = []
    for key in (chain or {}):
        if key[0] != t:
            continue
        try:
            k = float(key[1:])
        except ValueError:
            continue
        if (side == "CALL" and k > sp) or (side == "PUT" and k < sp):
            ks.append(k)
    ks.sort(key=lambda k: abs(k - sp))
    best = None
    for k in ks:
        q = lb_quote(chain, side, k)
        if q is None:
            continue
        if LB_C_LO <= q["mid"] <= LB_C_HI:
            return dict(q, k=k, band=True)
        gap = LB_C_LO - q["mid"] if q["mid"] < LB_C_LO else q["mid"] - LB_C_HI
        if best is None or gap < best[0]:
            best = (gap, dict(q, k=k, band=False))
    return best[1] if best else None


def _hilo(mins, now):
    v = [s for t, s in _LB["spots"] if now - t <= mins * 60.0]
    return (round(max(v), 2), round(min(v), 2)) if v else (None, None)


def lb_open(ny, now, side, sp, st, flow, bull, chain, inp):
    c = lb_pick(chain, side, sp)
    if c is None:
        return None
    zones = _LB["zones"]
    z = lb_zone_at(side, sp, zones)
    h15, l15 = _hilo(15, now)
    h30, l30 = _hilo(30, now)
    s = st[side]
    _LB["n"] += 1
    day = ny.strftime("%Y-%m-%d")
    op = _LB["open"]
    why = [f"المسيطرون {'صعودي' if side == 'CALL' else 'هبوطي'} "
           f"{bull if side == 'CALL' else 100 - bull:.0f}% · ثابت {s['held']} ث",
           f"التدفّق مشبع {'بوت' if side == 'CALL' else 'كول'}: ميل {flow['bias']:+.2f} "
           f"(كول {flow['call']} · بوت {flow['put']})",
           f"المساحة {s['room']:.1f} نقطة حتى {s['obst']}"]
    if z:
        why.append(f"من داخل منطقة {'طلب' if z['kind'] == 'demand' else 'عرض'} "
                   f"{z['lo']:.0f}–{z['hi']:.0f} ({z['t']})")
    x = {"id": _LB["n"], "side": side, "t": _hms(ny), "tk": _ksa_hm(ny),
         "mn": ny.hour * 60 + ny.minute, "t0": now, "sp": sp,
         "grade": "A" if z else "B", "why": why, "room": s["room"], "obst": s["obst"],
         "bull": bull, "bias": flow["bias"], "fcall": flow["call"], "fput": flow["put"],
         "fage": flow["age"], "in_zone": "YES" if z else "NO",
         "zone_lo": z["lo"] if z else None, "zone_hi": z["hi"] if z else None,
         "zones": ";".join(f"{q['kind']}/{q['lo']}/{q['hi']}/{q['t']}/{q['broken'] or ''}"
                           for q in zones[-12:]),
         "open": op, "move_open": round(sp - op, 2) if op else None,
         "hi15": h15, "lo15": l15, "hi30": h30, "lo30": l30,
         "csym": _occ(day, side, c["k"]), "ck": c["k"], "cband": "YES" if c["band"] else "NO",
         "c0": c["mid"], "ca0": c["ask"], "cb0": c["bid"], "cnow": c["mid"],
         "state": "open", "peak": c["mid"], "armed": False, "arm_t": None,
         "exit_t": None, "exit_mid": None, "exit_bid": None, "reason": None,
         "pnl_mid": None, "pnl_real": None, "pnl_now": 0.0,
         "chi": c["mid"], "chi_t": _hms(ny), "clo": c["mid"], "clo_t": _hms(ny),
         "t10": None, "t15": None, "t20": None, "mae10": None, "mae15": None,
         "mae20": None, "mfe": 0.0, "mfe_t": None, "mae": 0.0, "spnow": sp,
         "end": "open", "gap": 0, "path": [[_hms(ny), round(sp, 2), c["mid"]]],
         "pend": None, "qmiss_t": 0.0, "inp": dict(inp or {}),
         "_saved": False, "_st": 0.0, "_pt": now}
    _LB["trades"].append(x)
    _LB["last"][side] = now
    _LB["hold"][side] = None
    return x


# ── إدارة الصفقة والقياس ──
def lb_manage(x, ny, now, sp, q):
    """يرجع True إن تغيّر ما يستحق الحفظ فوراً."""
    ch = False
    hms = _hms(ny)
    mn = ny.hour * 60 + ny.minute
    d = 1 if x["side"] == "CALL" else -1
    # أهداف SPX حتى 60 د من الدخول (تستمر بعد الخروج)
    if x["end"] == "open":
        mv = d * (sp - x["sp"])
        x["spnow"] = sp
        if mv > x["mfe"]:
            x["mfe"], x["mfe_t"] = round(mv, 2), hms
        x["mae"] = round(min(x["mae"], mv), 2)
        for T in LB_TGTS:
            if x[f"t{T}"] is None and mv >= T:
                x[f"t{T}"], x[f"mae{T}"] = hms, x["mae"]
                ch = True
        if mn - x["mn"] >= LB_TRACK_MIN or mn >= 15 * 60 + 55:
            x["end"] = "done"
            ch = True
    # العقد
    if x["state"] == "open" and q is not None:
        m = q["mid"]
        x["cnow"] = m
        x["pnl_now"] = round(m / x["c0"] - 1.0, 4)
        if m > x["chi"]:
            x["chi"], x["chi_t"] = m, hms
        if m < x["clo"]:
            x["clo"], x["clo_t"] = m, hms
        if m > x["peak"]:
            x["peak"] = m
        if not x["armed"] and m >= x["c0"] * (1.0 + LB_ARM):
            x["armed"], x["arm_t"] = True, hms
            ch = True
        why = None
        if m <= x["c0"] * (1.0 - LB_SL):
            why = f"SL-{int(LB_SL * 100)}%"
        elif x["armed"] and m <= x["peak"] * (1.0 - LB_TRAIL):
            why = f"Trail-{int(LB_TRAIL * 100)}%"
        elif mn >= LB_CLOSE:
            why = "TimeClose"
        if why and why != "TimeClose" and x["pend"] != why:
            x["pend"] = why                    # لقطتان متتاليتان قبل الخروج
            why = None
        if why:
            x.update({"state": "closed", "exit_t": hms, "exit_mid": m,
                      "exit_bid": q["bid"], "reason": why,
                      "pnl_mid": round(m / x["c0"] - 1.0, 4),
                      "pnl_real": round(q["bid"] / x["ca0"] - 1.0, 4) if x["ca0"] else None})
            ch = True
        elif not (m <= x["c0"] * (1.0 - LB_SL) or
                  (x["armed"] and m <= x["peak"] * (1.0 - LB_TRAIL))):
            x["pend"] = None
    # المسار
    if (x["state"] == "open" or x["end"] == "open") and now - x["_pt"] >= LB_PATH_SEC:
        x["path"].append([hms, round(sp, 2),
                          x["cnow"] if x["state"] == "open" else None])
        x["_pt"] = now
    return ch


def _lb_vals(x):
    v = {f"lb_{k}": x.get(k) for k in (
        "id", "side", "t", "tk", "grade", "room", "obst", "bull", "bias", "fcall",
        "fput", "fage", "in_zone", "zone_lo", "zone_hi", "zones", "open",
        "move_open", "hi15", "lo15", "hi30", "lo30", "csym", "ck", "cband", "c0",
        "ca0", "cb0", "state", "peak", "arm_t", "exit_t", "exit_mid", "exit_bid",
        "reason", "pnl_mid", "pnl_real", "chi", "chi_t", "clo", "clo_t", "t10",
        "t15", "t20", "mae10", "mae15", "mae20", "mfe", "mfe_t", "mae", "end", "gap")}
    v["lb_why"] = " | ".join(x.get("why") or [])[:500]
    # بلا فواصل: /liq.csv يستبدل الفاصلة بمسافة ⇒ «وقت/SPX/منتصف;…»
    v["lb_path"] = ";".join(f"{p[0]}/{p[1]}/{'' if p[2] is None else p[2]}"
                            for p in (x.get("path") or []))
    return v


def lb_persist(x, day, now, force=False):
    ex = _H["db_execute"]
    if ex is None:
        return False
    if x["_saved"] and not force and now - x["_st"] < LB_SAVE_SEC:
        return True
    key = f"lb_{day}_{x['id']}"
    v = _lb_vals(x)
    try:
        if not x["_saved"]:
            inp = x.get("inp") or {}
            base = {"sig_key": key, "tag": "liq_bot",
                    "captured_ny": f"{day} {x['t']}", "liq_und": LIQ_UND,
                    "expiration": day, "session": "open", "spot": x["sp"],
                    "gex": inp.get("gex"), "flip": inp.get("flip"),
                    "call_wall": inp.get("call_wall"), "put_wall": inp.get("put_wall"),
                    "vwap_dist_und": (round(x["sp"] - inp["vwap_und"], 2)
                                      if inp.get("vwap_und") is not None else None),
                    "em_hi": inp.get("em_hi"), "em_lo": inp.get("em_lo"),
                    "agg_bull_pct": x["bull"], "flow_bias_active": x["bias"],
                    "flow_call_15m": x["fcall"], "flow_put_15m": x["fput"],
                    "bot_side": x["side"], "bot_strike": x["ck"], "ok": "YES"}
            base.update(v)
            cols = list(base.keys())
            ex("INSERT INTO liq_snaps(" + ",".join(cols) + ") VALUES(" +
               ",".join(["?"] * len(cols)) + ")", tuple(base[c] for c in cols))
            x["_saved"] = True
        else:
            cols = [c for c in LB_COLS if c != "lb_id"]
            ex("UPDATE liq_snaps SET " + ",".join(f"{c} = ?" for c in cols) +
               " WHERE sig_key = ? AND tag = ?",
               tuple(v[c] for c in cols) + (key, "liq_bot"))
        x["_st"] = now
        return True
    except Exception as e:
        _LB["errs"] += 1
        _LB["last_err"] = f"persist: {type(e).__name__}: {e}"[:160]
        print("liq lb persist err:", e)
        return False


def lb_path_parse(txt):
    out = []
    for p in str(txt or "").split(";"):
        a = p.split("/")
        if len(a) == 3 and _hm_mn(a[0]) is not None:
            out.append([a[0], _num(a[1]), _num(a[2]) if a[2] else None])
    return out


def lb_restore(day, now, ny):
    """بعد إعادة تشغيل Render: صفقات اليوم من القاعدة وتُكمل من حيث توقفت.
       الفجوة (دقائق بلا رصد) تُسجَّل في lb_gap ولا تُملأ تخميناً."""
    q = _H["db_query"]
    if q is None:
        return 0
    try:
        rows = q("SELECT spot, " + ",".join(LB_COLS) + " FROM liq_snaps WHERE tag = ? "
                 "AND sig_key LIKE ? ORDER BY id", ("liq_bot", f"lb_{day}_%"))
    except Exception as e:
        print("liq lb restore err:", e)
        return 0
    mn_now = ny.hour * 60 + ny.minute
    lst, n = [], 0
    for r in rows:
        d = dict(zip(LB_COLS, r[1:]))
        try:
            i = int(d["lb_id"])
        except Exception:
            continue
        n = max(n, i)
        x = {k[3:]: d[k] for k in LB_COLS}
        x["sp"] = _num(r[0])
        x["c0"] = _num(x.get("c0"))
        if x["sp"] is None or not x["c0"]:
            continue
        x["path"] = lb_path_parse(d["lb_path"])
        x["why"] = d["lb_why"].split(" | ") if d["lb_why"] else []
        x["mn"] = _hm_mn(x["t"]) or 0
        for k in ("peak", "chi", "clo", "mfe", "mae"):
            x[k] = _num(x.get(k)) or (x["c0"] if k in ("peak", "chi", "clo") else 0.0)
        x["id"] = i
        x["armed"] = bool(x.get("arm_t"))
        last = x["path"][-1] if x["path"] else None
        x["cnow"] = (last[2] if last and last[2] else x["c0"])
        x["pnl_now"] = round(x["cnow"] / x["c0"] - 1.0, 4)
        x["spnow"] = last[1] if last else x["sp"]
        live = x.get("state") == "open" or x.get("end") == "open"
        gap = max(0, mn_now - (_hm_mn(last[0]) if last else x["mn"])) if live else 0
        x["gap"] = int(_num(x.get("gap")) or 0) + gap
        x.update({"pend": None, "qmiss_t": 0.0, "inp": {}, "restored": True,
                  "t0": now - (mn_now - x["mn"]) * 60.0,
                  "_saved": True, "_st": 0.0, "_pt": now})
        lst.append(x)
    with _LB_LOCK:
        _LB["trades"], _LB["n"] = lst[-60:], n
        for x in lst:
            _LB["last"][x["side"]] = max(_LB["last"][x["side"]], x["t0"])
    return len(lst)


def lb_tick(td, ny, now=None):
    """دورة البوت — بعد agg_tick الناجح (كل 5 ثوانٍ). لا ترمي أبداً."""
    if not LB_ENABLED:
        return "off"
    now = now or time.time()
    try:
        day = ny.strftime("%Y-%m-%d")
        mn = ny.hour * 60 + ny.minute
        if _LB["day"] != day:
            with _LB_LOCK:
                _LB.update({"day": day, "n": 0, "trades": [], "open": None,
                            "bars": [], "bars_t": 0.0, "zones": [], "cond": None,
                            "hold": {"CALL": None, "PUT": None},
                            "last": {"CALL": 0.0, "PUT": 0.0}})
                _LB["vols"].clear()
                _LB["spots"].clear()
            if _LB["restored_day"] != day:
                _LB["restored_day"] = day
                lb_restore(day, now, ny)
        with _AGG_LOCK:
            chain, sp = _AGG["prev"], _AGG["spot"]
        if sp is None or not chain:
            return "no-data"
        aw = agg_window(now=now)
        bull = aw["bull_pct"] if aw.get("ready") else None
        with _LB_LOCK:
            if _LB["open"] is None and mn >= 9 * 60 + 30:
                _LB["open"] = sp
            _LB["spots"].append((now, sp))
            flow = lb_flow(now, chain, sp)
            _LB["flow"] = flow
        lb_bars_tick(td, ny, now)
        inp = _DEC.get("in") or {}
        fresh = inp and now - inp.get("t", 0) <= 120
        em_hi = inp.get("em_hi") if fresh else None
        em_lo = inp.get("em_lo") if fresh else None
        with _LB_LOCK:
            st, ready = lb_eval(now, sp, bull, flow, _LB["zones"], em_hi, em_lo, mn)
            _LB["cond"] = {"t": _hms(ny), "sp": sp, "bull": bull, "flow": flow,
                           "st": st, "em_hi": em_hi, "em_lo": em_lo,
                           "win": LB_FROM <= mn < LB_TO}
            new = lb_open(ny, now, ready, sp, st, flow, bull, chain, inp) if ready else None
            items = list(_LB["trades"])
            _LB["ticks"] += 1
        for x in items:
            if x["state"] != "open" and x["end"] != "open":
                continue
            q = lb_quote(chain, x["side"], x["ck"]) if x["state"] == "open" else None
            if q is None and x["state"] == "open" and x.get("csym") and \
                    now - x["qmiss_t"] >= LB_PATH_SEC:
                x["qmiss_t"] = now                # خارج نافذة الجامع ⇒ نداء مباشر
                js, err = td("/markets/quotes", {"symbols": x["csym"], "greeks": "false"})
                if not err and isinstance(js, dict):
                    qq = (js.get("quotes") or {}).get("quote")
                    qq = qq[0] if isinstance(qq, list) and qq else qq
                    if isinstance(qq, dict):
                        b, a = _num(qq.get("bid")), _num(qq.get("ask"))
                        if a and b is not None and a >= b >= 0:
                            q = {"bid": b, "ask": a, "mid": round((a + b) / 2.0, 4)}
            with _LB_LOCK:
                ch = lb_manage(x, ny, now, sp, q)
            lb_persist(x, day, now, force=ch or x is new)
        return "ok"
    except Exception as e:
        _LB["errs"] += 1
        _LB["last_err"] = f"{type(e).__name__}: {e}"[:160]
        print("liq lb tick err:", e)
        return "err"


def lb_public():
    """للوحة عبر /liq_agg — الحالة + صفقات اليوم (بلا المسار) + المناطق."""
    with _LB_LOCK:
        tr = []
        for x in _LB["trades"]:
            tr.append({k: v for k, v in x.items()
                       if not k.startswith("_") and k not in ("path", "inp", "zones", "t0")})
        return {"lb_on": LB_ENABLED, "lb_day": _LB["day"], "lb_cond": _LB["cond"],
                "lb_trades": tr,
                "lb_zones": [z for z in _LB["zones"]][-10:],
                "lb_bars_err": _LB["bars_err"], "lb_err": _LB["last_err"],
                "lb_rules": {"bull": LB_BULL, "bear": LB_BEAR, "hold": LB_HOLD,
                             "flow": LB_FLOW, "room": LB_ROOM, "sl": LB_SL,
                             "arm": LB_ARM, "trail": LB_TRAIL,
                             "c_lo": LB_C_LO, "c_hi": LB_C_HI},
                "calls_min": calls_per_min()}


def status():
    """حالة الوحدة — للعرض في /health."""
    return {"version": VERSION, "enabled": LIQ_ENABLED, "url": LIQ_URL,
            "underlying": LIQ_UND, "timeout": LIQ_TIMEOUT,
            "strikes": LIQ_STRIKES,
            "flow_window_min": FLOW_WINDOW_MIN,
            "flow_max_age_min": FLOW_MAX_AGE_MIN,
            "flow_neutral": FLOW_NEUTRAL,
            "flow_edge_window": [FLOW_EDGE_MIN, FLOW_EDGE_MAX],
            "flow_edge_hot": FLOW_EDGE_HOT,
            "flow_edge_raw": True,              # [v2.3]
            "onset_detect": True,               # [v2.6]
            "flow_onset_min": FLOW_ONSET_MIN,
            "flow_onset_accel": FLOW_ONSET_ACCEL,
            "flow_prev_max": FLOW_PREV_MAX,
            "positioning_saved": True,          # [v2.4]
            "shared_client": _HTTP["c"] is not None,   # [v2.5]
            "pos_cols": ["gex", "vex", "chex", "flip", "flip_dist",
                         "call_wall", "put_wall", "atm_iv", "hours_left"],
            "flow_ranges": FLOW_RANGES,
            "agg": {"enabled": AGG_ENABLED, "sec": AGG_SEC,          # [v2.7]
                    "strikes": AGG_STRIKES,
                    "alive": bool(_AGG["thread"] and _AGG["thread"].is_alive()),
                    "ticks": _AGG["ticks"], "errs": _AGG["errs"],
                    "last_ok": _AGG["last_ok"], "last_err": _AGG["last_err"],
                    "events": len(_AGG["ev"]),
                    "series_points": len(_AGG["series"]),      # [v2.8]
                    "series_day": _AGG["series_day"]},
            "verdict_saved": True,                             # [v2.8]
            "dec": {"enabled": DEC_ENABLED, "ticks": _DEC["ticks"],   # [v2.9]
                    "day": _DEC["day"], "n": _DEC["n"],
                    "active": sum(1 for x in _DEC["list"] if not x["done"]),
                    "in_ok": _DEC["in_ok"], "in_err": _DEC["in_err"],
                    "errs": _DEC["errs"], "last_err": _DEC["last_err"],
                    "cur": (_DEC["cur"] or {}).get("v"),
                    "in_alive": bool(_DEC["thread"] and _DEC["thread"].is_alive())},
            "dec_legacy": DEC_LEGACY,                          # [v3.0]
            "lb": {"enabled": LB_ENABLED, "ticks": _LB["ticks"], "day": _LB["day"],
                   "n": _LB["n"], "open": sum(1 for x in _LB["trades"] if x["state"] == "open"),
                   "zones": len(_LB["zones"]), "bars": len(_LB["bars"]),
                   "bars_err": _LB["bars_err"], "errs": _LB["errs"],
                   "last_err": _LB["last_err"]},
            "calls_min": calls_per_min(),
            "db_query": _H["db_query"] is not None}
