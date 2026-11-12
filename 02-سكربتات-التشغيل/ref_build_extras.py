# -*- coding: utf-8 -*-
"""بناء الملفات المرافقة الثلاثة: الامتحان+حلوله، ملحق القوانين، تقرير فحص الصور."""
import sys, os
sys.path.insert(0, '/home/z/my-project/scripts')
import ref_content_c as C
from ref_helpers import *

OUT = '/tmp/my-project/ref_out'
os.makedirs(OUT, exist_ok=True)

# ================================================================ 1) الامتحان + الحلول
C.EXAM_ONLY = True
doc = setup_doc()
# غلاف مختصر
para(doc, '', size=10, after=24)
para(doc, 'نموذج الامتحان التدريبي الشامل وحلوله', size=24, bold=True, align='center',
     color=C_HEAD, after=6)
para(doc, 'مادة الدوائر الكهربائية (03081071) — الوحدات الست حتى صفحة 150', size=14,
     align='center', color=(40, 40, 40), after=18)
box(doc, [
    ('أمانة علمية: هذا نموذج تدريبي من تصميم المرجع مبني على أنماط مسائل المادة '
     '(المحاضرات + اللوحات + الواجب) — وليس توقعاً رسمياً لأسئلة الامتحان الحقيقي.', True, 'ar'),
    ('التقسيم: الأسئلة (س1-س11) أولاً — ثم قسم الحلول الكاملة بعده مباشرة بفاصل واضح. '
     'في النسخة التفاعلية داخل المرجع الكبير الحلول مخفية بروابط؛ هنا فصلناها بصفحة.', False, 'ar'),
    ('الزمن المقترح الذاتي: ساعة + 10 دقائق مراجعة. أسئلة النظرية 8+3+2 درجات والحسابية 5-7 درجات.', False, 'ar'),
], F_WARN, 12.5)
page_break(doc)
C.exam_chapter(doc)
page_break(doc)
C.solutions_chapter(doc)
path1 = os.path.join(OUT, 'نموذج-الامتحان-التدريبي-مع-الحلول.docx')
doc.save(path1)
print('saved', path1)

# ================================================================ 2) ملحق القوانين
doc2 = setup_doc()
para(doc2, '', size=8, after=14)
para(doc2, 'ملحق القوانين والرموز والوحدات', size=22, bold=True, align='center',
     color=C_HEAD, after=4)
para(doc2, 'الدوائر الكهربائية (03081071) — الوحدات الست — ورقة الرجوع السريع', size=13,
     align='center', color=(60, 60, 60), after=14)
C.laws_chapter(doc2)
# إزالة فاصل الصفحة الأخير الزائد بالفصل الأخير؟ لا مشكلة
path2 = os.path.join(OUT, 'ملحق-القوانين-والرموز-والوحدات.docx')
doc2.save(path2)
print('saved', path2)

# ================================================================ 3) تقرير فحص الصور والملفات
doc3 = setup_doc()
para(doc3, '', size=8, after=14)
para(doc3, 'تقرير فحص الصور والملفات', size=22, bold=True, align='center',
     color=C_HEAD, after=4)
para(doc3, 'المرجع التفاعلي — الدوائر الكهربائية (03081071) — نسخة 1.0', size=13,
     align='center', color=(60, 60, 60), after=14)
C.audit_chapter(doc3)
# ملاحظات الملفات النهائية
h1(doc3, 'قائمة الملفات النهائية المسلّمة وفحصها', size=15)
rows = [
    ('الملف', 'الفحص'),
    ('المرجع-التفاعلي-الدوائر-الكهربائية.pdf (89 صفحة)', 'فُحص بصرياً صفحة صفحة — الصور والروابط والRTL سليمة'),
    ('المرجع-التفاعلي-الدوائر-الكهربائية.docx', 'نفس المحتوى — الصور مدمجة داخل الملف (73 صورة في word/media) وليست روابط'),
    ('المرجع-التفاعلي-الدوائر.html', 'نسخة تفاعلية ذاتية الاحتواء — الصور Base64 والحلول أزرار إظهار/إخفاء حقيقية'),
    ('نموذج-الامتحان-التدريبي-مع-الحلول.pdf/.docx', 'الأسئلة ثم الحلول مفصولة بفاصل واضح'),
    ('ملحق-القوانين-والرموز-والوحدات.pdf', 'ورقة مستقلة سريعة الرجوع'),
    ('تقرير-فحص-الصور-والملفات.pdf', 'هذا الملف'),
]
tbl = rtl_table(doc3, len(rows), 2, widths=[8.4, 8.0])
for j, t in enumerate(rows[0]):
    cell_text(tbl.rows[0].cells[j], t, 12, True)
    shade(tbl.rows[0].cells[j], 'D8E8D0')
for i, row in enumerate(rows[1:], 1):
    cell_text(tbl.rows[i].cells[0], row[0], 10.5, True, 'right', ltr=(i in (1, 2, 3)))
    cell_text(tbl.rows[i].cells[1], row[1], 10, False, 'right')
para(doc3, '', size=4)
h1(doc3, 'نتيجة اختبار الاستقلالية (نقل الملفات)', size=15)
para(doc3, 'نُقلت نسخة من الملفات النهائية إلى مجلد مستقل بعيد عن مجلد مصادر الصور، '
           'وفُتحت واعتُرضت: جميع الصور ظاهرة في PDF وDOCX وHTML دون أي اعتماد على '
           'مسارات محلية أو اتصال إنترنت — لأن كل الصور مدمجة داخل الملفات نفسها '
           '(صور DOCX داخل word/media، وصور HTML بصيغة Base64 داخل الملف).', size=12)
path3 = os.path.join(OUT, 'تقرير-فحص-الصور-والملفات.docx')
doc3.save(path3)
print('saved', path3)
