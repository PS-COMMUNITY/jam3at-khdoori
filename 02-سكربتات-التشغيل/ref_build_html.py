# -*- coding: utf-8 -*-
"""توليد نسخة HTML التفاعلية ذاتية الاحتواء من ملف DOCX المُنتَج.
التحويلات الذكية:
 - صناديق التظليل (1x1 جداول ملوّنة) → صناديق CSS
 - المراسي S*/EX*/H* → عناصر <details> مخفية قابلة للفتح
 - روابط 🔒 و 💡 و ↑ → أزرار فتح/إخفاء وتنقل حقيقية (JS محلي بلا إنترنت)
 - الصور → Base64 مدمجة (ملف واحد مستقل تماماً)
"""
import os, re, base64, html
from docx import Document
from docx.oxml.ns import qn

SRC = '/tmp/my-project/ref_out/المرجع-التفاعلي-الدوائر-الكهربائية.docx'
OUT = '/tmp/my-project/ref_out/المرجع-التفاعلي-الدوائر-الكهربائية.html'

doc = Document(SRC)
body = doc.element.body

# خريطة العلاقات → ملفات الوسائط
rels = {}
for rid, rel in doc.part.rels.items():
    if 'image' in rel.reltype:
        rels[rid] = rel.target_ref  # مثل word/media/image1.png

BOXFILL = {
    'FFF2CC': 'law', 'E2EFDA': 'why', 'FBE4E4': 'warn', 'EDF3FA': 'step',
    'F7F1E3': 'act', 'EEF3FB': 'hint', 'F2F2F2': 'sum', 'EAF4EA': 'answer',
    'F2F2F2 ': 'sum', 'FFF9E6': 'answer', 'D8E8D0': 'thead',
}

def get_fill(tbl):
    try:
        tc = tbl.tbl.rows[0].cells[0]._tc
        shd = tc.find(qn('w:tcPr') + '/' + qn('w:shd'))
        # بحث يدوي
        tcPr = tc.find(qn('w:tcPr'))
        if tcPr is not None:
            sh = tcPr.find(qn('w:shd'))
            if sh is not None:
                return sh.get(qn('w:fill'))
    except Exception:
        pass
    return None

def text_of_p(p_el):
    """النص الكامل لفقرة مع تحويل مقاطع LRE إلى رمز مارك-أب لاحق."""
    out = []
    for child in p_el.iter():
        tag = child.tag
        if tag == qn('w:t'):
            t = child.text or ''
            out.append(('t', t))
        elif tag == qn('w:tab'):
            out.append(('t', ' '))
    # إعادة بناء مع تقسيم LRE/PDF
    s = ''.join(x[1] for x in out)
    return s

def runs_html(p_el, links_map=None):
    """إخراج HTML للفقرات مع حماية مقاطع LTR (LRE…PDF) وروابط."""
    parts = []
    for node in p_el.iter():
        if node.tag == qn('w:hyperlink'):
            anchor = node.get(qn('w:anchor'))
            txt = ''.join(t.text or '' for t in node.iter(qn('w:t')))
            if anchor:
                parts.append(('link', anchor, txt))
            continue
        if node.tag == qn('w:t'):
            # قد يتبع لقطة داخل hyperlink — نتجاهل لأننا التقيناه أعلاه؟ iter يمر على الأبناء أيضاً
            pass
    # بناء أمان: مرّ على الأبناء المباشرين فقط للفقرة، وتبع hyperlinks
    result = []
    def walk(el):
        for child in el:
            if child.tag == qn('w:r'):
                t = ''.join(x.text or '' for x in child.iter(qn('w:t')))
                if t:
                    result.append(('run', t))
            elif child.tag == qn('w:hyperlink'):
                anchor = child.get(qn('w:anchor'))
                txt = ''.join(x.text or '' for x in child.iter(qn('w:t')))
                result.append(('link', anchor or '', txt))
            elif child.tag == qn('w:bookmarkStart'):
                result.append(('bm', child.get(qn('w:name'))))
    walk(p_el)
    return result

def esc(s):
    return html.escape(s, quote=False)

def fmt_text(s):
    """تقسيم LRE…PDF إلى spans لاتينية، والباقي عربي."""
    s = s.replace('\u202A', '\x01').replace('\u202C', '\x02')
    segs = re.split(r'(\x01[^\x02]*\x02)', s)
    out = []
    for seg in segs:
        if not seg:
            continue
        if seg.startswith('\x01'):
            inner = seg[1:-1]
            out.append(f'<span dir="ltr" class="eq">{esc(inner)}</span>')
        else:
            out.append(esc(seg))
    return ''.join(out).strip()

