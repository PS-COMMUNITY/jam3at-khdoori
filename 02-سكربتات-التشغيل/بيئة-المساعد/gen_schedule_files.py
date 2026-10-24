# -*- coding: utf-8 -*-
"""مولّد ملفات جدول تاريخ المقررات — الفصل الأول PTUK"""
import os, html

BASE = "/home/z/my-project/فصل_اول_تنظيم"

def page(title, teacher, meta, deadlines, sections, bullets, color):
    d = ""
    if deadlines:
        rows = "".join(
            f"<tr><td>{html.escape(x[0])}</td><td>{html.escape(x[1])}</td>"
            f"<td><span class='b {x[2]}'>{x[3]}</span></td></tr>"
            for x in deadlines)
        d = f"""
        <h2>📌 المواعيد المهمة</h2>
        <table><thead><tr><th>التاريخ</th><th>الحدث</th><th>الحالة</th></tr></thead>
        <tbody>{rows}</tbody></table>"""
    s = ""
    for sec_title, items in sections:
        lis = "".join(
            f"<li><span class='b {i[1]}'>{i[2]}</span> {html.escape(i[0])}</li>"
            if len(i) == 3 else f"<li>{html.escape(i)}</li>"
            for i in items)
        s += f"<div class='sec'><h3>{html.escape(sec_title)}</h3><ul>{lis}</ul></div>"
    n = ""
    if bullets:
        n = "<h2>📝 حالة المقرر الآن</h2><ul>" + "".join(
            f"<li>{html.escape(x)}</li>" for x in bullets) + "</ul>"
    return f"""<!DOCTYPE html>
<html dir="rtl" lang="ar"><head><meta charset="UTF-8">
<title>{html.escape(title)} — جدول تاريخ المقرر</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:'Segoe UI',Tahoma,Arial,sans-serif;margin:0;background:#f4f5f7;color:#1d2733;line-height:1.9}}
.wrap{{max-width:900px;margin:0 auto;padding:24px 16px}}
header{{background:{color};color:#fff;border-radius:14px;padding:26px 28px;margin-bottom:22px}}
header h1{{margin:0 0 6px;font-size:26px}}
header .m{{opacity:.95;font-size:14px}}
h2{{color:{color};border-right:5px solid {color};padding-right:10px;font-size:20px;margin:28px 0 12px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.08)}}
th{{background:{color};color:#fff;padding:10px;font-size:14px;text-align:right}}
td{{padding:10px;border-top:1px solid #e7eaf0;font-size:14px}}
.b{{display:inline-block;padding:1px 10px;border-radius:20px;font-size:12px;font-weight:600;white-space:nowrap}}
.done{{background:#e6f6ec;color:#147a3d}} .open{{background:#fff4dc;color:#8a5b00}}
.late{{background:#fdeaea;color:#a12626}} .info{{background:#e8f0fd;color:#1c4fa1}}
.warn{{background:#f3e8fd;color:#6b2fa0}}
.sec{{background:#fff;border-radius:10px;padding:14px 18px;margin-bottom:12px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
.sec h3{{margin:0 0 8px;font-size:16px;color:{color}}}
ul{{margin:0;padding-right:20px}} li{{font-size:14px;margin:3px 0}}
.foot{{text-align:center;color:#8a93a3;font-size:12px;margin-top:26px}}
@media print{{body{{background:#fff}} .wrap{{max-width:100%}} .sec,table{{box-shadow:none;border:1px solid #ddd}}}}
</style></head><body><div class="wrap">
<header><h1>📘 {html.escape(title)}</h1>
<div class="m">👨‍🏫 {html.escape(teacher)} &nbsp;|&nbsp; {html.escape(meta)}</div></header>
{d}{s}{n}
<div class="foot">أُعدّ تلقائياً من بيانات نظام المودل — جامعة فلسطين التقنية خضوري 🎓</div>
</div></body></html>"""

