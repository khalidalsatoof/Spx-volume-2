# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════════════════════
  لوحة سيولة العقود — تطبيق مستقل تماماً  (v2.3.1)
═══════════════════════════════════════════════════════════════════════════════
  خدمة منفصلة عن SPX Paper Bot. لا تتصل به ولا تشاركه قاعدة بيانات ولا حالة.
  ⇒ خطرها على المشروع = صفر. تُنشر وتُوقف وتُعدَّل بحرية تامة.

  ── الجديد في v1.8 ──
  ㊵ [v2.3] القرارات النشطة — القرار لم يعد يُمحى حين يعود إلى «انتظر»
     (طلب خالد 23 سبتمبر: قالت PUT ثم «انتظر» فقط فبدا كأن البيانات اختفت).
     ① كل قرار CALL/PUT مؤكَّد (بعد الـ60 ثانية) يُسجَّل برقم يومي: قرار #1، #2…
        بقيمه المجمَّدة: الوقت (NY وKSA) · SPX · الهدف · الإبطال · العقد المرشّح.
     ② يبقى على اللوحة 60 دقيقة بالضبط ثم يُحذف. قرار معاكس ⇒ قرار جديد
        ويبقى السابق حتى تنتهي دقائقه · نفس الاتجاه والسابق نشط ⇒ ليس جديداً.
     ③ العقد المرشّح = الأعلى تداولاً اليوم في اتجاه القرار وسعره ≤ $4.50
        (طلب خالد) · يُتتبَّع بالمنتصف: الآن · أعلى · أدنى خلال الستين دقيقة
        ونسبتها من سعر لحظة القرار مع وقت كلٍّ منها.
     ④ لمس الهدف أو الإبطال في SPX يُسجَّل بوقته ولا يُنهي التتبّع.
     ⑤ ثبات القرار يصمد أمام إعادة تحميل الصفحة: حالة التخلّف والتأكيد
        تُحفظ في المتصفح (عمر ≤ 3 دقائق). كان الجوال يعيد التحميل عند
        الرجوع للصفحة فيُصفّرها ⇒ PUT عند 10:47 ثم «الضغط متوازن» عند 10:50.
     ⑥ إصلاح: v2.3 الأولى لم تسجّل شيئاً — بيانات الصفحة بلا ts_ny (يحمله
        /snap فقط). التاريخ الآن من ساعة نيويورك في المتصفح.
     ⑦ الصفحة مغلقة لا تُفقد الساعة: كل 30 ثانية (والصفحة مفتوحة) وعند
        فتحها تُطلب شموع الدقيقة من /bars (Tradier) للعقد وللأداة من وقت
        القرار ⇒ الأعلى والأدنى ولمس الهدف والإبطال تُسدّ من البيانات
        الحقيقية. ⚠ تسجيل القرار نفسه يحتاج الصفحة مفتوحة لحظة صدوره.
     ⚠ لا تغيير في منطق القرار نفسه (العتبات والأهداف كما هي).

  ㊴ [v2.2] ① /snap يُخرج نطاق اليوم (day_high · day_low · day_range) لتحفظه
     liq v2.8 ويُختبر عليه سبب خسارة إشارات النطاق الميت.
     ② رسم قوة الاتجاه يقرأ سلسلة اليوم من الخادم (/liq_agg · حقل series ·
        نقطة لكل دقيقة) فيظهر اليوم كاملاً حتى لو لم تُفتح الصفحة إطلاقاً.
        المتصفح يبقى احتياطاً: تُدمج نقاطه مع الخادم، والخادم له الأولوية.

  ㊳ [v2.1.3] رسم «قوة الاتجاه» أوضح: خط واحد منعَّم (متوسط 5 دقائق) بدل خطّين
     متعاكسين يتقاطعان · مساحة خضراء فوق 50% وحمراء تحته · نقطة القيمة الحالية
     برقمها · شبكة ساعات · ارتفاع أكبر. ⚠ البيانات ما زالت من المتصفح حتى liq.

  ㊲ [v2.1.2] ثبات القرار — كان يتقلّب كل دقيقة عند عتبة 55% (22 سبتمبر 11:48–11:50)
     ① تخلّف في الضغط: يصير صعودياً عند ≥55% ولا يعود متوازناً إلا تحت 50%
        (والعكس للهبوط). رقم 54↔55 لم يعد يقلب شيئاً.
     ② التأكيد: الدخول (CALL/PUT) يثبت 60 ثانية متصلة قبل أن يظهر،
        والتراجع إلى «انتظر» 20 ثانية. يُكتب «قيد التأكيد» أثناءها.
     ③ الهدف = أول عائق في الطريق لا VWAP دائماً: جدار CALL عند +0.6 بين
        السعر وVWAP كان يُتجاهل فقالت CALL بهدف +9.7. الآن العائق الأقرب
        هو الهدف، وإن كان أقرب من الحدّ الأدنى ⇒ انتظر.
     + التدفّق يبقى داخل «تفاصيل متقدمة» (طلب خالد) · محور الزمن مُصلح.

  ㊱ [v2.1.1] محور الزمن في رسم قوة الاتجاه كان معكوساً (09:30 يميناً والخط يُرسم
     من اليسار) ⇒ صار يساراً ليطابق الرسم.

  ㉟ [v2.1] قرار أدق + قراءة أسهل
     ① شرط الربح/الخطر إلزامي: المسافة للهدف ≥ المسافة للإبطال، والهدف
        ≥ 0.04% من السعر (~3 نقاط SPX). وإلا «انتظر» مع النسبة مكتوبة.
        السبب: مثال 22 سبتمبر 11:04 قال CALL بهدف +5 وخطر −16 (1:3 ضدّك).
     ② العقد المرشّح: أقرب سترايك في اتجاه القرار مع سعر الطلب.
     ③ «قوة الاتجاه»: خط الضغط الصعودي عبر اليوم (نقطة كل دقيقة، يُحفظ
        في المتصفح لكل أداة ويتصفّر يومياً). ⚠ يمتلئ فقط والصفحة مفتوحة
        حتى يُضاف الجمع من الخادم في liq.
     ④ لصاقتا «مقاومة مباشرة» و«دعم مباشر» على أقرب مستوى فوق وتحت.

  ㉞ [v2.0] «القرار» — كلمة واحدة بدل مؤشرات متعاكسة
     الإطار (المعتمد عند SpotGamma ومن يتبعها): النظام أولاً ثم الاتجاه.
       ① النظام من خط الانقلاب: فوقه = تذبذب (الوسطاء يبيعون الصعود ويشترون
          الهبوط ⇒ السعر يرتد نحو VWAP) · تحته = ترند (يلاحقون الحركة ⇒ تمتد).
       ② التذبذب: الدخول **عكس** الامتداد عن VWAP بعد أن يتحوّل الضغط —
          يطابق نتيجتنا الوحيدة المسنودة (الإشارة المتأخرة بعد امتداد تخسر).
          الهدف VWAP · الإبطال الجدار خلف السعر.
       ③ الترند: الدخول **مع** جهة السعر من VWAP حين يؤكّد الضغط.
          الهدف الجدار التالي أو حدّ اليوم · الإبطال VWAP.
       الضغط (5د) لتأكيد التوقيت فقط لا لتحديد الاتجاه — لأنه يتقلّب.
     ⚠ تجريبي غير مختبَر. يُسجَّل للاختبار مع liq لاحقاً.
     + تنظيف: الخانات الأربع وشريط المشترين/البائعين وأزرار البوابة
       اختفت · شريط واحد صعودي/هبوطي · الأقسام القديمة (التدفّق والجدران
       والتموضع والإجماليات) مطويّة تحت «تفاصيل متقدمة».

  ㉝ [v1.9.3] ① /snap يُخرج بوابة VWAP وحدّي اليوم كحقول مسطّحة لتحفظها liq v2.7.
     ② شريط المسيطر يقرأ من الخادم (/liq_agg — جامع كل 5 ثوانٍ على Render)
        حين تكون تغطيته أكبر من تغطية المتصفح، ويسقط للمتصفح عند أي فشل.
        الخادم يجمع SPX فقط ⇒ تبويب SPY يبقى على حساب المتصفح.

  ㉜ [v1.9.2] «قراءة اللحظة» تظهر دائماً: خارج الجلسة باهتة بوسم «خارج
     الجلسة» مع آخر قراءة محفوظة للمسيطر، بدل الإخفاء التام.

  ㉛ [v1.9.1] شريط المسيطر يُحفظ في المتصفح (مفتاح لكل أداة) — ينجو من
     إعادة التحميل وقفل الجوال. ⚠ لا يملأ الفراغ: ما لم تكن الصفحة مفتوحة
     لا يُرى تداوله، فيُعرض «مغطّى X من 5 د» بدل ادّعاء نافذة كاملة.
     الحل الكامل (جمع دائم من الخادم) يأتي مع liq.
     + تخطيط متجاوب: عمود واحد على الجوال · عمود مركزي على اللابتوب.

  ㉚ [v1.9] «قراءة اللحظة» — قسم واحد في أعلى اللوحة بثلاثة أرقام خام
     ① المسيطر آخر 5 دقائق: كل عقد يُقارَن سعر آخر صفقة فيه بالعرض والطلب
        في اللقطة السابقة (قاعدة لي-ريدي). قرب الطلب = مشترٍ · قرب العرض =
        بائع · المنتصف لا يُصنَّف. يُحسب في المتصفح لأن Vercel بلا حالة.
        ⚠ غير مختبَر — يُعرض ويُسجَّل لاحقاً عبر liq قبل أي اعتماد.
     ② بوابة الدخول: بُعد SPY عن VWAP. الوحيد المسنود بصفقاتنا: 44 صفقة ·
        ≤$0.40 فوز 63% · أبعد 18%. ⚠ العتبة اختيرت بعد رؤية البيانات
        (من 4 عتبات) وتُحسم على صفقات 21–30 سبتمبر. SPX بلا حجم ⇒ VWAP من
        SPY دائماً، والمسافة تُحوَّل لنقاط SPX بنسبة السعرين.
        الحساب مطابق للمحاكاة: السعر النموذجي + تقييد الحجم الشاذ بخمسة
        أضعاف الوسيط (صفقات كتل مُبلَّغ عنها متأخرة كانت تشوّه VWAP).
     ③ حدّا اليوم: السعر ± السعر × VIX1D × √(الساعات المتبقية ÷ 1638).
        محاكاة 1,008 لقطة (4–18 سبتمبر): الإغلاق داخله 93% · المسار كله
        86% · سقط يوم الفدرالي. وسيط ما يبلغه السعر 21–32% منه ⇒ حدود لا أهداف.
     الجداران والانقلاب يظهران في السلّم بوسم «غير مختبَر» — محاكاة جدران
     OI صمدت 56% = نفس المستويات العشوائية كل 25 نقطة.
     ④ ساعة السوق من Tradier: اللوحة سجّلت لقطات يوم عطلة 7 سبتمبر بسعر
        ثابت. الحالة الآن تُصحَّح من /markets/clock (يسقط بصمت للحساب المحلي).
     ⚠ صفر تغيير في أي حساب قائم أو في /snap — الحقول الجديدة إضافية فقط.

  ㉙ [v1.8.3] عميل HTTP مشترك — يوقف بناء سياق SSL في كل نداء
     نفس إصلاح server وliq وtradier. على Vercel الأثر أصغر (الدوال
     قصيرة العمر) لكن المكسب حقيقي في النداءات المتتالية داخل الطلب
     الواحد: السلسلة والسعر وVIX وVIX0D — أربعة نداءات لكل /snap.
     ⚠ صفر تغيير في أي حساب أو عرض.

  ㉘ [v1.8.2] أرقام التموضع تُصدَّر مع اللقطة — كانت تُعرض وتُرمى
     العطل: snapshot_row لا يُخرج gex ولا vex ولا مستوى الانقلاب، مع أن
     fetch() يحسبها ويرجعها في مفتاح "pos" منذ v1.8. فكانت اللوحة تعرضها
     كل خمس ثوانٍ ولا يصل منها شيء إلى قاعدة بيانات البوت.
     الأثر: سؤال «هل بُعد السعر عن الانقلاب يفصل الرابح من الخاسر؟» و
     «هل تغيّر vex يسبق حركة SPY أم يتبعها؟» لا يُجابان بالنظر — يحتاجان
     سلسلة زمنية، ولا سلسلة بلا حفظ.
     الإصلاح: تمرير تسعة حقول من pos إلى مخرجات snapshot_row.
     ⚠ تمرير لا حساب: صفر نداءات إضافية لـTradier · صفر أرقام جديدة ·
       صفر تغيير في اللوحة أو في أي قرار. الأرقام محسوبة أصلاً وتُهمل.
     ⚠ يقابله liq v2.4 — وهو إلزامي: save() يبني الـINSERT من LIQ_COLS
       حرفياً، فأي مفتاح خارج القائمة يُرمى بصمت بلا رسالة خطأ.

  ㉗ [v1.8.1] إصلاح جدار البوت
     كان يأخذ أكبر OI في السلسلة كلها بلا وزن ولا نطاق ⇒ التقط 6000
     على SPX عند 7590 (21% تحت السعر) — سترايك تحوّط بعيد لا جدار
     تداولي. جدار الكول نجا صدفةً لأنه موزون بـGEX والغاما تتلاشى
     بعيداً عن السعر. الآن كلاهما بمقياس GEX وداخل WALL_NEAR_PCT.

  ㉖ [v1.8] لوحة التموضع — GEX · فانّا · تشارم
     الحجم يصف ما حدث. التموضع يصف ما **سيُجبَر** صنّاع السوق على فعله.
     • GEX (غاما): هل التحوّط يكبح الحركة أم يضخّمها؟ ليست اتجاهية —
       متماثلة بطبيعتها. تجيب: هل ستمتدّ أي حركة تبدأ أم تُبتلع؟
     • فانّا (∂Δ/∂σ): حين يتحرّك التقلّب الضمني يتغيّر تحوّط المتعاملين
       اتجاهياً. **اتجاهية** — وتعمل في نافذتنا الصباحية لأن VIX0D يتحرّك.
     • تشارم (∂Δ/∂t): الدلتا تنحدر بمرور الوقت وحده فيُجبَر التحوّط على
       التعديل. **اتجاهية** لكن أثرها يتركّز في آخر 90 دقيقة ⇒ خارج
       نافذتنا غالباً. تُعرض للسياق لا للقيادة.
     ⚠ يتطلب greeks=true في استعلام السلسلة (كان false).
     ⚠ افتراض المتعامل (قصير الكول · طويل البوت) يصمد لخيارات المؤشرات
       وينكسر في 0DTE ⇒ الأرقام حدّ أعلى لا حقيقة.
     ⚠ وصف لا قرار — تماماً كبقية اللوحة.

  ── الجديد في v1.7 ──
  ㉕ [v1.7] العدّاد يحسب النطاق النشط لا السلّم كله
     كان يجمع 16 سترايك فيعطي ~50/50 دائماً (السترايكان الملاصقان
     للسعر يبتلعان كل شيء ويتعادلان) بينما الرأس يعرض النطاق النشط.
     رقمان صحيحان لنطاقين مختلفين على شاشة واحدة. صار المصدر واحداً.

  ⑳ السلّم المركزي: السترايك في المنتصف · البوت يساراً والكول يميناً
     العين تنزل عموداً واحداً بلا مسح أفقي في كل صف.
     ⚠ مقياس الطول مشترك بين الجهتين (أطول شريط = 100%) — لو فُصل
       المقياسان لبدا 33k مساوياً لـ38k وهو تشويه.
  ㉑ خط السعر الحيّ يُدرَج بين السترايكين المحيطين به
     يريك موقع السعر بينهما، ويفصل المنطقة الخضراء عن الحمراء بصرياً.
  ㉒ عدّاد الهيمنة أسفل السلّم: شريط PUT/CALL + علامة التعادل 50%
     + فرق العقود + التسارع. الحكم قبل قراءة أي رقم.
  ㉓ تظليل النطاق النشط (رتبة 3–8) — المنطقة الوحيدة التي أظهرت
     إشارة في أول قياس حقيقي. النطاقان القريب والواسع أعطيا صفراً.
     ⚠ يبقى 8 سترايكات لكل جهة لا 6: النطاق النشط نفسه يمتد للرتبة 8،
       فتقليصه إلى 6 يخفي ثلث المنطقة التي يُحسب عليها المؤشر.
  ㉔ الأرقام دون 60 عقداً تُخفى — تنظيف الأطراف من ضجيج بلا معنى.

  ── الجديد في v1.5 ──
  ⑲ التدفّق يُقرأ من البوت (/liq_flow) لا من المتصفح
     دوال Vercel بلا حالة، فكان الحساب في localStorage يحتاج صفحة
     مفتوحة ربع ساعة — وأسوأ: لو فُتحت بعد ساعات أخذ لقطة قديمة جداً
     كمرجع فأعطى رقماً خاطئاً يبدو صحيحاً. /liq_cron يبني التاريخ في
     Postgres بلا علاقة بالمتصفح. أي فشل يسقط تلقائياً للحساب المحلي.

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

