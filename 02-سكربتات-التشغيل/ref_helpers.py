# -*- coding: utf-8 -*-
"""أدوات بناء المستند العربي RTL للمرجع التفاعلي — مبنية على خط الأنابيب المجرّب.
يشمل: bidi كامل، معادلات ⟪⟫ كـruns لاتينية معزولة بLRE/PDF، صناديق مظللة،
مراسي bookmark وروابط داخلية للحلول المخفية، تضمين صور اللوح مع التوثيق."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AR_FONT = 'Arial'
IMG_D = '/tmp/my-project/ref_assets/diagrams'
IMG_B = '/tmp/my-project/ref_assets/img'

C_LAW = (139, 94, 0)      # بني للقوانين
C_EQ = (139, 69, 19)      # بني للمعادلات داخل النص
C_HEAD = (20, 90, 40)
C_HINT = (26, 95, 180)

F_LAW = 'FFF2CC'   # أصفر — قوانين
F_WHY = 'E2EFDA'   # أخضر — ليش
F_WARN = 'FBE4E4'  # أحمر — فخاخ
F_STEP = 'EDF3FA'  # أزرق — خطوات
F_ACT = 'F7F1E3'   # بيج — نشاطات
F_HINT = 'EEF3FB'  # أزرق فاتح — تلميحات
F_SUM = 'F2F2F2'   # رمادي — ملخصات


def _set_rtl(p, align='right'):
    pPr = p._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi')
    bidi.set(qn('w:val'), '1')
    pPr.append(bidi)
    p.alignment = {'right': WD_ALIGN_PARAGRAPH.RIGHT,
                   'center': WD_ALIGN_PARAGRAPH.CENTER,
                   'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
                   'left': WD_ALIGN_PARAGRAPH.LEFT}[align]


def _style_run(r, size, bold, color=None, rtl=True, font=None):
    r.font.size = Pt(size)
    r.bold = bold
    r.font.name = font or AR_FONT
    rPr = r._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:cs'), font or AR_FONT)
    szCs = OxmlElement('w:szCs')
    szCs.set(qn('w:val'), str(int(size * 2)))
    rPr.append(szCs)
    if bold:
        bCs = OxmlElement('w:bCs')
        bCs.set(qn('w:val'), '1')
        rPr.append(bCs)
    if rtl:
        rtl_el = OxmlElement('w:rtl')
        rtl_el.set(qn('w:val'), '1')
        rPr.append(rtl_el)
    if color:
        r.font.color.rgb = RGBColor(*color)


def para(doc, text='', size=13, bold=False, align='right', color=None,
         after=5, before=0, ltr=False):
    p = doc.add_paragraph()
    if ltr:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if align == 'center' else \
            WD_ALIGN_PARAGRAPH.RIGHT if align == 'right' else WD_ALIGN_PARAGRAPH.JUSTIFY
    else:
        _set_rtl(p, align)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if text:
        r = p.add_run(text)
        _style_run(r, size, bold, color)
    return p


def rich(doc, text, size=13, align='right', after=5, before=0, bold=False):
    """نص عربي فيه أجزاء لاتينية/معادلات بين ⟪ ⟫ تُدرج LTR بلون بني مع LRE/PDF."""
    p = doc.add_paragraph()
    _set_rtl(p, align)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    import re
    parts = re.split(r'(⟪[^⟫]*⟫)', text)
    for part in parts:
        if not part:
            continue
        if part.startswith('⟪'):
            inner = part[1:-1]
            r = p.add_run('\u202A' + inner + '\u202C')
            _style_run(r, size, bold, C_EQ, rtl=False, font='Cambria')
        else:
            r = p.add_run(part)
            _style_run(r, size, bold)
    return p


def eqp(doc, text, size=13, bold=True, box=False, color=None, after=3, before=2, fill=None):
    """معادلة لاتينية مستقلة LTR في سطر مركزي (خارج سياق RTL تماماً)."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    r = p.add_run('\u202A' + text + '\u202C')
    _style_run(r, size, bold, color or C_EQ, rtl=False, font='Cambria')
    if box or fill:
        pPr = p._p.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        for side in ('top', 'left', 'bottom', 'right'):
            el = OxmlElement(f'w:{side}')
            el.set(qn('w:val'), 'single')
            el.set(qn('w:sz'), '10')
            el.set(qn('w:space'), '3')
            el.set(qn('w:color'), '1d6f42' if box else 'B0B0B0')
            pBdr.append(el)
        pPr.append(pBdr)
        if fill:
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:fill'), fill)
            pPr.append(shd)
    return p