OK = ("تم ✅", "done"); WAIT = ("بانتظار ⏳", "warn"); ACT = ("مفتوح 📌", "open")
INFO = ("معلومة", "info"); LATE = ("مغلق ⛔", "late")

courses = []

# ============ 1. الدوائر الكهربائية ============
courses.append(("01_الدوائر_الكهربائية", "الدوائر الكهربائية — الشعبة 1 (نظري)",
    "أ. مصطفى عبد الرحيم", "معرف المقرر: 40579", "#0e7490",
    [], [
    "المحاضرات 1-6 (تم تحميلها ودراسة الصفحات 1-53)",
    "تجهيز ما بعد الصفحة 53 — ملف جاهز",
    "شرح ملفات PDF للمحاضرات 1-6 — مؤجل",
    "لا يوجد أي واجب أو اختبار مفتوح حالياً",
    "متابعة أسبوعية للمقرر لاصطياد أي واجب جديد فور نزوله",
    ]))

# ============ 2. الرياضيات التقنية ============
courses.append(("02_الرياضيات_التقنية", "الرياضيات التقنية — الشعبة 1 (نظري)",
    "أ. نداء حمدان", "معرف المقرر: 41870", "#7c3aed",
    [], [
    "حل واجب المعادلة كامل مع الشرح التفصيلي — منتهٍ",
    "تحويل الحل إلى PDF عربي RTL — قيد الإعداد",
    "لا يوجد أي واجب أو اختبار مفتوح حالياً (10 ملفات + رابطان)",
    "متابعة أسبوعية للمقرر",
    ]))

# ============ 3. اللغة العربية ============
courses.append(("03_اللغة_العربية", "اللغة العربية — الشعبة 1 (نظري)",
    "لجنة تدريس اللغة العربية", "معرف المقرر: 42715", "#b45309",
    [
    ("20/9", "الواجب الأول (دبلوم الصيفي 2026)", LATE[1], "مغلق"),
    ("—", "الواجب الثاني (دبلوم الصيفي 2026)", LATE[1], "مغلق"),
    ], [
    "واجبان قديمان من الفصل الصيفي 2026 تركهما المعلم بالمقرر — انتهت مهلتهما (66 و53 يوماً) والتسليم مغلق نهائياً",
    "لا تأثير عليك إطلاقاً — واجبات دفعة سابقة",
    "19 غرفة شات (Chat) = حضور الحصص المباشرة",
    "لو ذكر المعلم الواجبين بالقاعة اسأله وهنبلّيك",
    ]))