import math
import os
import re                                     # [v2.3] /bars
import threading
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

# [v1.8.1] نطاق جداري GEX — أوسع من شريط OI لأن الجدار قد يبعد عن السعر،
#          لكنه محدود وإلا التُقطت سترايكات التحوّط البعيدة بلا معنى تداولي.
WALL_NEAR_PCT = float(os.getenv("WALL_NEAR_PCT", "1.5"))

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

# [v1.9] بوابة الدخول: أقصى بُعد لـSPY عن VWAP في اتجاه الصفقة (دولار SPY)
VWAP_GATE_SPY = float(os.getenv("VWAP_GATE_SPY", "0.40"))
# تقييد حجم الشمعة الشاذة: أضعاف وسيط أحجام شموع اليوم
VWAP_CAP_MULT = float(os.getenv("VWAP_CAP_MULT", "5"))
VWAP_CACHE_SEC = 30.0
_VWAP = {"ts": 0.0, "day": None, "val": None}
_CLOCK = {"ts": 0.0, "val": None}
CLOCK_CACHE_SEC = 60.0
# ساعات جلسة كاملة × أيام تداول السنة — مقام VIX1D
EM_YEAR_HOURS = 6.5 * 252

_CACHE = {}
_EXPS = {}          # {underlying: (ts, [تواريخ])}
_VIX = {"ts": 0.0, "val": None}
_VIX1D = {"ts": 0.0, "val": None}
VIX_CACHE_SEC = 60.0
CUTOFF_NY = (16, 15)   # بعده تُعرض سلسلة الانتهاء التالي
_HIST = {}          # {underlying: [(ts, {(strike,side): vol})]}
HIST_KEEP_SEC = 1800
DELTA_WINDOW = 300  # نافذة التغيّر بالثواني (5 دقائق) — متدحرجة



# ═══════════════════════════════════════════════════════════════════════════
#  [v1.8.3] عميل HTTP مشترك — إصلاح تسرّب الذاكرة
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

_HTTP_LIMITS = httpx.Limits(max_keepalive_connections=4,
                            max_connections=8,
                            keepalive_expiry=30.0)
_HTTP = {"c": None}
_HTTP_LOCK = threading.Lock()


def _http():
    """العميل المشترك — يُبنى عند أول نداء فقط."""
    c = _HTTP["c"]
    if c is None:
        with _HTTP_LOCK:
            if _HTTP["c"] is None:
                _HTTP["c"] = httpx.Client(timeout=TD_TIMEOUT,
                                          limits=_HTTP_LIMITS,
                                          headers={"User-Agent": "spx-liqboard/1.8.3"})
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
        r = _http().get(f"{TD_BASE}{path}", params=params, timeout=TD_TIMEOUT,
                        headers={"Authorization": f"Bearer {TD_TOKEN}",
                                 "Accept": "application/json"})
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:200]}"
        return r.json(), None
    except Exception as e:
        # [v1.8.3] اتصال تالف ⇒ ابنِ عميلاً جديداً للنداء التالي
        if isinstance(e, getattr(httpx, "TransportError", Exception)):
            _http_reset()
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


def _market_clock():
    """[v1.9] حالة السوق من Tradier — تكشف العطل وأيام الإغلاق المبكر.

       يرجع open · premarket · postmarket · closed — أو None عند الفشل."""
    now = datetime.now().timestamp()
    if _CLOCK["val"] is not None and (now - _CLOCK["ts"]) < CLOCK_CACHE_SEC:
        return _CLOCK["val"]
    js, err = _get("/markets/clock", {})
    st = None
    if not err and isinstance(js, dict) and isinstance(js.get("clock"), dict):
        st = str(js["clock"].get("state") or "").lower() or None
    if st:
        _CLOCK["ts"], _CLOCK["val"] = now, st
    return st


def session_state():
    """حالة الجلسة بتوقيت نيويورك: قبل الافتتاح · مفتوح · بعد الإغلاق · عطلة.

       [v1.9] الحساب المحلي يُصحَّح بساعة Tradier في اتجاه واحد فقط
       (نحو الإغلاق): عطلة ⇒ مغلق · إغلاق مبكر ⇒ بعد الإغلاق."""
    loc = _session_local()
    try:
        clk = _market_clock()
    except Exception:
        clk = None
    if clk == "closed" and loc[0] != "closed":
        return "closed", "السوق مغلق اليوم"
    if clk == "postmarket" and loc[0] == "open":
        return "post", "بعد الإغلاق"
    return loc


def _session_local():
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