# ---------------------------------------------------------------- المرور على العناصر
body_children = list(body)
html_parts = []
open_details_stack = []  # قائمة عناصر details المفتوحة حالياً بالبناء

DETAIL_ANCHORS = re.compile(r'^(S|EX|H)[0-9A-Za-z\-]*$')

def close_details():
    if open_details_stack:
        html_parts.append('</div></details>')
        open_details_stack.pop()

for el in body_children:
    tag = el.tag
    if tag == qn('w:p'):
        p_el = el
        items = runs_html(p_el)
        # صور داخل الفقرة؟
        img_rids = [blip.get(qn('r:embed')) for blip in p_el.iter(qn('a:blip'))]
        has_image = bool(img_rids)
        # page break?
        br_page = any(br.get(qn('w:type')) == 'page' for br in p_el.iter(qn('w:br')))
        text_all = ''.join(x[1] for x in items if x[0] == 'run')
        # class الفقرة من الخصائص
        is_bold = any(r.find(qn('w:rPr')) is not None and r.find(qn('w:rPr')).find(qn('w:b')) is not None
                      for r in p_el.iter(qn('w:r')))
        szs = [int(r.find(qn('w:rPr')).find(qn('w:sz')).get(qn('w:val')))
               for r in p_el.iter(qn('w:r'))
               if r.find(qn('w:rPr')) is not None and r.find(qn('w:rPr')).find(qn('w:sz')) is not None]
        maxsz = max(szs) / 2 if szs else 13
        alignment = 'right'
        pPr = p_el.find(qn('w:pPr'))
        if pPr is not None:
            jc = pPr.find(qn('w:jc'))
            if jc is not None:
                alignment = jc.get(qn('w:val'))
        # bookmarkStart names
        bms = [b.get(qn('w:name')) for b in p_el.iter(qn('w:bookmarkStart'))]

        if br_page:
            html_parts.append('<hr class="pb">')
            continue

        # إغلاق details عند رابط العودة
        links = [x for x in items if x[0] == 'link']
        if links and open_details_stack:
            first_txt = links[0][2]
            if first_txt.startswith('↑') or first_txt.startswith('عودة'):
                # أغلق details الحالي ثم أكمل (الرابط نفسه يصبح زر عودة داخل summary)
                pass

        # مراسي details: أول مرساة S*/EX*/H* تفتح details
        detail_bm = next((b for b in bms if DETAIL_ANCHORS.match(b)), None)
        if detail_bm and not open_details_stack:
            label = 'الحل الكامل' if detail_bm.startswith(('S', 'EX')) else 'التلميح'
            html_parts.append(f'<details class="sol" id="{detail_bm}"><summary>🔒 {label} — اضغط للإظهار أو للإخفاء</summary><div>')
            open_details_stack.append(detail_bm)
        elif detail_bm and open_details_stack:
            # مرساة داخل details (تلميح داخل حل) — علامة فقط
            html_parts.append(f'<span id="{detail_bm}"></span>')

        if has_image:
            for rid in img_rids:
                if rid in rels:
                    media_path = doc.part.related_parts[rid].blob
                    b64 = base64.b64encode(media_path).decode()
                    ext = rels[rid].split('.')[-1].lower()
                    html_parts.append(f'<div class="imgwrap"><img src="data:image/{ext};base64,{b64}" alt="صورة مصدر مدمجة"></div>')
            continue

        # رابط عودة = نهاية details
        if links and open_details_stack and links[0][2].startswith('↑'):
            link_el = links[0]
            html_parts.append(f'<p class="back"><a href="#{link_el[1]}" onclick="closeDetail(event,this)">{esc(link_el[2])}</a></p>')
            close_details()
            continue

        # نص الفقرة
        rendered = []
        for kind, *rest in items:
            if kind == 'run':
                rendered.append(fmt_text(rest[0]))
            elif kind == 'link':
                anchor, txt = rest
                txt_s = txt
                if txt_s.startswith('🔒') or txt_s.startswith('💡'):
                    target = anchor
                    rendered.append(f'<button class="openbtn" onclick="openDetail(\'{target}\')">{esc(txt_s)}</button>')
                else:
                    rendered.append(f'<a class="ilink" href="#{anchor}">{esc(txt_s)}</a>')
        joined = ''.join(rendered).strip()
        if not joined:
            continue
        # العناوين
        if maxsz >= 16:
            html_parts.append(f'<h1>{joined}</h1>')
        elif maxsz >= 13.5:
            html_parts.append(f'<h2>{joined}</h2>')
        else:
            cls = 'center' if alignment == 'center' else ''
            html_parts.append(f'<p class="{cls}">{joined}</p>')

    elif tag == qn('w:tbl'):
        from docx.table import Table
        tbl = Table(el, doc)
        fill = get_fill(tbl)
        nrows = len(tbl.rows)
        ncols = len(tbl.rows[0].cells) if nrows else 0
        if ncols == 1 and nrows == 1:
            fillc = fill or ''
            cls = BOXFILL.get(fillc, 'sum')
            # صناديق الإجابات الخضراء EAF4EA = إجابة نهائية
            lines = []
            for p_el in tbl.rows[0].cells[0]._tc.iter(qn('w:p')):
                t = ''.join(x.text or '' for x in p_el.iter(qn('w:t')))
                if t.strip():
                    lines.append(fmt_text(t))
            content = '<br>'.join(lines) if lines else ''
            if cls in ('law', 'why', 'warn', 'step', 'act', 'hint', 'sum'):
                html_parts.append(f'<div class="box {cls}">{content}</div>')
            else:
                html_parts.append(f'<div class="answer">{content}</div>')
        else:
            # جدول عادي
            rows_html = []
            for ri, row in enumerate(tbl.rows):
                cells = []
                for cell in row.cells:
                    txts = []
                    for p_el in cell._tc.iter(qn('w:p')):
                        t = ''.join(x.text or '' for x in p_el.iter(qn('w:t')))
                        if t.strip():
                            txts.append(fmt_text(t))
                    cells.append(' '.join(txts))
                rows_html.append(cells)
            thead = ''
            body_rows = rows_html
            # أول صف مظلل D8E8D0 → رأس
            try:
                tcPr = tbl.rows[0].cells[0]._tc.find(qn('w:tcPr'))
                sh = tcPr.find(qn('w:shd')) if tcPr is not None else None
                if sh is not None and (sh.get(qn('w:fill')) or '').upper() == 'D8E8D0':
                    thead = '<tr>' + ''.join(f'<th>{c}</th>' for c in rows_html[0]) + '</tr>'
                    body_rows = rows_html[1:]
            except Exception:
                pass
            trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in body_rows)
            html_parts.append(f'<table>{thead}{trs}</table>')