# ============ 4. اللغة الإنجليزية ============
eng_sections = [
("📅 الأسبوع 1 — 12 إلى 18 سبتمبر", [
    ("Unit 1: صفحات 14-16 + قواعد الماضي البسيط Past Simple", INFO[1], "درس"),
    ("ملف الوحدة 2 + مصطلحات P.15 و P.16", INFO[1], "درس"),
    ("✅ خُذ Unit Two Quiz يوم 18/9 (3 دقائق و36 ثانية)", OK[1], "اختبار"),
]),
("📅 الأسبوع 2 — 19 إلى 25 سبتمبر", [
    ("اجتماع أونلاين + درس Coincidences 2C+2D", INFO[1], "درس"),
    ("قواعد الماضي المستمر Past Continuous + مصطلحات P.18 حتى P.20", INFO[1], "درس"),
]),
("📅 الأسبوع 3 — 26 سبتمبر إلى 2 أكتوبر", [
    ("مراجعة الوحدة 2 + مفتاح الإجابات P.21", INFO[1], "درس"),
    ("✅ خُذ Mock Quiz يوم 1/10 مساءً (اختبار تجريبي بلا علامات)", OK[1], "تجريبي"),
    ("✅ نسخة الميدترم من Unit Two Quiz: النتيجة 8/8 = 100%", OK[1], "اختبار"),
]),
("📅 الأسبوع الحالي — 3 إلى 9 أكتوبر", [
    ("✅ خُذ First Quiz on Wednesday يوم 4/10 — 10/10 مطابق للمفتاح الرسمي", OK[1], "اختبار"),
    ("📝 واجب Unit 3 A (من 3 علامات) — يفتح 27/10 الساعة 10 مساءً", ACT[1], "واجب"),
    ("درس Unit 3A صفحات 22+23 + مصطلحات P.23", INFO[1], "درس"),
]),
("📅 الأسبوع القادم — 10 إلى 16 أكتوبر", [
    ("مفردات Unit 3: Get Qualified + دروس 3B و 3D (صفحات 25-29)", INFO[1], "درس"),
    ("مراجعة الوحدة الثالثة", INFO[1], "مراجعة"),
]),
("📅 17 إلى 23 أكتوبر", [
    ("مفردات الوحدة 4 + دروس 4A و 4B (صفحات 31-32)", INFO[1], "درس"),
]),
("📦 قسم مادة الامتحان النصفي (Midterm Material)", [
    ("نسخ مكررة من الاختبارين + First Quiz (انتهت جميعها)", INFO[1], "مؤرشف"),
    ("شرح طبيعة الامتحان النصفي + العلامة من 55 (نصفي + أعمال فصلية)", INFO[1], "مهم"),
    ("تمارين إضافية: Present Continuous/Simple + Nor/So + have to", INFO[1], "تمارين"),
]),
("📦 قسم النهائي", [
    ("Unit 5 + Second Assignment (واجب ثانٍ قادم — راقبوه)", WAIT[1], "قادم"),
    ("الامتحان النهائي يغطي 4 وحدات + مراجعات نهائية", INFO[1], "قادم"),
]),
("📝 ملاحظات خاصة", [
    ("العلامة الكلية للمقرر من 55: النصفي + الأعمال الفصلية", INFO[1], "مهم"),
    ("درجات الاختبارات مخفية عن الطلاب — يطلعها المعلم لاحقاً", INFO[1], "معلومة"),
    ("نفس بنك أسئلة الوحدة 2 جاء في First Quiz — ذاكر المفاتيح المحفوظة عندك", INFO[1], "نصيحة"),
]),
]
courses.append(("04_اللغة_الإنجليزية", "اللغة الإنجليزية — الشعبة 2 (نظري)",
    "اسم المعلم مخفي بالنظام", "معرف المقرر: 41463", "#1d6f42",
    [
    ("18/9", "Unit Two Quiz (النسخة الأصلية)", OK[1], "أُدّي"),
    ("1/10", "Mock Quiz (تجريبي بلا علامات)", OK[1], "أُدّي"),
    ("4/10", "First Quiz on Wednesday — الحقيقي", OK[1], "100%"),
    ("27/10 10م", "فتح واجب Unit 3 A", WAIT[1], "قادم"),
    ("3/11 10م", "آخر مهلة واجب Unit 3 A (3 علامات!)", ACT[1], "مفتوح"),
    ], eng_sections))

# ============ 5. الإلكترونيات ============
courses.append(("05_الالكترونيات", "الالكترونيات — الشعبة 1 (نظري)",
    "أ. لينا عموص", "معرف المقرر: 42231", "#c2410c",
    [], [
    "38 ملفاً و10 روابط و4 صفحات دراسية",
    "صفحتان حدّيتان تحددان نطاق الامتحان النهائي: «من هنا يبدأ الامتحان النهائي» و«إلى هنا الامتحان النهائي»",
    "لا يوجد أي واجب أو اختبار مفتوح حالياً",
    "متابعة أسبوعية للمقرر",
    ]))

# ============ 6. أخلاقيات المهنة ============
courses.append(("06_أخلاقيات_المهنة", "أخلاقيات المهنة — الشعبة 1 (نظري)",
    "أ. رغد سنيوره", "معرف المقرر: 41748", "#9d174d",
    [], [
    "مقرر خفيف: ملف واحد فقط + منتدى إعلانات",
    "لا يوجد أي واجب أو اختبار حالياً",
    "متابعة أسبوعية",
    ]))