def _box_table(doc, fill, width_cm=16.4):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    cell.width = Cm(width_cm)
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), fill)
    tcPr.append(shd)
    return tbl, cell


def _cell_paras(cell, lines, size=12.5):
    """lines: list of (text, bold, kind) — kind: ar/eq/ric"""
    cell.paragraphs[0].text = ''
    first = True
    for item in lines:
        text, bold, kind = item
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        if kind == 'eq':
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run('\u202A' + text + '\u202C')
            _style_run(r, size + 0.5, True, C_EQ, rtl=False, font='Cambria')
        elif kind == 'ric':
            import re
            _set_rtl(p, 'right')
            for part in re.split(r'(⟪[^⟫]*⟫)', text):
                if not part:
                    continue
                if part.startswith('⟪'):
                    rr = p.add_run('\u202A' + part[1:-1] + '\u202C')
                    _style_run(rr, size, bold, C_EQ, rtl=False, font='Cambria')
                else:
                    rr = p.add_run(part)
                    _style_run(rr, size, bold)
        else:
            _set_rtl(p, 'right')
            r = p.add_run(text)
            _style_run(r, size, bold)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(1)


def box(doc, lines, fill=F_LAW, size=12.5, after=6):
    """صندوق مظلل عام. lines: [(text, bold, kind)]"""
    tbl, cell = _box_table(doc, fill)
    _cell_paras(cell, lines, size)
    para(doc, '', size=4, after=after)
    return tbl


def law_box(doc, title, formula, extras=None):
    """صندوق القانون الأصفر: العنوان + المعادلة + أسطر اختيارية."""
    lines = [(title, True, 'ar'), (formula, True, 'eq')]
    if extras:
        for e in extras:
            lines.append((e, False, 'ric'))
    box(doc, lines, F_LAW, 12.5)


def why_box(doc, text):
    box(doc, [(text, False, 'ric')], F_WHY, 12)


def warn_box(doc, text):
    box(doc, [(text, False, 'ric')], F_WARN, 12)


def step_box(doc, text):
    box(doc, [(text, False, 'ric')], F_STEP, 12)


def act_box(doc, icon, text):
    """صندوق النشاط: دفتر/كتاب/حاسبة/لوح."""
    box(doc, [(f'{icon} {text}', False, 'ric')], F_ACT, 12)


def h1(doc, text, size=17, color=C_HEAD, before=10, after=6):
    return para(doc, text, size=size, bold=True, align='right', color=color,
                after=after, before=before)


def h2(doc, text, size=14, color=(40, 40, 40)):
    return para(doc, text, size=size, bold=True, align='right', color=color,
                after=4, before=6)


def board_img(doc, key, caption, look=None, width=15.2):
    """تضمين صورة مصدر (لوح/كتاب/واجب) مع التوثيق وإرشاد النظر."""
    path = os.path.join(IMG_B, key + '.jpg')
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(path, width=Cm(width))
    para(doc, caption, size=10.5, align='center', color=(90, 90, 90), after=2)
    if look:
        box(doc, [(f'👁 ماذا تبحث عنه في هذه الصورة: {look}', False, 'ric')], F_SUM, 11)


def diagram(doc, name, caption, width=13.5):
    path = os.path.join(IMG_D, name + '.png')
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(path, width=Cm(width))
    para(doc, caption, size=10.5, align='center', color=(90, 90, 90), after=4)


def rtl_table(doc, rows, cols, widths=None):
    tbl = doc.add_table(rows=rows, cols=cols)
    tbl.style = 'Table Grid'
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    bidi = OxmlElement('w:bidiVisual')
    tblPr.append(bidi)
    if widths:
        for i, w in enumerate(widths):
            for row in tbl.rows:
                row.cells[i].width = Cm(w)
    return tbl