def _vwap_calc(bars, cap_mult=None):
    """[v1.9] VWAP الجلسة من شموع الدقيقة — بنفس طريقة المحاكاة حرفياً.

       السعر النموذجي (أعلى+أدنى+إغلاق)÷3 · وحجم كل شمعة مقيَّد بـcap_mult
       ضعف وسيط أحجام اليوم. يرجع (vwap, عدد الشموع, عدد المقيَّدة)."""
    cap_mult = VWAP_CAP_MULT if cap_mult is None else cap_mult
    rows = []
    for b in bars or []:
        if not isinstance(b, dict):
            continue
        v = _f(b.get("volume"))
        h, l, c = _f(b.get("high")), _f(b.get("low")), _f(b.get("close"))
        if v <= 0 or h <= 0 or l <= 0 or c <= 0:
            continue
        rows.append(((h + l + c) / 3.0, v))
    if not rows:
        return None, 0, 0
    vs = sorted(v for _, v in rows)
    m = len(vs)
    med = vs[m // 2] if m % 2 else (vs[m // 2 - 1] + vs[m // 2]) / 2.0
    cap = cap_mult * med if med > 0 else float("inf")
    num = den = 0.0
    capped = 0
    for tp, v in rows:
        if v > cap:
            v, capped = cap, capped + 1
        num += tp * v
        den += v
    if den <= 0:
        return None, len(rows), capped
    return num / den, len(rows), capped


def _spy_vwap():
    """[v1.9] VWAP الجلسة لـSPY من /markets/timesales — cache 30 ثانية.

       SPX مؤشر بلا حجم ⇒ لا VWAP له. نحسبه من SPY دائماً."""
    ny = datetime.now(NY)
    day = ny.strftime("%Y-%m-%d")
    now = datetime.now().timestamp()
    if _VWAP["day"] == day and (now - _VWAP["ts"]) < VWAP_CACHE_SEC:
        return _VWAP["val"]
    js, err = _get("/markets/timesales",
                   {"symbol": "SPY", "interval": "1min",
                    "start": f"{day} 09:30",
                    "end": ny.strftime("%Y-%m-%d %H:%M"),
                    "session_filter": "open"})
    if err or not isinstance(js, dict):
        return _VWAP["val"] if _VWAP["day"] == day else None
    bars = _listify(js.get("series"), "data")
    vw, nb, nc = _vwap_calc(bars)
    val = {"vwap": round(vw, 3), "bars": nb, "capped": nc} if vw else None
    _VWAP["ts"], _VWAP["day"], _VWAP["val"] = now, day, val
    return val


def _vwap_block(underlying, spot):
    """[v1.9] بوابة الدخول: بُعد SPY عن VWAP ومقابله بنقاط الأداة المعروضة."""
    try:
        vv = _spy_vwap()
        if not vv:
            return None
        spy = spot if underlying == "SPY" else _spot("SPY")[0]
        if not spy:
            return None
        ratio = (spot / spy) if underlying != "SPY" else 1.0
        dist = spy - vv["vwap"]
        return {
            "vwap_spy": round(vv["vwap"], 2), "spy": round(spy, 2),
            "dist_spy": round(dist, 2), "ratio": round(ratio, 4),
            "dist_und": round(dist * ratio, 2),
            "vwap_und": round(spot - dist * ratio, 2),
            "gate": VWAP_GATE_SPY,
            # CALL ممنوع إن كان السعر ممتداً فوق VWAP · PUT إن كان ممتداً تحته
            "call_ok": dist <= VWAP_GATE_SPY,
            "put_ok": -dist <= VWAP_GATE_SPY,
            "bars": vv["bars"], "capped": vv["capped"],
        }
    except Exception as e:
        print("vwap err:", e)
        return None


def _expected_move(spot, iv_pct, ny=None):
    """[v1.9] حدّا اليوم من التقلّب الضمني ليوم واحد.

       em = السعر × IV × √(الساعات المتبقية حتى 16:00 ÷ 1638).
       يرجع None خارج الجلسة أو بلا تقلّب."""
    ny = ny or datetime.now(NY)
    if not spot or not iv_pct or iv_pct <= 0:
        return None
    mins = 16 * 60 - (ny.hour * 60 + ny.minute) - ny.second / 60.0
    if mins <= 0 or mins > 390:
        return None
    hrs = mins / 60.0
    em = spot * iv_pct / 100.0 * math.sqrt(hrs / EM_YEAR_HOURS)
    return {"em": round(em, 2), "hi": round(spot + em, 2),
            "lo": round(spot - em, 2), "hours": round(hrs, 2),
            "iv": round(iv_pct, 2)}


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


# ═══════════════════════════════════════════════════════════════════════════
#  [v1.8] التموضع — GEX · فانّا · تشارم
# ═══════════════════════════════════════════════════════════════════════════
#  المبدأ: صانع السوق محايد الدلتا يجب أن يعيد التحوّط كلما تغيّرت دلتا
#  دفتره. وهي تتغيّر لثلاثة أسباب مستقلة:
#     غاما  ← حركة السعر    (متماثلة ⇒ ليست اتجاهية)
#     فانّا ← حركة التقلّب   (اتجاهية)
#     تشارم ← مرور الوقت     (اتجاهية · تتركّز آخر 90 دقيقة)
#
#  الاصطلاح المعياري: المتعامل قصير الكول وطويل البوت ⇒ مساهمة الكول
#  موجبة والبوت سالبة. يصمد جيداً لخيارات المؤشرات وينكسر في 0DTE،
#  فتُقرأ النتيجة حدّاً أعلى لا حقيقة.
#
#  r = q = 0: على أفق ساعات، الفائدة والتوزيعات لا تُذكر. وبهذا الفرض
#  يتساوى فانّا وتشارم للكول والبوت عند نفس السترايك (لأن دلتا البوت =
#  دلتا الكول − 1، وثابت الطرح يختفي بالاشتقاق) — والفرق كله في الإشارة.

def _norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def _bs_greeks(S, K, T, sig):
    """يرجع (gamma, vanna, charm) لعقد واحد — r=q=0.

       gamma = ∂²V/∂S²      · vanna = ∂Δ/∂σ  · charm = ∂Δ/∂t (سنوي)
       يرجع None عند أي مدخل غير صالح بدل أن يرمي."""
    try:
        if S <= 0 or K <= 0 or T <= 0 or sig <= 0:
            return None
        v = sig * math.sqrt(T)
        if v <= 1e-9:
            return None
        d1 = (math.log(S / K) + 0.5 * sig * sig * T) / v
        d2 = d1 - v
        ph = _norm_pdf(d1)
        gamma = ph / (S * v)
        vanna = -ph * d2 / sig
        charm = ph * d2 / (2.0 * T)
        return gamma, vanna, charm
    except (ValueError, ZeroDivisionError, OverflowError):
        return None


def _time_to_exp(exp_str):
    """سنوات حتى 16:00 نيويورك من تاريخ الانتهاء. أدنى حدّ 10 دقائق."""
    try:
        y, m, d = [int(x) for x in str(exp_str)[:10].split("-")]
        end = datetime(y, m, d, 16, 0, 0, tzinfo=NY)
        sec = (end - datetime.now(NY)).total_seconds()
        return max(sec, 600.0) / (365.0 * 24.0 * 3600.0)
    except Exception:
        return 1.0 / 365.0


def _positioning(rows, spot, exp_str):
    """يحسب تعرّض المتعاملين. يرجع dict — أو None إن غابت الإغريق.

       الوحدات: GEX بالدولار لكل حركة 1% · VEX بالدولار لكل نقطة تقلّب
       واحدة · CHEX بالدولار لكل يوم يمرّ."""
    try:
        T = _time_to_exp(exp_str)
        gex = vex = chex = 0.0
        per = []
        atm_iv = None
        atm_d = float("inf")
        for K, r in rows.items():
            for typ, sgn in (("call", 1.0), ("put", -1.0)):
                leg = r.get(typ) or {}
                oi = _i(leg.get("oi"))
                sig = _f(leg.get("iv"))
                if oi <= 0 or sig <= 0:
                    continue
                g = _bs_greeks(spot, K, T, sig)
                if g is None:
                    continue
                gm, vn, ch = g
                notional = oi * 100.0
                g_d = sgn * gm * notional * spot * spot * 0.01
                gex += g_d
                vex += sgn * vn * notional * spot * 0.01
                chex += sgn * ch * notional * spot / 365.0
                per.append({"strike": K, "typ": typ, "gex": g_d})
            dd = abs(K - spot)
            if dd < atm_d:
                cl = (r.get("call") or {}).get("iv")
                pl = (r.get("put") or {}).get("iv")
                ivs = [x for x in (cl, pl) if x]
                if ivs:
                    atm_d, atm_iv = dd, sum(ivs) / len(ivs)
        if not per:
            return None

        # ── مستوى الانقلاب: السعر الذي يعبر عنده GEX الصافي الصفر ──
        def gex_at(S):
            t = 0.0
            for K, r in rows.items():
                for typ, sgn in (("call", 1.0), ("put", -1.0)):
                    leg = r.get(typ) or {}
                    oi = _i(leg.get("oi"))
                    sig = _f(leg.get("iv"))
                    if oi <= 0 or sig <= 0:
                        continue
                    g = _bs_greeks(S, K, T, sig)
                    if g is None:
                        continue
                    t += sgn * g[0] * oi * 100.0 * S * S * 0.01
            return t

        flip = None
        lo, hi = spot * 0.97, spot * 1.03
        steps = 24
        prev_S = lo
        prev_v = gex_at(lo)
        for i in range(1, steps + 1):
            S = lo + (hi - lo) * i / steps
            v = gex_at(S)
            if prev_v is not None and v is not None and \
               ((prev_v < 0 <= v) or (prev_v > 0 >= v)):
                # تقريب خطّي بين النقطتين
                if v != prev_v:
                    flip = prev_S + (S - prev_S) * (0.0 - prev_v) / (v - prev_v)
                else:
                    flip = S
                break
            prev_S, prev_v = S, v

        # ── الجداران: بوزن GEX لا بـOI الخام، وداخل نطاق WALL_NEAR_PCT ──
        #  ⚠ عطل v1.8.0: جدار البوت كان يأخذ أكبر OI في السلسلة كلها بلا
        #    وزن ولا نطاق، فالتقط سترايك تحوّط بعيداً (6000 على SPX عند
        #    7590 = 21% تحت السعر). جدار الكول نجا صدفةً لأن GEX يوزن
        #    بالغاما وهي تتلاشى بعيداً عن السعر. الآن الاثنان بنفس
        #    المقياس: أكبر مساهمة كول موجبة فوق، وأكبر مساهمة بوت
        #    سالبة تحت — وكلاهما داخل نطاق قابل للتداول.
        span = spot * WALL_NEAR_PCT / 100.0
        up = [x for x in per if x["typ"] == "call"
              and 0 < x["strike"] - spot <= span]
        dn = [x for x in per if x["typ"] == "put"
              and 0 <= spot - x["strike"] <= span]
        call_wall = max(up, key=lambda x: x["gex"])["strike"] if up else None
        put_wall = min(dn, key=lambda x: x["gex"])["strike"] if dn else None

        return {
            "gex": round(gex, 0), "vex": round(vex, 0), "chex": round(chex, 0),
            "flip": round(flip, 2) if flip else None,
            "flip_dist": round(spot - flip, 2) if flip else None,
            "call_wall": call_wall, "put_wall": put_wall,
            "atm_iv": round(atm_iv * 100, 1) if atm_iv else None,
            "hours_left": round(T * 365 * 24, 2),
        }
    except Exception as e:
        print("positioning err:", e)
        return None


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

    # [v1.8] greeks=true — لازم لحساب GEX وفانّا وتشارم. يرجع
    #        delta · gamma · theta · vega · mid_iv لكل عقد من ORATS.
    js, err = _get("/markets/options/chains",
                   {"symbol": q_sym, "expiration": exp, "greeks": "true"})
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
        g = o.get("greeks") or {}
        rows.setdefault(strike, {"call": {}, "put": {}})[typ] = {
            "symbol": o.get("symbol"),
            "bid": bid, "ask": ask,
            "mid": round((bid + ask) / 2.0, 3) if ask > 0 else None,
            "spread": round(ask - bid, 3) if ask > 0 else None,
            "last": _f(o.get("last")) or None,           # [v1.9] المسيطر
            "vol": _i(o.get("volume")),
            "oi": _i(o.get("open_interest")),
            # [v1.8] الإغريق من ORATS عبر Tradier
            "iv": _f(g.get("mid_iv")) or _f(g.get("smv_vol")) or None,
            "delta": _f(g.get("delta")) if g.get("delta") is not None else None,
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
            "call_last": r["call"].get("last"),             # [v1.9]
            "call_sym": r["call"].get("symbol"),            # [v2.3] لتتبّع القرار
            "put_vol": pv, "put_oi": r["put"].get("oi", 0),
            "put_mid": r["put"].get("mid"),
            "put_bid": r["put"].get("bid"), "put_ask": r["put"].get("ask"),
            "put_spread": r["put"].get("spread"),
            "put_last": r["put"].get("last"),               # [v1.9]
            "put_sym": r["put"].get("symbol"),              # [v2.3]
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
    pos = _positioning(rows, spot, exp)          # [v1.8]

    # [v1.9] قراءة اللحظة — بوابة VWAP وحدّا اليوم
    ses = session_state()
    vwap = _vwap_block(underlying, spot) if ses[0] == "open" else None
    v1d = _vix1d()
    iv_src, iv_val = ("VIX1D", v1d) if v1d else \
        (("ATM", pos.get("atm_iv")) if pos and pos.get("atm_iv") else (None, None))
    em = _expected_move(spot, iv_val) if ses[0] == "open" else None
    if em:
        em["src"] = iv_src

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
        "session": ses[0], "session_txt": ses[1],
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
        "pos": pos,                                      # [v1.8] التموضع
        "vwap": vwap, "em": em,                          # [v1.9]
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

    # [v1.8.2] التموضع — محسوب في fetch() ومهمَل حتى الآن.
    #   يبقى None كاملاً إن غابت الإغريق (greeks=false أو سلسلة بلا IV)
    #   فلا ينكسر شيء — الحقول تُحفظ فارغة كبقية الحقول الاختيارية.
    p = d.get("pos") or {}

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
        # ── [v1.8.2] التموضع — ما سيُجبَر المتعاملون على فعله ──
        #  gex  نظام الحركة: سالب يمدّها · موجب يبتلعها
        #  vex  تعرّض الفانّا — اتجاهي، يعمل حين يتحرّك VIX0D
        #  chex تعرّض التشارم — اتجاهي، أثره في آخر 90 دقيقة
        #  flip / flip_dist  مستوى انقلاب الغاما وبُعد السعر عنه
        #  call_wall / put_wall  جداران بوزن GEX — غير جداري OI أعلاه
        #  atm_iv  التقلّب الضمني عند السعر — يلزم لقياس تغيّره لاحقاً
        #  hours_left  ساعات حتى الانتهاء — وزن التشارم يتبعها
        "gex": p.get("gex"),
        "vex": p.get("vex"),
        "chex": p.get("chex"),
        "flip": p.get("flip"),
        "flip_dist": p.get("flip_dist"),
        "call_wall": p.get("call_wall"),
        "put_wall": p.get("put_wall"),
        "atm_iv": p.get("atm_iv"),
        "hours_left": p.get("hours_left"),
        # ── [v1.9.3] قراءة اللحظة — للحفظ في liq v2.7 ──
        "vwap_spy": (d.get("vwap") or {}).get("vwap_spy"),
        "vwap_dist_spy": (d.get("vwap") or {}).get("dist_spy"),
        "vwap_dist_und": (d.get("vwap") or {}).get("dist_und"),
        "vwap_call_ok": (d.get("vwap") or {}).get("call_ok"),
        "vwap_put_ok": (d.get("vwap") or {}).get("put_ok"),
        "em_pts": (d.get("em") or {}).get("em"),
        "em_hi": (d.get("em") or {}).get("hi"),
        "em_lo": (d.get("em") or {}).get("lo"),
        "em_src": (d.get("em") or {}).get("src"),
        # [v2.2] نطاق اليوم حتى هذه اللحظة
        "day_high": d.get("day_high"), "day_low": d.get("day_low"),
        "day_range": (round(d["day_high"] - d["day_low"], 2)
                      if d.get("day_high") and d.get("day_low") else None),
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
    if row.get("gex") is not None:
        g = row["gex"]
        reg = "سالبة ⇒ الحركة تمتدّ" if g < 0 else "موجبة ⇒ الحركة تُبتلع"
        L.append(f"غاما {reg}")
        if row.get("flip") is not None:
            L.append(f"الانقلاب {row['flip']:g} · البُعد "
                     f"{row.get('flip_dist'):+g}")
    L.append(f"🕐 {row['ts_ny']} NY")
    return "\n".join(L)


def debug(underlying="SPY"):
    """يعرض أول عقد خاماً كما يرجعه Tradier — للتحقق من أسماء الحقول."""
    q_sym = UNDERLYINGS.get(str(underlying).upper(), ("SPY",))[0]
    exp, _tag = pick_expiration(q_sym)
    js, err = _get("/markets/options/chains",
                   {"symbol": q_sym, "expiration": exp, "greeks": "true"})
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
    return {"ok": True, "token": bool(TD_TOKEN), "version": "2.3.1",
            "clock": _market_clock(), "vwap_gate_spy": VWAP_GATE_SPY,  # [v1.9]
            "positioning": True, "greeks": True,
            "pos_in_snapshot": True,          # [v1.8.2]
            "shared_client": True,            # [v1.8.3]
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


# ═══ [v2.3] شموع الدقيقة لعقد القرار وللأداة — التتبّع يكتمل والصفحة مغلقة ═══
#  المتصفح يسجّل القرار ويحفظه، ثم يطلب من هنا شموع الدقيقة من وقت القرار
#  حتى الآن ⇒ الأعلى والأدنى ولمس الهدف والإبطال محسوبة من بيانات Tradier
#  الحقيقية حتى لو كانت الصفحة مغلقة أغلب الساعة. لا حفظ هنا (Vercel بلا حالة).
_OCC_RE = re.compile(r"[A-Z]{1,6}\d{6}[CP]\d{8}")
_HM_RE = re.compile(r"\d{2}:\d{2}")


def _bars(sym, start_hm):
    ny = datetime.now(NY)
    day = ny.strftime("%Y-%m-%d")
    js, err = _get("/markets/timesales",
                   {"symbol": sym, "interval": "1min",
                    "start": f"{day} {start_hm}",
                    "end": ny.strftime("%Y-%m-%d %H:%M"),
                    "session_filter": "open"})
    if err or not isinstance(js, dict):
        return None, err or "رد غير متوقع"
    out = []
    for b in _listify(js.get("series"), "data"):
        hm = str(b.get("time", ""))[11:16]
        h, l, c = _f(b.get("high")), _f(b.get("low")), _f(b.get("close"))
        if _HM_RE.fullmatch(hm) and h > 0 and l > 0:
            out.append([hm, round(h, 3), round(l, 3), round(c, 3)])
    return out, None


def bars(opt, und, start):
    if not _OCC_RE.fullmatch(opt or ""):
        return {"ok": False, "err": "رمز عقد غير صالح"}
    if not _HM_RE.fullmatch(start or ""):
        return {"ok": False, "err": "وقت بداية غير صالح"}
    u = (und or "SPX").upper()
    u = u if u in UNDERLYINGS else "SPX"
    ob, oe = _bars(opt, start)
    ub, ue = _bars(UNDERLYINGS[u][1], start)
    return {"ok": ob is not None or ub is not None, "opt": ob or [],
            "und": ub or [], "opt_err": oe, "und_err": ue,
            "ny_now": datetime.now(NY).strftime("%H:%M")}


@app.get("/bars")
def as_bars(opt: str = "", und: str = "SPX", start: str = ""):
    return JSONResponse(bars(opt, und, start))


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
def catch_all(full_path: str, u: str = "SPY", n: int = 0, r: int = 5,
              opt: str = "", und: str = "SPX", start: str = ""):
    p = "/" + (full_path or "").strip("/")
    if p.endswith("/bars"):                                   # [v2.3]
        return JSONResponse(bars(opt, und, start))
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

/* ── [v1.6] لوحة تدفّق آخر 15 دقيقة ── */
.flow{background:var(--c1);border:1px solid var(--ln);border-radius:13px;
 padding:8px 9px 6px;margin-bottom:9px}
.fhd{display:flex;justify-content:space-between;align-items:center;gap:6px;
 font-size:10px;color:var(--dim);margin-bottom:7px}
.fhd s{text-decoration:none;font-size:9px}
.ftot{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:7px}
.ft1{background:rgba(255,255,255,.03);border-radius:9px;padding:6px 3px;text-align:center}
.ft1 u{display:block;font-size:9px;color:var(--dim);text-decoration:none;margin-bottom:2px}
.ft1 b{font-size:14px;font-weight:700}
/* [v1.6] السترايك في المنتصف · البوت يساراً والكول يميناً
   مقياس الطول مشترك بين الجهتين ⇒ النسب صادقة بصرياً */
.fr{display:grid;grid-template-columns:1fr 46px 1fr;gap:4px;align-items:center;
 height:18px;margin-bottom:1px;padding:0 2px;border-radius:3px}
.fr.act{background:rgba(255,181,71,.10)}   /* النطاق النشط رتبة 3–8 */
.fs{font-size:10.5px;font-weight:700;text-align:center}
.fhalf{display:flex;align-items:center;gap:4px;min-width:0}
.fhalf.l{justify-content:flex-end}
.fbar{height:10px;border-radius:2px;transition:width .4s;flex:0 0 auto}
.fnum{font-size:9px;font-weight:700;white-space:nowrap}
/* خط السعر — يُدرَج بين السترايكين المحيطين بالسعر */
.fpx{display:flex;align-items:center;gap:6px;margin:3px 0 4px}
.fpx i{flex:1;height:2px;background:var(--ac);border-radius:1px}
.fpx b{font-size:10px;font-weight:700;color:#fff;background:var(--ac);
 border-radius:9px;padding:2px 8px;white-space:nowrap}
/* عدّاد الهيمنة */
.fmet{margin-top:9px;padding-top:8px;border-top:1px solid rgba(33,43,60,.6)}
.fmlbl{display:flex;justify-content:space-between;align-items:center;
 font-size:10px;margin-bottom:5px}
.fmbar{position:relative;height:8px;border-radius:4px;overflow:hidden;display:flex}
.fmbar u{height:100%;transition:width .4s}
.fmmid{position:relative;height:0}
.fmmid s{position:absolute;inset-inline-start:50%;top:-11px;width:2px;height:14px;
 background:var(--tx);opacity:.55;transform:translateX(-50%)}
.fmfoot{display:flex;justify-content:space-between;margin-top:8px;
 font-size:9.5px;color:var(--dim)}
/* ── [v1.8] لوحة التموضع ── */
.pos{background:var(--c1);border:1px solid var(--ln);border-radius:13px;
 padding:8px 9px;margin-bottom:9px}
.phd{display:flex;justify-content:space-between;align-items:center;
 font-size:10px;color:var(--dim);margin-bottom:7px}
.pvd{display:flex;align-items:center;justify-content:center;gap:8px;
 padding:7px 6px;border-radius:10px;margin-bottom:7px;font-weight:700;
 font-size:13px;letter-spacing:-.2px}
.pvd s{text-decoration:none;font-size:10px;font-weight:600;opacity:.8}
.p3{display:grid;grid-template-columns:repeat(3,1fr);gap:5px}
.p1{background:rgba(255,255,255,.03);border-radius:9px;padding:6px 3px;
 text-align:center}
.p1 u{display:block;font-size:9px;color:var(--dim);text-decoration:none;
 margin-bottom:3px}
.p1 b{display:block;font-size:12px;font-weight:700;line-height:1.25}
.p1 s{display:block;font-size:8.5px;text-decoration:none;color:var(--ft);
 margin-top:2px}
.plv{display:flex;justify-content:space-between;gap:6px;margin-top:7px;
 padding-top:7px;border-top:1px solid rgba(33,43,60,.6);
 font-size:9.5px;color:var(--dim)}
.plv b{font-weight:700}
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
/* ── [v1.9] قراءة اللحظة ── */
.now{background:var(--c1);border:1px solid var(--ln);border-radius:14px;padding:10px 10px 8px;margin-bottom:9px}
.nhd{display:flex;justify-content:space-between;align-items:center;font-size:10.5px;color:var(--dim);margin-bottom:8px}
.nhd b{color:var(--tx);font-size:12.5px;font-weight:700}
.nsec{margin-bottom:10px}
.nlb{display:flex;justify-content:space-between;align-items:center;font-size:10px;color:var(--dim);margin-bottom:5px}
.ntag{font-size:9px;padding:1px 6px;border-radius:6px;background:rgba(255,181,71,.13);color:var(--wr);font-weight:700}
.ntag.ok{background:rgba(45,212,160,.13);color:var(--up)}
.agb{display:flex;height:26px;border-radius:8px;overflow:hidden;font-size:11.5px;font-weight:700}
.agb u{display:flex;align-items:center;justify-content:center;text-decoration:none;transition:width .5s;white-space:nowrap;overflow:hidden}
.agv{margin-top:7px;font-size:13px;font-weight:700;text-align:center}
.ag4{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:7px}
.ag4 span{font-size:10.5px;font-weight:600;padding:5px 7px;border-radius:8px;background:rgba(255,255,255,.035);display:flex;justify-content:space-between}
.agf{margin-top:5px;font-size:9.5px;color:var(--ft);text-align:center}
.gp{display:grid;grid-template-columns:1fr 1fr;gap:6px}
.gp span{text-align:center;padding:7px 4px;border-radius:9px;font-size:12.5px;font-weight:700}
.gtr{position:relative;height:6px;border-radius:3px;background:rgba(255,255,255,.06);margin:9px 0 3px}
.gtr i{position:absolute;top:0;height:6px;background:rgba(45,212,160,.28);border-radius:3px}
.gtr b{position:absolute;top:-4px;width:3px;height:14px;border-radius:2px;background:var(--tx);transform:translateX(50%);transition:right .5s}
.gsc{display:flex;justify-content:space-between;font-size:9px;color:var(--ft)}
.lad{border-top:1px solid rgba(33,43,60,.6);padding-top:6px}
.lr{display:grid;grid-template-columns:64px 1fr 44px;gap:6px;align-items:center;padding:5px 2px;border-bottom:1px solid rgba(33,43,60,.45);font-size:11px}
.lr:last-child{border-bottom:none}
.lr b{font-weight:700;font-size:12px}
.lr s{text-decoration:none;color:var(--dim);font-size:10px}
.lr em{font-style:normal;text-align:left;font-size:10px;color:var(--dim)}
.lr.px{background:rgba(74,144,255,.14);border-radius:7px}
.lr.px b{color:#8ab6ff}
/* ── [v2.0] القرار ── */
.hide{display:none!important}
.vd{border-radius:12px;padding:12px 10px 10px;margin-bottom:10px;text-align:center;background:rgba(255,255,255,.035);border:1px solid var(--ln)}
.vw{font-size:30px;font-weight:800;letter-spacing:.5px;line-height:1.1}
.vr{margin-top:6px;font-size:12px;color:var(--tx);line-height:1.55}
.vt{display:flex;justify-content:center;gap:14px;margin-top:8px;font-size:12px;font-weight:700;flex-wrap:wrap}
.vt span{padding:3px 9px;border-radius:8px;background:rgba(255,255,255,.05)}
.vg{margin-top:7px;font-size:10.5px;color:var(--dim)}
/* ── [v2.3] آخر إشارة ── */
.ls{margin-top:10px;padding:9px 10px;border-radius:10px;background:rgba(255,255,255,.03);border:1px solid var(--ln);text-align:right;font-size:12px;line-height:1.7}
.ls .lh{display:flex;justify-content:space-between;align-items:center;gap:8px}
.ls .lh b{font-size:13px}
.ls .st{padding:1px 8px;border-radius:7px;font-size:11px;font-weight:700;white-space:nowrap}
.ls .ln{color:var(--dim);font-size:11px}
details.adv{margin-bottom:9px}
.ts{margin:0 0 10px}
.ts svg{width:100%;height:96px;display:block;background:linear-gradient(180deg,rgba(45,212,160,.05),rgba(255,255,255,.015) 50%,rgba(255,92,114,.05));border-radius:10px}
.tsl{direction:ltr;display:flex;justify-content:space-between;font-size:9.5px;color:var(--ft);margin-top:3px}
.lr i{font-style:normal;font-size:9px;font-weight:800;padding:1px 5px;border-radius:5px;margin-inline-start:4px}
details.adv>summary{cursor:pointer;list-style:none;text-align:center;font-size:12px;color:var(--dim);padding:9px;border:1px dashed var(--ln);border-radius:12px;margin-bottom:9px}
details.adv>summary::-webkit-details-marker{display:none}
details.adv[open]>summary{color:var(--tx)}
/* [v1.9.1] لابتوب: عمود مركزي بعرض قراءة مريح بدل تمدّد الأشرطة على الشاشة كلها */
@media (min-width:760px){body{max-width:720px;margin:0 auto;padding-left:18px;padding-right:18px}
 .agb{height:30px;font-size:13px}.agv{font-size:14.5px}.lr{font-size:12px;padding:6px 4px}}
@media (min-width:1200px){body{max-width:780px}}
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

<div class="now" id="now" style="display:none">
 <div class="nhd"><b>القرار</b><span id="nts"></span></div>
 <div class="vd" id="vd">
  <div class="vw" id="vW" style="color:var(--dim)">—</div>
  <div class="vr" id="vR">جارٍ القراءة…</div>
  <div class="vt" id="vT"></div>
  <div class="vg" id="vG">تجريبي · غير مختبَر</div>
  <div id="vL" style="display:none"></div>
 </div>
 <div class="ts"><div class="nlb"><span>قوة الاتجاه · الضغط الصعودي عبر اليوم</span><span id="tsn" style="font-size:9.5px"></span></div>
  <svg id="tsv" viewBox="0 0 390 96" preserveAspectRatio="none"></svg>
  <div class="tsl"><span>09:30</span><span>11:00</span><span>12:30</span><span>14:00</span><span>16:00</span></div></div>
 <div class="nsec">
  <div class="nlb"><span>الضغط · آخر 5 دقائق (للتوقيت فقط)</span><span class="ntag">غير مختبَر</span></div>
  <div class="agb"><u id="agB" style="width:50%;background:#2dd4a0;color:#06251b">صعودي —</u>
   <u id="agS" style="width:50%;background:#ff5c72;color:#2a060c">هبوطي —</u></div>
  <div class="agv hide" id="agV" style="color:var(--dim)">جارٍ البناء…</div>
  <div class="ag4 hide">
   <span><s style="text-decoration:none;color:var(--up)">شراء CALL</s><b id="agCB">—</b></span>
   <span><s style="text-decoration:none;color:var(--dn)">شراء PUT</s><b id="agPB">—</b></span>
   <span><s style="text-decoration:none;color:var(--dim)">بيع PUT ↑</s><b id="agPS">—</b></span>
   <span><s style="text-decoration:none;color:var(--dim)">بيع CALL ↓</s><b id="agCS">—</b></span>
  </div>
  <div class="agf" id="agF"></div>
 </div>
 <div class="nsec hide" id="gsec">
  <div class="nlb"><span>بوابة الدخول · بُعد SPY عن VWAP</span><span class="ntag ok">مسنود · 44 صفقة</span></div>
  <div class="gp"><span id="gC">CALL —</span><span id="gP">PUT —</span></div>
  <div class="gtr"><i id="gZ"></i><b id="gM"></b></div>
  <div class="gsc"><span id="gL">—</span><span id="gT">—</span><span id="gR">—</span></div>
 </div>
 <div class="nlb"><span>المستويات · الأقرب للسعر في الوسط</span><span id="lsrc"></span></div>
 <div class="lad" id="lad"></div>
</div>

<div class="exp"><span>سلسلة العقود</span><b id="exp">…</b></div>
<div class="picks"><span>سترايكات</span>__PICKS__</div>

<details class="adv"><summary>تفاصيل متقدمة · للتحليل ▾</summary>
<div class="flow" id="flow">
 <div class="fhd"><span>تدفّق آخر 15 دقيقة · 8 سترايك فوق و8 تحت</span>
  <span id="fnote"><s style="color:var(--dim)">جارٍ بناء النافذة…</s></span></div>
 <div class="ftot">
  <div class="ft1"><u>كول</u><b id="fcall" style="color:var(--up)">—</b></div>
  <div class="ft1"><u>تسارع</u><b id="faccel">—</b></div>
  <div class="ft1"><u>بوت</u><b id="fput" style="color:var(--dn)">—</b></div>
 </div>
 <div id="fbars"></div>
 <div class="fmet" id="fmet" style="display:none">
  <div class="fmlbl">
   <span id="fmput" style="color:var(--dn);font-weight:700">PUT —</span>
   <span id="fmdiff" style="color:var(--dim)">—</span>
   <span id="fmcall" style="color:var(--up);font-weight:700">CALL —</span></div>
  <div class="fmbar"><u id="fmp" style="background:#ff5c72;width:50%"></u>
   <u id="fmc" style="background:#2dd4a0;width:50%"></u></div>
  <div class="fmmid"><s></s></div>
  <div class="fmfoot"><span id="fmacc">تسارع —</span>
   <span>العدّاد والأرقام: النطاق النشط · رتبة 3–8</span></div>
 </div>
</div>
<div class="stats">
 <div class="st"><u>كول</u><b id="cv" style="color:var(--up)">—</b></div>
 <div class="st"><u>بوت / كول</u><b id="pc">—</b></div>
 <div class="st"><u>بوت</u><b id="pv" style="color:var(--dn)">—</b></div>
</div>

<div class="walls">
 <div class="wrow up" id="wup"><span class="wtag" style="color:var(--up)">▲ OI</span></div>
 <div class="wrow dn" id="wdn"><span class="wtag" style="color:var(--dn)">▼ OI</span></div>
</div>

<div class="pos" id="pos" style="display:none">
 <div class="phd"><span>التموضع — ما سيُجبَر المتعاملون على فعله</span>
  <span id="phrs"></span></div>
 <div class="pvd" id="pvd"><span>—</span></div>
 <div class="p3">
  <div class="p1"><u>غاما · النظام</u><b id="pg">—</b><s id="pgs">—</s></div>
  <div class="p1"><u>فانّا · التقلّب</u><b id="pv2">—</b><s id="pvs">—</s></div>
  <div class="p1"><u>تشارم · الوقت</u><b id="pc2">—</b><s id="pcs">—</s></div>
 </div>
 <div class="plv">
  <span>الانقلاب <b id="pflip">—</b></span>
  <span>جدار الكول <b id="pcw" style="color:var(--up)">—</b></span>
  <span>جدار البوت <b id="ppw" style="color:var(--dn)">—</b></span>
 </div>
</div>

</details>

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
/* ═══ [v1.6] تدفّق آخر 15 دقيقة ═══
   المبدأ: حجم الخيارات تراكمي منذ ما قبل الافتتاح ولا ينخفض أبداً.
   ⇒ الفرق بين لقطتين = ما تُدووِل في تلك الفترة بالضبط.
   ⚠ الطرح يتم **لكل سترايك على حدة** لا على المجموع: السعر يتحرك
     فيدخل السترايك النافذة أو يخرج منها، والطرح على المجموع يقيس
     حركة السعر لا التدفّق. (خطأ وقعنا فيه وصحّحناه — 4 سبتمبر)
   ⚠ رصيد ما قبل الافتتاح يسقط تلقائياً في الفرح لأنه في اللقطتين معاً. */
const FK="liq_flow_"+U;
/* [v1.6] مصدر التدفّق الأساسي: البوت.
   دوال Vercel بلا حالة فلا تحفظ لقطة سابقة، وحساب المتصفح كان يحتاج
   صفحة مفتوحة ربع ساعة — وأسوأ: لو فُتحت بعد ساعات أخذ لقطة قديمة
   جداً كمرجع فأعطى رقماً خاطئاً يبدو صحيحاً.
   /liq_cron يبني التاريخ في Postgres كل خمس دقائق بلا علاقة بالمتصفح.
   ⚠ قراءة فقط · وأي فشل يسقط تلقائياً إلى حساب المتصفح. */
const BOT="https://spx-paper-bot.onrender.com";
const SRV_MS=60000;              // نداء البوت كل دقيقة (التدفّق يتغيّر كل 5)
let SRV={t:0,data:null};
async function srvFlow(){
 if(U!=="SPX")return null;       // البوت يسجّل SPX فقط
 const now=Date.now();
 if(SRV.data&&now-SRV.t<SRV_MS)return SRV.data;
 try{
  const c=new AbortController(); setTimeout(()=>c.abort(),4000);
  const r=await fetch(BOT+"/liq_flow",{signal:c.signal});
  if(!r.ok)return SRV.data;
  const j=await r.json();
  if(!j||!j.ok)return SRV.data;
  SRV={t:now,data:j}; return j;
 }catch(e){return SRV.data;}
}
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
/* ══ [v1.6] لوحة تدفّق آخر 15 دقيقة ══
   ما تقوله: أين تُتداول العقود **الآن** — لا منذ الافتتاح.
   ⚠ لا تقول من المشتري ومن البائع (كل صفقة لها طرفان)، بل أين
     تتركّز الحرارة. ⚠ عتبات النص مؤقتة حتى تتوفر مئينات حقيقية. */
async function renderFlow(d){
 const el=document.getElementById("flow"); if(!el)return;
 // ── المصدر الأول: البوت (تاريخ دائم · يعمل فور فتح الصفحة) ──
 const sv=await srvFlow();
 if(sv&&sv.flow_bias_active!=null){drawFlow(sv,d,true);return;}
 // ── الاحتياطي: حساب المتصفح ──
 drawFlowLocal(d);
}
/* [v1.6] الرسم المشترك — يستعمله مسار البوت ومسار المتصفح معاً.
   المصدر واحد للتخطيط فلا ينحرف أحدهما عن الآخر مع الوقت.
   per = [{strike,call,put}] · spot = سعر الأداة لحظة اللقطة */
/* [v1.6.1] العدّاد يقرأ **النطاق النشط** لا السلّم كله.
   العطل الذي أصلحه: كان يجمع الستة عشر سترايكاً فيظهر 50/50 بينما
   البطاقات تقول 65/35. السترايكان الملاصقان للسعر (38k و33k) يبتلعان
   الفارق ويسحبان النسبة إلى التعادل — وهو نفس سبب استبعادهما من
   النطاق النشط أصلاً. عدّاد يُظهر التوازن حيث توجد إشارة أسوأ من
   عدّاد لا يوجد. actC/actP يأتيان من المستدعي (نفس مصدر البطاقات). */
function paintFlow(per, spot, acc, actC, actP){
 const F=document.getElementById("fbars"), M=document.getElementById("fmet");
 if(!per||!per.length){F.innerHTML="";if(M)M.style.display="none";return;}
 const rows=per.slice().sort((a,b)=>b.strike-a.strike);
 // مقياس مشترك للجهتين: أطول شريط في الجدول = 100%
 const mx=Math.max(...rows.map(x=>Math.max(x.call,x.put)),1);
 // الرتبة من السعر لكل جهة على حدة — النطاق النشط 3–8
 const ab=rows.filter(x=>x.strike>spot).map(x=>x.strike).sort((a,b)=>a-b);
 const be=rows.filter(x=>x.strike<=spot).map(x=>x.strike).sort((a,b)=>b-a);
 const rank=k=>((k>spot?ab:be).indexOf(k)+1);
 let h="";
 rows.forEach((x,i)=>{
  const up=x.strike>spot, rk=rank(x.strike), act=rk>=3&&rk<=8;
  const wc=Math.max(1,Math.round(100*x.call/mx));
  const wp=Math.max(1,Math.round(100*x.put/mx));
  h+=`<div class="fr${act?" act":""}">
   <span class="fhalf l"><span class="fnum" style="color:#ff5c72">${x.put>60?K(Math.round(x.put)):""}</span>
    <span class="fbar" style="width:${wp}%;background:#ff5c72b3"></span></span>
   <span class="fs" style="color:${up?"#2dd4a0":"#ff5c72"}">${x.strike}</span>
   <span class="fhalf"><span class="fbar" style="width:${wc}%;background:#2dd4a0b3"></span>
    <span class="fnum" style="color:#2dd4a0">${x.call>60?K(Math.round(x.call)):""}</span></span></div>`;
  // خط السعر يُدرج بين السترايكين المحيطين به
  const nx=rows[i+1];
  if(nx&&x.strike>spot&&nx.strike<=spot)
   h+=`<div class="fpx"><i></i><b>${Number(spot).toFixed(2)}</b><i></i></div>`;
 });
 F.innerHTML=h;
 // ── عدّاد الهيمنة ──
 if(!M)return;
 // [v1.7] المصدر الوحيد: مجموعا النطاق النشط (رتبة 3–8) — نفس ما يعرضه
 // الرأس والبطاقات. جمع السلّم كله كان يعطي ~50/50 دائماً لأن السترايكين
 // الملاصقين للسعر يبتلعان كل شيء ويتعادلان (flow_bias_wide = +0.002).
 let C=actC,P=actP;
 if(C==null||P==null){
  C=0;P=0;
  rows.forEach(x=>{const r=rank(x.strike);
   if(r>=3&&r<=8){C+=x.call;P+=x.put;}});
 }
 const tot=C+P;
 if(tot<=0){M.style.display="none";return;}
 M.style.display="";
 const pp=P/tot*100, pc=100-pp;
 document.getElementById("fmp").style.width=pp+"%";
 document.getElementById("fmc").style.width=pc+"%";
 document.getElementById("fmput").textContent="PUT "+pp.toFixed(0)+"%";
 document.getElementById("fmcall").textContent="CALL "+pc.toFixed(0)+"%";
 document.getElementById("fmdiff").textContent=
  "فرق "+K(Math.round(Math.abs(C-P)))+" عقد";
 const fa=document.getElementById("fmacc");
 fa.innerHTML=acc==null?"تسارع —"
  :`تسارع <b style="color:${acc>=2?"var(--wr)":"var(--tx)"}">${acc.toFixed(1)}×</b>`;
}
/* رسم من رد البوت */
function drawFlow(sv,d,fromBot){
 const setTxt=(id,v)=>{const e=document.getElementById(id);if(e)e.textContent=v;};
 const c=sv.flow_call_15m||0,p=sv.flow_put_15m||0,tot=c+p;
 setTxt("fcall",K(Math.round(c))); setTxt("fput",K(Math.round(p)));
 const acc=sv.flow_accel;
 setTxt("faccel",acc==null?"—":acc.toFixed(1)+"×");
 const ae=document.getElementById("faccel");
 if(ae)ae.style.color=acc==null?"var(--dim)":(acc>=2?"var(--wr)":(acc>=1.3?"var(--tx)":"var(--dim)"));
 const cp=tot>0?c/tot*100:50;
 let note,col;
 if(cp>=F_STRONG){note="نشاط CALL";col="var(--up)";}
 else if(100-cp>=F_STRONG){note="نشاط PUT";col="var(--dn)";}
 else if(Math.max(cp,100-cp)>=F_WEAK){
  note=(cp>50?"ميل CALL":"ميل PUT")+" · تركيز منخفض";
  col=cp>50?"rgba(45,212,160,.65)":"rgba(255,92,114,.65)";
 }else{note="نشاط متوازن";col="var(--dim)";}
 const dom=Math.max(cp,100-cp).toFixed(0);
 const burst=acc!=null&&acc>=2&&Math.max(cp,100-cp)>=F_STRONG;
 const w=sv.flow_window_min?Math.round(sv.flow_window_min):15;
 const ageTxt=(sv.snap_age_min!=null&&sv.snap_age_min>7)
   ?`<s style="color:var(--wr)"> · اللقطة قبل ${Math.round(sv.snap_age_min)}د</s>`:"";
 document.getElementById("fnote").innerHTML=
  `<span style="color:${col};font-weight:700">${burst?"⚡ ":""}${note} ${dom}%</span>`
  +`<s style="color:var(--ft);font-weight:600"> · ${w}د · مؤقتة</s>`+ageTxt;
 paintFlow(sv.per_strike||[], sv.spot||d.spot, acc, c, p);
}
/* الاحتياطي — حساب المتصفح (يعمل لو تعذّر البوت أو على SPY) */
function drawFlowLocal(d){
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
  const _m=document.getElementById("fmet"); if(_m)_m.style.display="none";
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
 paintFlow(now.per, d.spot, acc, now.call, now.put);
}
/* ══ [v1.8] لوحة التموضع ══
   ثلاثة أسباب مستقلة تُجبر صانع السوق على التحوّط:
     غاما  ← حركة السعر   ⇒ نظام (كبح/تضخيم) · ليست اتجاهية
     فانّا ← حركة التقلّب  ⇒ اتجاهية · تعمل في نافذتنا الصباحية
     تشارم ← مرور الوقت    ⇒ اتجاهية · تتركّز آخر 90 دقيقة
   ⚠ الحكم النهائي يجمع الثلاثة: الاتجاه من فانّا وتشارم،
     وقوّته من الغاما (السالبة تمدّد الحركة · الموجبة تبتلعها). */
const IVK="liq_iv_"+U;
const IV_WIN=300000;      // نافذة قياس تغيّر التقلّب: 5 دقائق
function pushIV(v){
 let h; try{h=JSON.parse(localStorage.getItem(IVK))||[]}catch(e){h=[]}
 const now=Date.now();
 if(v!=null&&(!h.length||now-h[h.length-1].t>20000))h.push({t:now,v:v});
 h=h.filter(x=>now-x.t<3600000);
 try{localStorage.setItem(IVK,JSON.stringify(h))}catch(e){}
 let ref=null;
 for(const x of h){if(now-x.t>=IV_WIN)ref=x;else break;}
 if(!ref||v==null)return null;
 return Math.round((v-ref.v)*10)/10;      // فرق بنقاط التقلّب
}
const MN=v=>{
 if(v==null)return "—";
 const a=Math.abs(v);
 if(a>=1e9)return (v/1e9).toFixed(1)+"B";
 if(a>=1e6)return (v/1e6).toFixed(0)+"M";
 if(a>=1e3)return (v/1e3).toFixed(0)+"K";
 return v.toFixed(0);
};
function renderPos(d){
 const el=document.getElementById("pos"); if(!el)return;
 const P0=d.pos;
 if(!P0||P0.gex==null){el.style.display="none";return;}
 el.style.display="";
 const g=P0.gex, vx=P0.vex, ch=P0.chex, spot=d.spot;
 const dIV=pushIV(P0.atm_iv);          // تغيّر التقلّب خلال 5 دقائق

 // ① الغاما — نظام لا اتجاه
 const neg=g<0;
 document.getElementById("pg").innerHTML=
  `<span style="color:${neg?"var(--dn)":"var(--up)"}">${neg?"سالبة":"موجبة"}</span>`;
 document.getElementById("pgs").textContent=
  (neg?"الحركة تمتدّ":"الحركة تُبتلع")+" · "+MN(Math.abs(g));

 // ② فانّا — الاتجاه يعتمد على اتجاه التقلّب نفسه
 //    VEX>0 ⇒ ارتفاع التقلّب يرفع دلتا الدفتر فيبيع المتعامل، والعكس
 let vTxt="—",vCol="var(--dim)",vSub="التقلّب ثابت",vScore=0;
 if(dIV!=null&&Math.abs(dIV)>=0.3&&vx){
  const buy=(vx>0&&dIV<0)||(vx<0&&dIV>0);
  vScore=buy?1:-1;
  vTxt=buy?"↑ شراء":"↓ بيع";
  vCol=buy?"var(--up)":"var(--dn)";
  vSub=(dIV<0?"التقلّب ↓":"التقلّب ↑")+" "+Math.abs(dIV).toFixed(1);
 }else if(dIV!=null){vSub="التقلّب "+(dIV>0?"+":"")+dIV;}
 document.getElementById("pv2").innerHTML=`<span style="color:${vCol}">${vTxt}</span>`;
 document.getElementById("pvs").textContent=vSub;

 // ③ تشارم — CHEX موجب ⇒ دلتا الدفتر ترتفع بمرور الوقت ⇒ بيع
 let cTxt="—",cCol="var(--dim)",cScore=0;
 if(ch){
  const buy=ch<0; cScore=buy?1:-1;
  cTxt=buy?"↑ شراء":"↓ بيع";
  cCol=buy?"var(--up)":"var(--dn)";
 }
 // وزن تشارم يكبر في آخر 90 دقيقة
 const late=P0.hours_left!=null&&P0.hours_left<=1.5;
 document.getElementById("pc2").innerHTML=`<span style="color:${cCol}">${cTxt}</span>`;
 document.getElementById("pcs").textContent=
  (late?"⚡ الوقت الفعّال":"أثره ضعيف الآن")+" · "+MN(Math.abs(ch));
 document.getElementById("phrs").innerHTML=
  P0.hours_left!=null?`<s style="color:var(--ft)">${P0.hours_left.toFixed(1)}س حتى الانتهاء</s>`:"";

 // ④ الحكم المجمَّع
 const score=vScore+(late?cScore:cScore*0.4);
 let vd,bg,fg;
 if(Math.abs(score)<0.5){
  vd=neg?"تضخيم · بلا ميل":"كبح · بلا ميل";
  bg=neg?"rgba(255,181,71,.13)":"rgba(255,255,255,.05)"; fg="var(--dim)";
 }else if(score>0){
  vd=(neg?"تضخيم":"كبح")+" · ميل CALL";
  bg="rgba(45,212,160,.14)"; fg="var(--up)";
 }else{
  vd=(neg?"تضخيم":"كبح")+" · ميل PUT";
  bg="rgba(255,92,114,.14)"; fg="var(--dn)";
 }
 const strength=neg?"ضغط ممتدّ":"ضغط مكبوح";
 const pv=document.getElementById("pvd");
 pv.style.background=bg; pv.style.color=fg;
 pv.innerHTML=`<span>${vd}</span><s>${strength}</s>`;

 // ⑤ المستويات
 const fl=document.getElementById("pflip");
 if(P0.flip){
  const dd=P0.flip_dist;
  fl.innerHTML=`${P0.flip.toFixed(0)} <s style="text-decoration:none;color:${dd>=0?"var(--up)":"var(--dn)"}">(${dd>0?"+":""}${dd.toFixed(0)})</s>`;
 }else fl.textContent="خارج ±3%";
 document.getElementById("pcw").textContent=P0.call_wall?P0.call_wall.toFixed(0):"—";
 document.getElementById("ppw").textContent=P0.put_wall?P0.put_wall.toFixed(0):"—";
}
/* ═══ [v1.9] قراءة اللحظة ═══
   المسيطر: الحجم الجديد بين لقطتين يُنسب لجهة بمقارنة سعر آخر صفقة بالعرض
   والطلب في اللقطة السابقة (قاعدة لي-ريدي). ≥60% من الفارق نحو الطلب =
   مشترٍ · ≤40% = بائع · بينهما لا يُصنَّف. فجوة >30 ثانية بين لقطتين ⇒
   لا نسب (لا نعرف متى تمّت الصفقات). الحالة في الذاكرة فقط: تبدأ من
   الصفر عند فتح الصفحة، وتكتمل النافذة بعد 5 دقائق. */
const AG_WIN=300000, AG_GAP=30000, AG_MIN=200;
const AGK="liq_ag_"+U;           // [v1.9.1] حفظ لكل أداة على حدة
let AG={prev:null,ev:[]};
try{const o=JSON.parse(localStorage.getItem(AGK));if(o&&Array.isArray(o.ev))AG=o;}catch(e){}
function agSave(){try{localStorage.setItem(AGK,JSON.stringify(AG));}catch(e){}}
function aggUpdate(d,now){
 const cur={};
 for(const t of (d.table||[]))for(const s of ["call","put"])
  cur[s[0]+t.strike]={v:t[s+"_vol"]||0,b:t[s+"_bid"],a:t[s+"_ask"],l:t[s+"_last"]};
 const P=AG.prev;
 if(P&&P.exp===d.expiration&&now-P.t<=AG_GAP&&now>P.t){
  const e={t:now,dt:now-P.t,cb:0,cs:0,pb:0,ps:0,u:0};
  for(const k in cur){
   const c=cur[k],p=P.q[k]; if(!p)continue;
   const dv=c.v-p.v; if(dv<=0)continue;
   let b=p.b,a=p.a; if(!(a>b&&b>=0)){b=c.b;a=c.a;}
   if(!(a>b&&b>=0)||c.l==null){e.u+=dv;continue;}
   const x=(c.l-b)/(a-b), sd=k[0];
   if(x>=0.6)e[sd+"b"]+=dv; else if(x<=0.4)e[sd+"s"]+=dv; else e.u+=dv;
  }
  AG.ev.push(e);
 }else if(P&&P.exp!==d.expiration)AG.ev=[];   // انتهاء جديد ⇒ بداية نظيفة
 // فجوة >30 ثانية (قفل الجوال): لا يُنسب حجمها لأحد، والأحداث السابقة تبقى
 // ما دامت داخل الخمس دقائق — والتغطية تُعرض صراحة.
 AG.prev={t:now,q:cur,exp:d.expiration};
 AG.ev=AG.ev.filter(x=>now-x.t<=AG_WIN);
 agSave();
 const r={cb:0,cs:0,pb:0,ps:0,u:0,cov:0};
 for(const e of AG.ev){for(const k of ["cb","cs","pb","ps","u"])r[k]+=e[k];r.cov+=(e.dt||5000);}
 r.cov=Math.min(r.cov,AG_WIN);
 return r;
}
function aggRead(r){
 const cls=r.cb+r.cs+r.pb+r.ps, all=cls+r.u;
 if(cls<AG_MIN)return {ready:false,cls,all,covMin:r.cov/60000};
 const buy=r.cb+r.pb, bull=r.cb+r.ps;
 const g=[["cb","مشترو CALL",1],["pb","مشترو PUT",-1],["ps","بائعو PUT",1],["cs","بائعو CALL",-1]]
  .sort((x,y)=>r[y[0]]-r[x[0]])[0];
 return {ready:true,cls,all,buyPct:buy/cls*100,bullPct:bull/cls*100,
  lead:g[1],leadDir:g[2],covMin:r.cov/60000,leadPct:r[g[0]]/cls*100,cover:all?cls/all*100:0,
  pct:{cb:r.cb/cls*100,cs:r.cs/cls*100,pb:r.pb/cls*100,ps:r.ps/cls*100}};
}
/* [v1.9.3] المسيطر من الخادم — جامع liq v2.7 كل 5 ثوانٍ طوال الجلسة.
   يُسأل كل 8 ثوانٍ، والرد يُعتبر صالحاً 30 ثانية. عند أي فشل يبقى
   حساب المتصفح كما هو. */
const SA={t:0,at:0,d:null};
function srvAgg(){
 const now=Date.now();
 if(now-SA.t>8000){SA.t=now;
  const c=new AbortController();setTimeout(()=>c.abort(),4000);
  fetch(BOT+"/liq_agg",{signal:c.signal}).then(r=>r.json())
   .then(j=>{if(j&&j.ok){SA.d=j;SA.at=Date.now();}}).catch(()=>{});}
 return (SA.d&&now-SA.at<30000&&SA.d.underlying===U)?SA.d:null;
}
/* ═══ [v2.0] القرار — النظام أولاً ثم الاتجاه ═══
   دالة نقية: تأخذ اللقطة ونسبة الضغط الصعودي وترجع {v, c, why, tgt, inv}.
   ⚠ تجريبية — تُختبر على السجل قبل أي اعتماد. */
function decide(d,bull,fstate){
 const P0=d.pos||{}, sp=d.spot, w=d.vwap, flip=P0.flip;
 const R=(v,why)=>({v:v,c:v.includes("CALL")?"var(--up)":v.includes("PUT")?"var(--dn)":"var(--wr)",why:why,tgt:null,inv:null,rr:null,side:null});
 if(!w||sp==null)return R("انتظر","بانتظار VWAP");
 const g=w.gate, ext=w.dist_spy, vw=w.vwap_und;
 const near=sp*0.0007;                       // ~5 نقاط SPX · ~0.5 SPY
 const minTgt=sp*0.0004;                     // ~3 نقاط SPX · ~0.3 SPY
 const flow=(fstate!=null)?fstate:(bull==null?0:bull>=55?1:bull<=45?-1:0);
 const fTxt=bull==null?"الضغط لم يكتمل":flow>0?"الضغط صعودي "+Math.round(bull)+"%":flow<0?"الضغط هبوطي "+Math.round(100-bull)+"%":"الضغط متوازن";
 const cw=P0.call_wall, pw=P0.put_wall, em=d.em||{};
 const trend=(flip!=null&&sp<flip);
 const dg=sp>1000?0:2, pts=v=>(v>0?"+":"")+v.toFixed(sp>1000?1:2), ext$="$"+Math.abs(ext).toFixed(2);
 // الحكم النهائي: الربح يجب أن يغطّي الخطر
 const fin=(side,strong,why,tgtP,tgtN,invP,invN)=>{
  if(tgtP==null||invP==null)return R("انتظر",why+" · لا هدف أو إبطال محدَّد");
  const rew=Math.abs(tgtP-sp), risk=Math.abs(sp-invP);
  const rrT="ربح "+rew.toFixed(sp>1000?0:2)+" : خطر "+risk.toFixed(sp>1000?0:2);
  if(rew<minTgt)return Object.assign(R("انتظر",why+" · الهدف قريب جداً ("+pts(tgtP-sp)+")"),{rr:rrT+" ✗"});
  if(rew<risk)return Object.assign(R("انتظر",why+" · الخطر أكبر من الربح"),{rr:rrT+" ✗"});
  const o=R((strong&&rew>=1.5*risk?"STRONG ":"")+side,why);
  o.side=side; o.rr=rrT+" ✓";
  o.tgtP=tgtP; o.invP=invP; o.tgtN=tgtN; o.invN=invN;
  o.tgt="الهدف "+tgtN+" "+tgtP.toFixed(dg)+" ("+pts(tgtP-sp)+")";
  o.inv="الإبطال "+invN+" "+invP.toFixed(dg)+" ("+pts(invP-sp)+")";
  return o;};
 if(!trend){
  const rg="تذبذب"+(flip!=null?" (فوق الانقلاب "+Math.round(flip)+")":"")+" — يميل للارتداد نحو VWAP";
  if(ext<=-g){
   if(flow<=0)return R("انتظر",rg+" · تحت VWAP بـ"+ext$+" لكن "+fTxt+" — انتظر تحوّله صعودياً");
   const atW=pw!=null&&sp-pw>=0&&sp-pw<=near;
   const inv=(pw!=null&&pw<sp)?pw:(em.lo!=null?em.lo:null);
   // أول عائق فوق السعر: جدار CALL إن سبق VWAP
   const blk=(cw!=null&&cw>sp&&cw<vw);
   if(blk&&cw-sp<minTgt)return Object.assign(R("انتظر",rg+" · تحت VWAP بـ"+ext$+" · "+fTxt+" · لكن جدار CALL فوقك مباشرة ("+pts(cw-sp)+")"),{rr:"ربح "+(cw-sp).toFixed(sp>1000?0:2)+" حتى أول مقاومة ✗"});
   return fin("CALL",ext<=-2*g||atW,rg+" · تحت VWAP بـ"+ext$+" · "+fTxt+(atW?" · عند جدار PUT":""),
     blk?cw:vw,blk?"جدار CALL":"VWAP",inv,(pw!=null&&pw<sp)?"كسر جدار PUT":"كسر حدّ اليوم");}
  if(ext>=g){
   if(flow>=0)return R("انتظر",rg+" · فوق VWAP بـ"+ext$+" لكن "+fTxt+" — انتظر تحوّله هبوطياً");
   const atW=cw!=null&&cw-sp>=0&&cw-sp<=near;
   const inv=(cw!=null&&cw>sp)?cw:(em.hi!=null?em.hi:null);
   const blk=(pw!=null&&pw<sp&&pw>vw);
   if(blk&&sp-pw<minTgt)return Object.assign(R("انتظر",rg+" · فوق VWAP بـ"+ext$+" · "+fTxt+" · لكن جدار PUT تحتك مباشرة ("+pts(pw-sp)+")"),{rr:"ربح "+(sp-pw).toFixed(sp>1000?0:2)+" حتى أول دعم ✗"});
   return fin("PUT",ext>=2*g||atW,rg+" · فوق VWAP بـ"+ext$+" · "+fTxt+(atW?" · عند جدار CALL":""),
     blk?pw:vw,blk?"جدار PUT":"VWAP",inv,(cw!=null&&cw>sp)?"اختراق جدار CALL":"اختراق حدّ اليوم");}
  return R("انتظر",rg+" · قريب من VWAP ("+(ext>=0?"+":"−")+ext$+") — لا ميزة، انتظر ابتعاده");
 }
 const rt="ترند (تحت الانقلاب "+Math.round(flip)+") — الحركة تميل للامتداد";
 const dir=ext<0?-1:1;
 if(flow===0||flow!==dir)return R("انتظر",rt+" · "+(dir<0?"تحت":"فوق")+" VWAP لكن "+fTxt+" — لا تأكيد");
 const st=(dir<0?bull<=40:bull>=60)&&Math.abs(ext)<=2*g;
 const nx=dir<0?((pw!=null&&pw<sp)?pw:em.lo):((cw!=null&&cw>sp)?cw:em.hi);
 const nxN=dir<0?((pw!=null&&pw<sp)?"جدار PUT":"حدّ اليوم"):((cw!=null&&cw>sp)?"جدار CALL":"حدّ اليوم");
 return fin(dir<0?"PUT":"CALL",st,rt+" · "+(dir<0?"تحت":"فوق")+" VWAP · "+fTxt,
   nx==null?null:nx,nxN,vw,"عودة "+(dir<0?"فوق":"تحت")+" VWAP");
}
/* ═══ [v2.1.2] ثبات القرار ═══
   ① تخلّف الضغط: +1 عند ≥55 ويبقى حتى <50 · −1 عند ≤45 ويبقى حتى >50.
   ② تأكيد 60 ثانية: القرار الجديد يظهر فقط بعد ثباته دقيقة متصلة. */
const VS={f:0,cur:null,cand:null,since:0};
/* [v2.3] حالة الثبات تُحفظ في المتصفح — الجوال يعيد تحميل الصفحة عند الرجوع
   إليها فكانت تُصفَّر: الضغط 49–52% يصير «متوازن» والقرار يقفز PUT ↔ انتظر.
   تُستعاد إن كان عمرها < 3 دقائق (أقدم من ذلك = السوق تغيّر ⇒ نبدأ من جديد). */
const VSK="liq_vs_"+U, VS_TTL=180000;
try{const o=JSON.parse(localStorage.getItem(VSK));
 if(o&&Date.now()-o.at<VS_TTL){VS.f=o.f||0;VS.cur=o.cur||null;VS.cand=o.cand||null;VS.since=o.since||0;}}catch(e){}
function vsSave(){try{localStorage.setItem(VSK,JSON.stringify({f:VS.f,cur:VS.cur,cand:VS.cand,since:VS.since,at:Date.now()}));}catch(e){}}
const V_CONFIRM=60000;
function flowHyst(bull){
 if(bull==null)return 0;   // [v2.3] لا نمسح الحالة حين يتأخر الضغط لحظياً
 if(VS.f===1){ if(bull<50)VS.f=(bull<=45?-1:0); }
 else if(VS.f===-1){ if(bull>50)VS.f=(bull>=55?1:0); }
 else { VS.f=bull>=55?1:bull<=45?-1:0; }
 return VS.f;
}
function stableVerdict(raw,now){
 if(!VS.cur){VS.cur=raw;VS.cand=null;return {o:raw,pending:null};}
 if(raw.v===VS.cur.v){VS.cur=raw;VS.cand=null;return {o:raw,pending:null};}
 if(!VS.cand||VS.cand.v!==raw.v){VS.cand=raw;VS.since=now;}
 else VS.cand=Object.assign(raw,{});
 // التراجع إلى «انتظر» أسرع (20ث) من الدخول (60ث) — الحذر أولى
 const need=raw.v==="انتظر"?20000:V_CONFIRM;
 if(now-VS.since>=need){VS.cur=raw;VS.cand=null;return {o:raw,pending:null};}
 return {o:VS.cur,pending:{v:raw.v,left:Math.ceil((need-(now-VS.since))/1000)}};
}
/* [v2.3] العقد المرشّح = الأعلى تداولاً اليوم في اتجاه القرار وسعره ≤ $4.50
   (طلب خالد 23 سبتمبر). تعادل الحجم ⇒ الأقرب للسعر. */
const PICK_MAX_ASK=4.5;
function pickContract(d,side){
 const T=d.table||[]; if(!side||!T.length)return null;
 const sp=d.spot; let best=null;
 for(const t of T){
  const k=t.strike, ask=side==="CALL"?t.call_ask:t.put_ask, v=Number(side==="CALL"?t.call_vol:t.put_vol)||0;
  if(!(ask>0)||ask>PICK_MAX_ASK)continue;
  if(!best||v>best.v||(v===best.v&&Math.abs(k-sp)<Math.abs(best.k-sp)))best={k:k,ask:ask,v:v,sym:(side==="CALL"?t.call_sym:t.put_sym)||null};
 }
 return best;
}
/* ═══ [v2.3] القرارات النشطة — كل قرار مؤكَّد يبقى 60 دقيقة ثم يُحذف ═══
   • يُرقَّم يومياً: قرار #1، #2… · إشارة معاكسة ⇒ قرار جديد والسابق يبقى
     حتى تنتهي دقائقه الستون · نفس الاتجاه والسابق ما زال نشطاً ⇒ ليس جديداً.
   • العقد المرشّح يُجمَّد لحظة القرار (الأعلى تداولاً · ≤ $4.50) ويُتتبَّع
     سعره بالمنتصف: الآن · أعلى · أدنى خلال الستين دقيقة (مع الوقت).
   • SPX: الهدف والإبطال يُسجَّل وقت لمس كلٍّ منهما ولا يُنهي التتبّع.
   ⚠ التتبّع في المتصفح: والصفحة مغلقة لا تُرصد الأسعار ⇒ علامة ⚠. */
const LSK="liq_ls2_"+U, LS_MAX_MIN=60, LS_GAP_MS=120000;
function nyDay(d){const s=((d&&d.ts_ny)||"").slice(0,10); if(s)return s;
 try{return new Date().toLocaleDateString("en-CA",{timeZone:"America/New_York"});}catch(e){return new Date().toDateString();}}
function ksaTime(mn){const m=(mn+7*60)%1440;return String(Math.floor(m/60)).padStart(2,"0")+":"+String(m%60).padStart(2,"0");}
function lsLoad(day){let o=null;try{o=JSON.parse(localStorage.getItem(LSK));}catch(e){}
 if(!o||o.day!==day||!Array.isArray(o.list))o={day:day,n:0,list:[]};return o;}
function lsSave(o){try{localStorage.setItem(LSK,JSON.stringify(o));}catch(e){}}
/* سعر العقد بالمنتصف من سلسلة اللقطة · null إن خرج السترايك من الجدول */
function lsMid(d,side,k){
 for(const t of (d.table||[])){ if(t.strike!==k)continue;
  const b=Number(side==="CALL"?t.call_bid:t.put_bid), a=Number(side==="CALL"?t.call_ask:t.put_ask);
  if(a>0&&b>0)return (a+b)/2; if(a>0)return a; return null;}
 return null;}
/* o = القرار المؤكَّد (لا الخام) · يُستدعى كل لقطة والجلسة مفتوحة */
function lsUpdate(d,o,nowMs){
 if(d.session!=="open"||!d.ny_time||d.spot==null)return null;
 const S=lsLoad(nyDay(d)), sp=d.spot, hm=d.ny_time.split(":").map(Number), mn=hm[0]*60+hm[1];
 for(const x of S.list){
  if(x.done)continue;
  if(mn-x.mn>=LS_MAX_MIN){x.done=true;continue;}
  if(x.lu&&nowMs-x.lu>LS_GAP_MS)x.gap=true;
  x.lu=nowMs;
  const dir=x.side==="PUT"?-1:1, mv=dir*(sp-x.sp);
  x.spNow=sp; x.mfe=Math.max(x.mfe||0,mv); x.mae=Math.min(x.mae||0,mv);
  if(!x.tgtT&&dir*(sp-x.tgt)>=0)x.tgtT=d.ny_time;
  if(!x.invT&&dir*(sp-x.inv)<=0)x.invT=d.ny_time;
  if(x.ck!=null&&x.c0>0){
   const m=lsMid(d,x.side,x.ck);
   if(m!=null){x.cNow=m;
    if(m>x.cHi){x.cHi=m;x.cHiT=d.ny_time;}
    if(m<x.cLo){x.cLo=m;x.cLoT=d.ny_time;}}
   else x.cOut=true;
  }
 }
 if(o&&o.side&&o.tgtP!=null&&o.invP!=null){
  const act=S.list.some(x=>!x.done&&x.side===o.side);
  if(!act){
   const c=pickContract(d,o.side), c0=c?lsMid(d,o.side,c.k):null;
   S.n=(S.n||0)+1;
   S.list.push({id:S.n,v:o.v,side:o.side,t:d.ny_time,tk:ksaTime(mn),mn:mn,sp:sp,tgt:o.tgtP,inv:o.invP,
     tgtN:o.tgtN||"",invN:o.invN||"",ck:c?c.k:null,ca:c?Number(c.ask):null,cv:c?c.v:null,csym:c?c.sym:null,
     c0:c0,cNow:c0,cHi:c0,cLo:c0,cHiT:d.ny_time,cLoT:d.ny_time,
     spNow:sp,mfe:0,mae:0,lu:nowMs,done:false});
   if(S.list.length>40)S.list=S.list.slice(-40);
  }
 }
 lsSave(S); lsBarsKick(S,nowMs); return S;
}
/* [v2.3] شموع الدقيقة من الخادم (Tradier) — كل 30 ثانية لكل قرار نشط.
   تسدّ ما فات والصفحة مغلقة: أعلى/أدنى العقد من الصفقات المنفَّذة فعلاً،
   ولمس الهدف والإبطال من شموع الأداة. تُدمج مع لقطات المتصفح (الأشد يفوز). */
const LS_BARS_MS=30000;
const hmMn=hm=>{const a=String(hm).split(":").map(Number);return a[0]*60+a[1];};
function lsMerge(x,js){
 const t0=x.mn,t1=x.mn+LS_MAX_MIN,inW=hm=>{const m=hmMn(hm);return m>=t0&&m<t1;};
 let nb=0;
 for(const b of (js.opt||[])){ if(!inW(b[0]))continue; nb++;
  if(x.cHi==null||b[1]>x.cHi){x.cHi=b[1];x.cHiT=b[0];}
  if(x.cLo==null||b[2]<x.cLo){x.cLo=b[2];x.cLoT=b[0];} }
 const dir=x.side==="PUT"?-1:1;
 for(const b of (js.und||[])){ if(!inW(b[0]))continue; nb++;
  const best=dir>0?b[1]:b[2], worst=dir>0?b[2]:b[1];
  if(dir*(best-x.tgt)>=0&&(!x.tgtT||hmMn(b[0])<hmMn(x.tgtT)))x.tgtT=b[0];
  if(dir*(worst-x.inv)<=0&&(!x.invT||hmMn(b[0])<hmMn(x.invT)))x.invT=b[0];
  x.mfe=Math.max(x.mfe||0,dir*(best-x.sp)); x.mae=Math.min(x.mae||0,dir*(worst-x.sp)); }
 if(nb){x.bOK=true;x.bN=(js.opt||[]).filter(b=>inW(b[0])).length;}
 return nb;
}
function lsBarsKick(S,nowMs){
 if(typeof fetch!=="function")return;
 for(const x of S.list){
  // المنتهي يُجلب مرة أخيرة واحدة (fin) — لساعة انتهت والصفحة مغلقة
  if(!x.csym||(x.done&&x.fin)||(x.bt&&nowMs-x.bt<LS_BARS_MS))continue;
  x.bt=nowMs; const id=x.id, day=S.day;
  lsSave(S);
  fetch(`/bars?opt=${encodeURIComponent(x.csym)}&und=${U}&start=${x.t}`).then(r=>r.json()).then(js=>{
   if(!js||!js.ok)return;
   const S2=lsLoad(day), y=S2.list.find(z=>z.id===id); if(!y)return;
   lsMerge(y,js); if(y.done)y.fin=true; lsSave(S2);
  }).catch(()=>{});
 }
}
function lsCard(x,mnNow){
 const big=x.sp>1000, f=v=>v.toFixed(big?1:2), sg=v=>(v>=0?"+":"−")+f(Math.abs(v));
 const pc=v=>(v>=x.c0?"+":"−")+Math.abs((v-x.c0)/x.c0*100).toFixed(1)+"%";
 const col=x.side==="PUT"?"var(--dn)":"var(--up)", dir=x.side==="PUT"?-1:1;
 const left=Math.max(0,LS_MAX_MIN-(mnNow-x.mn));
 let st, sb, sc;
 if(x.tgtT&&(!x.invT||x.tgtT<=x.invT)){st="تحقق الهدف ✓ "+x.tgtT;sb="rgba(45,212,160,.16)";sc="var(--up)";}
 else if(x.invT){st="أُبطل ✗ "+x.invT;sb="rgba(255,90,110,.16)";sc="var(--dn)";}
 else {st="جارٍ";sb="rgba(74,144,255,.18)";sc="#8ab6ff";}
 let h=`<div class="ls"><div class="lh"><b>قرار #${x.id} · <span style="color:${col}">${x.v}</span> ${x.t} NY · ${x.tk} KSA</b>`
  +`<span class="st" style="background:${sb};color:${sc}">${st}</span></div>`;
 if(x.ck!=null&&x.c0>0){
  h+=`<div>العقد <b>${x.side} ${x.ck}</b> · تداول ${K(x.cv)} · دخول $${x.c0.toFixed(2)} <span class="ln">(العرض $${x.ca.toFixed(2)})</span></div>`;
  h+=`<div>الآن <b>$${x.cNow.toFixed(2)} (${pc(x.cNow)})</b> · `
   +`<span style="color:var(--up)">أعلى $${x.cHi.toFixed(2)} (${pc(x.cHi)}) ${x.cHiT}</span> · `
   +`<span style="color:var(--dn)">أدنى $${x.cLo.toFixed(2)} (${pc(x.cLo)}) ${x.cLoT}</span></div>`;
  if(x.bOK)h+=`<div class="ln">الأعلى والأدنى يشملان شموع الدقيقة من Tradier (شموع العقد: ${x.bN||0})</div>`;
  else if(x.cOut)h+=`<div class="ln">⚠ السترايك خرج من السلسلة المعروضة لحظات — لم يُرصد سعره فيها</div>`;
 } else h+=`<div class="ln">لا عقد ≤ $${PICK_MAX_ASK.toFixed(2)} في هذا الاتجاه لحظة القرار</div>`;
 h+=`<div>SPX ${f(x.sp)} → <span style="color:var(--up)">الهدف ${x.tgtN} ${f(x.tgt)} (${sg(x.tgt-x.sp)})</span> · `
  +`<span style="color:var(--dn)">الإبطال ${f(x.inv)} (${sg(x.inv-x.sp)})</span></div>`;
 const mv=dir*(x.spNow-x.sp);
 h+=`<div class="ln">SPX الآن ${sg(mv)} نقطة في اتجاهه (أقصى ${sg(x.mfe||0)} · أسوأ ${sg(x.mae||0)}) · يُحذف بعد ${left} د</div>`;
 if(x.gap&&!x.bOK)h+=`<div class="ln">⚠ الصفحة كانت مغلقة جزءاً من المدة وشموع Tradier لم تصل بعد — الأعلى والأدنى قد لا يكونان كاملين</div>`;
 return h+`</div>`;
}
function lsPaint(S,d){
 const E=document.getElementById("vL"); if(!E)return;
 let mnNow=0; try{const hm=d.ny_time.split(":").map(Number);mnNow=hm[0]*60+hm[1];}catch(e){}
 const act=(S&&S.list||[]).filter(x=>!x.done&&mnNow-x.mn<LS_MAX_MIN&&mnNow>=x.mn);
 if(!act.length){E.innerHTML="";E.style.display="none";return;}
 E.innerHTML=act.slice().reverse().map(x=>lsCard(x,mnNow)).join(""); E.style.display="";
}
function paintVerdict(o,live,d,pending){
 const W=document.getElementById("vW"),Rr=document.getElementById("vR"),T=document.getElementById("vT");
 if(!live){W.textContent="—";W.style.color="var(--dim)";Rr.textContent="خارج الجلسة";T.innerHTML="";return;}
 W.textContent=o.v;W.style.color=o.c;Rr.textContent=o.why;
 let h="";
 if(o.tgt)h+=`<span style="color:var(--up)">${o.tgt}</span>`;
 if(o.inv)h+=`<span style="color:var(--dn)">${o.inv}</span>`;
 if(o.rr)h+=`<span style="color:${o.rr.endsWith("✓")?"var(--up)":"var(--wr)"}">${o.rr}</span>`;
 const c=o.side&&d?pickContract(d,o.side):null;
 if(c)h+=`<span style="color:#8ab6ff">مرشّح ${o.side} ${c.k} · $${Number(c.ask).toFixed(2)} · تداول ${K(c.v)}</span>`;
 if(pending)h+=`<span style="color:var(--dim)">تحوّل إلى ${pending.v} قيد التأكيد · ${pending.left}ث</span>`;
 T.innerHTML=h;
}
/* ═══ قوة الاتجاه — نقطة كل دقيقة، في المتصفح لكل أداة، تتصفّر يومياً ═══ */
const TSK="liq_ts_"+U;
function tsRecord(d,bull){
 if(bull==null||d.session!=="open"||!d.ny_time)return;
 let o=null;try{o=JSON.parse(localStorage.getItem(TSK));}catch(e){}
 const day=(d.ts_ny||"").slice(0,10)||new Date().toDateString();
 if(!o||o.day!==day)o={day:day,p:[]};
 const [h,m]=d.ny_time.split(":").map(Number), mn=h*60+m;
 const last=o.p[o.p.length-1];
 if(last&&last[0]===mn)last[1]=Math.round(bull);
 else o.p.push([mn,Math.round(bull)]);
 if(o.p.length>400)o.p=o.p.slice(-400);
 try{localStorage.setItem(TSK,JSON.stringify(o));}catch(e){}
}
function tsDraw(){
 const sv=document.getElementById("tsv"); if(!sv)return;
 let o=null;try{o=JSON.parse(localStorage.getItem(TSK));}catch(e){}
 // [v2.2] الخادم أولاً (سلسلة اليوم كاملة) ثم نقاط المتصفح لما ينقصه
 const mp=new Map();
 for(const p of ((o&&o.p)||[]))mp.set(p[0],p[1]);
 let srvN=0;
 try{const sv=SA.d;
  if(sv&&sv.series&&sv.underlying===U){for(const p of sv.series){mp.set(p[0],p[1]);srvN++;}}
 }catch(e){}
 const P=[...mp.entries()].sort((a,b)=>a[0]-b[0]), H=96, M=H/2;
 const X=mn=>Math.max(0,Math.min(390,mn-570)), Y=b=>H-4-(b/100)*(H-8);
 // شبكة: خط 50% + ساعات
 let h=`<defs><clipPath id="cU"><rect x="0" y="0" width="390" height="${Y(50)}"/></clipPath>
  <clipPath id="cD"><rect x="0" y="${Y(50)}" width="390" height="${H}"/></clipPath></defs>`;
 for(let t=600;t<960;t+=60)h+=`<line x1="${X(t)}" y1="0" x2="${X(t)}" y2="${H}" stroke="rgba(255,255,255,.05)"/>`;
 h+=`<line x1="0" y1="${Y(50)}" x2="390" y2="${Y(50)}" stroke="rgba(255,255,255,.22)" stroke-dasharray="4 4"/>`;
 // تنعيم: متوسط آخر 5 دقائق داخل كل مقطع متصل
 const segs=[];let cur=[];
 for(let i=0;i<P.length;i++){ if(i&&P[i][0]-P[i-1][0]>5){segs.push(cur);cur=[];} cur.push(P[i]); }
 if(cur.length)segs.push(cur);
 let lastPt=null;
 for(const sg of segs){
  const sm=sg.map((p,i)=>{const w=sg.slice(Math.max(0,i-4),i+1);return [p[0],w.reduce((a,q)=>a+q[1],0)/w.length];});
  if(sm.length===1){lastPt=sm[0];continue;}
  const line=sm.map(p=>X(p[0]).toFixed(1)+","+Y(p[1]).toFixed(1)).join(" ");
  const area=`${X(sm[0][0])},${Y(50)} ${line} ${X(sm[sm.length-1][0])},${Y(50)}`;
  h+=`<polygon points="${area}" fill="rgba(45,212,160,.28)" clip-path="url(#cU)"/>`;
  h+=`<polygon points="${area}" fill="rgba(255,92,114,.28)" clip-path="url(#cD)"/>`;
  h+=`<polyline points="${line}" fill="none" stroke="#2dd4a0" stroke-width="2" stroke-linejoin="round" clip-path="url(#cU)"/>`;
  h+=`<polyline points="${line}" fill="none" stroke="#ff5c72" stroke-width="2" stroke-linejoin="round" clip-path="url(#cD)"/>`;
  lastPt=sm[sm.length-1];
 }
 if(lastPt){
  const up=lastPt[1]>=50, c=up?"#2dd4a0":"#ff5c72", x=X(lastPt[0]), y=Y(lastPt[1]);
  h+=`<circle cx="${x}" cy="${y}" r="3.5" fill="${c}" stroke="#0b111b" stroke-width="1.5"/>`;
 }
 sv.innerHTML=h;
 const n=document.getElementById("tsn");
 if(n){
  if(lastPt){const v=Math.round(lastPt[1]);n.innerHTML=`<b style="color:${v>=50?"var(--up)":"var(--dn)"}">${v>=50?"صعودي "+v:"هبوطي "+(100-v)}%</b> · ${P.length} دقيقة${srvN?" · الخادم":" · المتصفح"}`;}
  else n.textContent="يمتلئ والصفحة مفتوحة";
 }
}
function markNearest(L,sp){
 let up=null,dn=null;
 for(const x of L){ if(x.px)continue;
  if(x.p>sp&&(!up||x.p<up.p))up=x;
  if(x.p<sp&&(!dn||x.p>dn.p))dn=x; }
 if(up)up.tag="مقاومة مباشرة"; if(dn)dn.tag="دعم مباشر";
 return L;
}
function buildLadder(d){
 const L=[], P0=d.pos||{}, sp=d.spot;
 if(d.em){L.push({p:d.em.hi,n:"حدّ اليوم ↑",t:"صمد 86–93%",c:"var(--dim)"});
          L.push({p:d.em.lo,n:"حدّ اليوم ↓",t:"صمد 86–93%",c:"var(--dim)"});}
 if(P0.call_wall)L.push({p:P0.call_wall,n:"جدار غاما CALL",t:"غير مختبَر",c:"var(--up)"});
 if(P0.put_wall)L.push({p:P0.put_wall,n:"جدار غاما PUT",t:"غير مختبَر",c:"var(--dn)"});
 if(P0.flip)L.push({p:P0.flip,n:"الانقلاب",t:sp>=P0.flip?"فوقه: كبح":"تحته: تضخيم",c:"var(--wr)"});
 if(d.vwap)L.push({p:d.vwap.vwap_und,n:"VWAP",t:"من SPY",c:"var(--ac)"});
 L.push({p:sp,n:"السعر",t:"",c:"",px:true});
 return L.filter(x=>x.p!=null&&isFinite(x.p)).sort((a,b)=>b.p-a.p);
}
const F1=v=>(v>0?"+":"")+v.toFixed(Math.abs(v)<10?2:1);
function renderNow(d){
 const el=document.getElementById("now"); if(!el)return;
 el.style.display="";
 const live=d.session==="open";
 el.style.opacity=live?"":".6";
 document.getElementById("nts").textContent=live?d.ny_time+" NY":"خارج الجلسة · يعمل 09:30–16:00 NY";
 // ① المسيطر — خارج الجلسة: آخر قراءة محفوظة بلا تحديث
 let a, src="المتصفح";
 if(live){
  a=aggRead(aggUpdate(d,Date.now()));
  let sv=null; try{sv=srvAgg();}catch(e){}
  if(sv&&(sv.cov_sec/60)>=(a.covMin||0)){
   a=aggRead({cb:sv.cb,cs:sv.cs,pb:sv.pb,ps:sv.ps,u:sv.u,cov:sv.cov_sec*1000});
   src="الخادم";
  }
 }
 else{const r={cb:0,cs:0,pb:0,ps:0,u:0,cov:0};
  for(const e of AG.ev){for(const k of ["cb","cs","pb","ps","u"])r[k]+=e[k];r.cov+=(e.dt||5000);}
  r.cov=Math.min(r.cov,AG_WIN);a=aggRead(r);
  if(a.ready)a.lead="آخر قراءة: "+a.lead;}
 const B=document.getElementById("agB"),S=document.getElementById("agS"),V=document.getElementById("agV");
 const cvT=" · مغطّى "+(a.covMin||0).toFixed(1)+" من 5 د"+(live?" · "+src:"");
 if(!a.ready){
  B.style.width=S.style.width="50%";B.textContent="صعودي —";S.textContent="هبوطي —";
  V.style.color="var(--dim)";V.textContent=live?"جارٍ البناء… "+K(a.cls)+" عقد مصنّف"+cvT:"لا قراءة محفوظة — يبدأ مع الافتتاح";
  for(const k of ["CB","CS","PB","PS"])document.getElementById("ag"+k).textContent="—";
  document.getElementById("agF").textContent=live?"جارٍ البناء…"+cvT:"";
 }else{
  const bp=Math.round(a.bullPct);
  B.style.width=Math.max(12,Math.min(88,bp))+"%";S.style.width=Math.max(12,Math.min(88,100-bp))+"%";
  B.textContent="صعودي "+bp+"%";S.textContent="هبوطي "+(100-bp)+"%";
  const bu=Math.round(a.bullPct), dirTxt=bu>=55?"ضغط صعودي "+bu+"%":bu<=45?"ضغط هبوطي "+(100-bu)+"%":"متوازن";
  V.style.color=bu>=55?"var(--up)":bu<=45?"var(--dn)":"var(--dim)";
  V.textContent=a.lead+" يقودون · "+dirTxt;
  document.getElementById("agCB").textContent=Math.round(a.pct.cb)+"%";
  document.getElementById("agPB").textContent=Math.round(a.pct.pb)+"%";
  document.getElementById("agPS").textContent=Math.round(a.pct.ps)+"%";
  document.getElementById("agCS").textContent=Math.round(a.pct.cs)+"%";
  document.getElementById("agF").textContent=K(a.cls)+" عقد مصنّف من "+K(a.all)+" ("+Math.round(a.cover)+"%)"+cvT;
 }
 // ⓪ القرار
 try{
  const bu=a.ready?a.bullPct:null;
  const raw=decide(d,bu,live?flowHyst(bu):null);
  const sv=live?stableVerdict(raw,Date.now()):{o:raw,pending:null};
  paintVerdict(sv.o,live,d,sv.pending);
  if(live)vsSave();
  // [v2.3] آخر إشارة — من القرار المؤكَّد فقط · خارج الجلسة تُعرض آخر حالة محفوظة
  try{lsPaint(live?lsUpdate(d,sv.o,Date.now()):lsLoad(nyDay(d)),d);
  }catch(e){console.log("ls",e);}
 }catch(e){console.log("verdict",e);}
 try{if(live&&a.ready)tsRecord(d,a.bullPct);tsDraw();}catch(e){console.log("ts",e);}
 // ② بوابة VWAP
 const g=document.getElementById("gsec"), w=d.vwap;
 if(!w){g.style.display="none";}else{
  const on=(id,ok,lbl)=>{const e=document.getElementById(id);
   e.style.background=ok?"rgba(45,212,160,.16)":"rgba(255,181,71,.15)";
   e.style.color=ok?"var(--up)":"var(--wr)";e.textContent=lbl+" "+(ok?"مسموح":"انتظر");};
  on("gC",w.call_ok,"CALL");on("gP",w.put_ok,"PUT");
  const R=1.2, pos=v=>(Math.max(-R,Math.min(R,v))+R)/(2*R)*100;
  const z=document.getElementById("gZ");
  z.style.right=pos(-w.gate)+"%"; z.style.width=(pos(w.gate)-pos(-w.gate))+"%";
  document.getElementById("gM").style.right=pos(w.dist_spy)+"%";
  document.getElementById("gL").textContent="−$"+R.toFixed(2);
  const pts=U==="SPX"?" · "+F1(w.dist_und)+" نقطة SPX":"";
  document.getElementById("gT").textContent="SPY "+(w.dist_spy>=0?"فوق":"تحت")+" VWAP بـ $"+Math.abs(w.dist_spy).toFixed(2)+pts;
  document.getElementById("gR").textContent="+$"+R.toFixed(2);
 }
 // ③ السلّم
 const L=markNearest(buildLadder(d),d.spot);
 document.getElementById("lsrc").textContent=d.em?("حدّا اليوم من "+d.em.src+" "+d.em.iv):"";
 document.getElementById("lad").innerHTML=L.map(x=>x.px
  ?`<div class="lr px"><b>${x.p.toFixed(2)}</b><s>${U} الآن</s><em></em></div>`
  :`<div class="lr"><b style="color:${x.c}">${x.p.toFixed(x.p>1000?0:2)}</b><s>${x.n}${x.tag?`<i style="background:${x.p>d.spot?"rgba(255,181,71,.18);color:var(--wr)":"rgba(255,92,114,.16);color:var(--dn)"}">${x.tag}</i>`:" · "+x.t}</s><em>${F1(x.p-d.spot)}</em></div>`).join("");
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
  // ══════ [v1.6] تدفّق آخر 15 دقيقة — 8 سترايكات فوق و8 تحت ══════
  renderFlow(d).catch(e=>console.log("flow",e));
  try{renderPos(d);}catch(e){console.log("pos",e);}
  try{renderNow(d);}catch(e){console.log("now",e);}
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