# ============ 7. المشغل الهندسي ============
courses.append(("07_المشغل_الهندسي", "المشغل الهندسي — الشعبة 1 (عملي)",
    "أ. يزن النابلسي", "معرف المقرر: 39773", "#3f6212",
    [], [
    "المقرر فاضي حالياً: منتدى إعلانات فقط",
    "راقبوه — المقررات العملية تنشط فجأة",
    ]))

# ============ 8. مشغل التمديدات ============
courses.append(("08_مشغل_التمديدات", "مشغل التمديدات الكهربائية — الشعبة 1 (عملي)",
    "أ. علي محمد", "معرف المقرر: 40889", "#1e40af",
    [
    ("29/9", "تسليم وظيفة 1 أونلاين (PDF مضغوط)", OK[1], "مسلّم"),
    ("5/10 12ص", "المهلة الرسمية — التسليم قبلها بـ5 أيام ✅", OK[1], "قبلها"),
    ("5/10", "تسليم الورقة اليدوية في المحاضرة", WAIT[1], "غداً"),
    ], [
    "✅ وظيفة 1 مسلّمة إلكترونياً ومستوفية المتطلبات الثلاثة: خط يد + الاسم على كل ورقة + قبل اللقاء بيوم",
    "📝 السؤال 4 (رسم 3 لمبات 3 مفاتيح): رأي المعلم الفني — النيوترال يبقى خطاً مستمراً بلا مفاتيح، وكل مفتاح بين لمبته والنيوترال",
    "الواجب الأصلي واجب 1.docx محفوظ بهذا المجلد",
    "الأسئلة الأربعة: فرق التوالي/التوازي + أهمية الفاحص + استخدامات الأفوميتر + رسم الدائرة",
    ]))

# ============ كتابة الملفات ============
for folder, title, teacher, meta, color, deadlines, sections in courses:
    p = os.path.join(BASE, folder)
    os.makedirs(p, exist_ok=True)
    if sections and isinstance(sections[0], tuple) and len(sections[0]) == 2:
        secs, bullets = sections, None
    else:
        secs, bullets = [], sections
    content = page(title, teacher, meta, deadlines, secs, bullets, color)
    with open(os.path.join(p, "جدول_تاريخ_المقرر.html"), "w", encoding="utf-8") as f:
        f.write(content)
    print("OK:", folder)

# ============ الفهرس الرئيسي ============
cal = "".join(
    f"<tr><td>{html.escape(x[0])}</td><td>{html.escape(x[1])}</td><td>{html.escape(x[2])}</td>"
    f"<td><span class='b {x[3]}'>{x[4]}</span></td></tr>"
    for x in [
    ("الاثنين 5/10", "تسليم ورقة وظيفة 1 اليدوية في محاضرة التمديدات (س4 مصحح)", "مشغل التمديدات", WAIT[1], "غداً"),
    ("الثلاثاء 27/10 - 10م", "فتح واجب Unit 3 A", "اللغة الإنجليزية", WAIT[1], "قادم"),
    ("الثلاثاء 3/11 - 10م", "آخر مهلة واجب Unit 3 A — 3 علامات", "اللغة الإنجليزية", ACT[1], "مفتوح"),
    ("موعود لاحقاً", "الامتحان النصفي لكل المواد (الإنجليزي: العلامة من 55)", "كل المقررات", INFO[1], "راقب"),
    ("نهاية الفصل", "الامتحان النهائي (الإنجليزي: يغطي 4 وحدات)", "كل المقررات", INFO[1], "لاحقاً"),
    ])
idx_courses = "".join(
    f"<tr><td>{html.escape(c[1])}</td><td>{html.escape(c[2])}</td>"
    f"<td>جدول_تاريخ_المقرر.html</td></tr>" for c in courses)