def cell_text(cell, text, size=12, bold=False, align='center', color=None, ltr=False):
    cell.paragraphs[0].text = ''
    p = cell.paragraphs[0]
    if ltr:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        _set_rtl(p, align)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(1)
    r = p.add_run(text)
    _style_run(r, size, bold, color)


def shade(cell, hexfill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), hexfill)
    tcPr.append(shd)


# ---------------------------------------------------------------- مراسي وروابط
_bm_id = [100]


def bookmark(doc, name):
    _bm_id[0] += 1
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    s = OxmlElement('w:bookmarkStart')
    s.set(qn('w:id'), str(_bm_id[0]))
    s.set(qn('w:name'), name)
    e = OxmlElement('w:bookmarkEnd')
    e.set(qn('w:id'), str(_bm_id[0]))
    r = p.add_run(' ')
    _style_run(r, 2, False)
    p._p.insert(0, s)
    p._p.append(e)
    return p


def link_p(doc, anchor, text, align='center', size=12, color=(26, 95, 180)):
    """فقرة تحتوي رابطاً داخلياً (مرساة) — تعمل في Word وتتحول لرابط PDF."""
    p = doc.add_paragraph()
    _set_rtl(p, align)
    p.paragraph_format.space_after = Pt(3)
    h = OxmlElement('w:hyperlink')
    h.set(qn('w:anchor'), anchor)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:cs'), AR_FONT)
    rPr.append(rFonts)
    col = OxmlElement('w:color')
    col.set(qn('w:val'), '%02X%02X%02X' % color)
    rPr.append(col)
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), str(int(size * 2)))
    rPr.append(sz)
    szCs = OxmlElement('w:szCs')
    szCs.set(qn('w:val'), str(int(size * 2)))
    rPr.append(szCs)
    b = OxmlElement('w:b')
    rPr.append(b)
    bCs = OxmlElement('w:bCs')
    rPr.append(bCs)
    rtl_el = OxmlElement('w:rtl')
    rtl_el.set(qn('w:val'), '1')
    rPr.append(rtl_el)
    r.append(rPr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    h.append(r)
    p._p.append(h)
    return p


def link_run(doc, anchor, text, size=12, color=(26, 95, 180), after=3):
    p = link_p(doc, anchor, text, size=size, color=color)
    return p


def setup_doc(landscape=False):
    doc = Document()
    for section in doc.sections:
        if landscape:
            section.page_width = Cm(29.7)
            section.page_height = Cm(21.0)
        else:
            section.page_width = Cm(21.0)
            section.page_height = Cm(29.7)
        section.left_margin = Cm(1.7)
        section.right_margin = Cm(1.7)
        section.top_margin = Cm(1.5)
        section.bottom_margin = Cm(1.5)
    style = doc.styles['Normal']
    style.font.name = AR_FONT
    style.font.size = Pt(13)
    return doc


def page_break(doc):
    from docx.enum.text import WD_BREAK
    p = doc.add_paragraph()
    r = p.add_run()
    r.add_break(WD_BREAK.PAGE)
    return p


def exercise(doc, tag, title, body_lines, diagram_name=None, diagram_caption=None,
             hints=None, sol_anchor=None, board_keys=None):
    """تدريب منظم: مرساة للسؤال + عنوان مرقّم + نص + رسم اختياري + روابط تلميح/حل مخفي."""
    bookmark(doc, 'Q' + tag.replace('-', ''))
    h2(doc, f'📋 {tag} — {title}', size=13.5)
    for ln in body_lines:
        rich(doc, ln, size=12.5)
    if diagram_name:
        diagram(doc, diagram_name, diagram_caption or '', 11.5)
    if board_keys:
        for bk, cap in board_keys:
            board_img(doc, bk, cap, width=14.0)
    if hints:
        for ha, hl in hints:
            link_run(doc, ha, f'💡 {hl}', size=11.5)
    if sol_anchor:
        link_run(doc, sol_anchor, '🔒 افتح الحل الكامل (في قسم الحلول آخر الملف)', size=12)
    para(doc, '', size=4)