close_details()

CSS = """
:root{--green:#1d6f42;--amber:#B47E00;--ink:#222}
*{box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,'DejaVu Sans',Arial,sans-serif;direction:rtl;background:#faf9f6;
     color:var(--ink);margin:0;padding:0 0 60px;line-height:1.75;font-size:15.5px}
main{max-width:900px;margin:0 auto;padding:18px 22px}
h1{color:var(--green);border-bottom:3px solid var(--green);padding-bottom:6px;margin-top:36px;font-size:1.45em}
h2{color:#204020;margin-top:26px;font-size:1.18em;border-right:4px solid var(--amber);padding-right:9px}
p{margin:7px 0}
p.center{text-align:center}
.eq{font-family:'Cambria','Times New Roman',serif;color:#8B4513;font-weight:600;direction:ltr;
    background:#f6f2ea;padding:0 4px;border-radius:3px;white-space:nowrap;display:inline-block}
.box{padding:11px 14px;border-radius:8px;margin:11px 0;border:1px solid rgba(0,0,0,.14);font-size:.97em}
.box.law{background:#FFF2CC;border-color:#E0C878;font-weight:500}
.box.why{background:#E2EFDA;border-color:#A9C79B}
.box.warn{background:#FBE4E4;border-color:#E0A0A0}
.box.step{background:#EDF3FA;border-color:#A8C0E0}
.box.act{background:#F7F1E3;border-color:#D8C8A0}
.box.hint{background:#EEF3FB;border-color:#B8C8E8}
.box.sum{background:#F2F2F2;border-color:#C8C8C8}
.answer{background:#EAF4EA;border:2px solid var(--green);border-radius:8px;padding:10px 14px;
        margin:11px 0;text-align:center;font-weight:600}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:.92em;background:#fff}
th,td{border:1px solid #999;padding:6px 8px;vertical-align:top}
th{background:#D8E8D0;color:#143014}
tr:nth-child(even) td{background:#FAFAF7}
.imgwrap{text-align:center;margin:14px 0}
.imgwrap img{max-width:100%;border:1px solid #ddd;border-radius:6px;box-shadow:0 1px 5px rgba(0,0,0,.12)}
details.sol{background:#F5FBF6;border:2px dashed var(--green);border-radius:9px;margin:14px 0;padding:0}
details.sol>summary{cursor:pointer;padding:10px 14px;font-weight:700;color:var(--green);
                    background:#E8F3EB;border-radius:8px;list-style:none}
details.sol>summary::before{content:"▸ ";display:inline-block;transition:.2s}
details.sol[open]>summary::before{transform:rotate(90deg)}
details.sol>div{padding:6px 16px 14px}
.openbtn{background:#EAF2FF;color:#1a5fb4;border:1.5px solid #1a5fb4;border-radius:20px;
         padding:3px 13px;cursor:pointer;font-size:.9em;font-family:inherit;margin:2px 3px;font-weight:700}
.openbtn:hover{background:#1a5fb4;color:#fff}
a.ilink{color:#1a5fb4;text-decoration:none;font-weight:700}
a.ilink:hover{text-decoration:underline}
p.back a{color:#8B4513;font-weight:700;text-decoration:none;border:1px solid #B47E00;
         background:#FFF6E8;padding:3px 12px;border-radius:6px;display:inline-block}
hr.pb{border:none;border-top:2px dashed #bbb;margin:42px 0 30px}
header.top{background:var(--green);color:#fff;padding:26px 18px 22px;text-align:center}
header.top h0{font-size:1.7em;font-weight:800}
header.top p{margin:4px 0;color:#EAF4EA}
nav.toc{background:#fff;border:1px solid #ddd;border-radius:10px;padding:14px 20px;margin:18px auto;max-width:900px}
nav.toc a{color:var(--green);text-decoration:none;display:block;padding:2.5px 0;font-weight:600}
nav.toc a:hover{color:var(--amber)}
"""