idx = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar"><head><meta charset="UTF-8">
<title>الفصل الأول — الفهرس والجدول الرئيسي</title>
<style>
*{{box-sizing:border-box}}
body{{font-family:'Segoe UI',Tahoma,Arial,sans-serif;margin:0;background:#0f172a;color:#e2e8f0;line-height:1.9}}
.wrap{{max-width:960px;margin:0 auto;padding:28px 16px}}
header{{background:linear-gradient(135deg,#1e3a8a,#1d4ed8);border-radius:16px;padding:30px;text-align:center;margin-bottom:24px}}
header h1{{margin:0;font-size:28px;color:#fff}}
header p{{margin:8px 0 0;color:#bfdbfe}}
h2{{color:#93c5fd;border-right:5px solid #2563eb;padding-right:12px;font-size:20px;margin:30px 0 14px}}
table{{width:100%;border-collapse:collapse;background:#1e293b;border-radius:12px;overflow:hidden;margin-bottom:8px}}
th{{background:#2563eb;color:#fff;padding:11px;font-size:14px;text-align:right}}
td{{padding:11px;border-top:1px solid #334155;font-size:14px}}
.b{{display:inline-block;padding:1px 10px;border-radius:20px;font-size:12px;font-weight:600;white-space:nowrap}}
.done{{background:#14532d;color:#86efac}} .open{{background:#78350f;color:#fcd34d}}
.late{{background:#7f1d1d;color:#fca5a5}} .info{{background:#1e3a8a;color:#bfdbfe}}
.warn{{background:#581c87;color:#d8b4fe}}
ol{{background:#1e293b;border-radius:12px;padding:20px 40px;margin:0}} li{{margin:8px 0;font-size:14px}}
.foot{{text-align:center;color:#64748b;font-size:12px;margin-top:26px}}
@media print{{body{{background:#fff;color:#111}} table,ol{{background:#fff;color:#111}}}}
</style></head><body><div class="wrap">
<header><h1>🎓 جامعة خضوري نحو المستقبل — السنة الأولى / الفصل الأول</h1>
<p>الفهرس الرئيسي والجدول الزمني الشامل — الطالب: محمد عادل محمد العقيلي</p></header>

<h2>🗓️ التقويم الشامل لكل المقررات</h2>
<table><thead><tr><th>التاريخ</th><th>الحدث</th><th>المقرر</th><th>الحالة</th></tr></thead>
<tbody>{cal}</tbody></table>

<h2>📁 مجلدات المقررات الثمانية</h2>
<table><thead><tr><th>المقرر</th><th>المعلم</th><th>الملف داخل المجلد</th></tr></thead>
<tbody>{idx_courses}</tbody></table>

<h2>✅ خطوات الترتيب الصحيح للتخزين</h2>
<ol>
<li>افتح مجلد <b>جامعة خضوري نحو المستقبل ← السنة الأولى ← الفصل الأول</b></li>
<li>ضع ملف <b>جدول_تاريخ_المقرر.html</b> داخل مجلد كل مساق بنفس اسم المجلد هنا (01 إلى 08)</li>
<li>المساقات بأسماء مختلفة عندك؟ انسخ الملف لأقرب مساق مطابق بالاسم — المهم يوصل لكل مساق جدوله</li>
<li>رتّب ملفات كل مساق: المحاضرات (بالأرقام 01، 02، 03...) ثم الواجبات ثم المراجع</li>
<li>افتح أي جدول بمتصفح كروم — ويمكن طباعته PDF مباشرة (Ctrl+P)</li>
<li>حدّث الجداول عند نزول واجب جديد — أو بلّغني وأنا أحدثها لك</li>
</ol>

<div class="foot">أُعدّ تلقائياً من بيانات نظام المودل الرسمي — محدّث بتاريخ 4/10/2026 🎓</div>
</div></body></html>"""
with open(os.path.join(BASE, "اقرأني_الفهرس_والجدول_الرئيسي.html"), "w", encoding="utf-8") as f:
    f.write(idx)
print("OK: index")