JS = """
function openDetail(id){
  var d = document.getElementById(id);
  if(d && d.tagName === 'DETAILS'){ d.open = true; d.scrollIntoView({behavior:'smooth', block:'center'}); }
}
function closeDetail(ev, a){
  var d = a.closest('details');
  if(d){ d.open = false; }
}
"""

# فهرس التنقل
TOC = """
<header class="top">
  <h0 style="font-size:1.7em;font-weight:800;margin:0">المرجع التفاعلي — الدوائر الكهربائية 03081071</h0>
  <p>الوحدات الست (حتى صفحة 150) — نسخة تفاعلية ذاتية الاحتواء تعمل دون إنترنت</p>
  <p>🔒 الحلول والتلميحات مخفية افتراضياً — اضغط الروابط لفتحها وإغلاقها</p>
</header>
<nav class="toc">
  <a href="#CH00">الفصل 0 — كيف تستخدم هذا المرجع</a>
  <a href="#CHCALC">الفصل أ — الآلة الحاسبة fx-991ES PLUS</a>
  <a href="#CHMETHOD">الفصل ب — منهجية «كيف أبدأ حل المسألة؟»</a>
  <a href="#CHU1">الوحدة 1 — الوحدات والبادئات وعناصر الدائرة</a>
  <a href="#CHU2">الوحدة 2 — أوم والمقاومة والقدرة والطاقة</a>
  <a href="#CHU3">الوحدة 3 — توالي/توازي/مركب والمقسمان</a>
  <a href="#CHU4">الوحدة 4 — مصادر الجهد والتيار</a>
  <a href="#CHU5">الوحدة 5 — كيرشوف والنظريات (قلب المادة)</a>
  <a href="#CHU6">الوحدة 6 — كرامر والعقد والحلقات</a>
  <a href="#CHHW">الفصل ج — الواجب الأول محلولاً</a>
  <a href="#CHEXAM">الفصل د — نموذج الامتحان التدريبي</a>
  <a href="#CHSOL">قسم الحلول الكاملة (الكل مخفي حتى تفتحه)</a>
  <a href="#CHLAW">الفصل هـ — ملخص القوانين</a>
  <a href="#CHAUDIT">الفصل و — سجل تدقيق الصور</a>
  <a href="#CHSRC">الفصل ز — دليل المصادر</a>
</nav>
"""

page = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>المرجع التفاعلي — الدوائر الكهربائية 03081071</title>
<style>{CSS}</style>
</head>
<body>
<main>
{TOC}
{''.join(html_parts)}
<p style="text-align:center;color:#777;font-size:.9em;margin-top:40px">
نسخة تفاعلية ذاتية الاحتواء — الصور مدمجة Base64 والحلول مخفية بالضغط — تعمل دون إنترنت — «وَقُل رَّبِّ زِدْنِي عِلْمًا»</p>
</main>
<script>{JS}</script>
</body>
</html>"""

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(page)
print('saved', OUT, os.path.getsize(OUT) // 1024, 'KB')
print('details blocks:', page.count('<details'))
print('images:', page.count('data:image'))
