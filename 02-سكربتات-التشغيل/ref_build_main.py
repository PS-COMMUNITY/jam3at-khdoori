# -*- coding: utf-8 -*-
"""بناء المرجع التفاعلي الشامل — DOCX واحد يجمع كل الفصول."""
import sys, os
sys.path.insert(0, '/home/z/my-project/scripts')
from ref_helpers import *
from ref_content_a import cover, how_to_use, calc_chapter, methodology, unit1, unit2, unit3
from ref_content_b import unit4, unit5, unit6
from ref_content_c import hw_chapter, exam_chapter, solutions_chapter, laws_chapter, audit_chapter, sources_chapter

OUT = '/tmp/my-project/ref_out'
os.makedirs(OUT, exist_ok=True)

doc = setup_doc()

cover(doc)
how_to_use(doc)
calc_chapter(doc)
methodology(doc)
unit1(doc)
unit2(doc)
unit3(doc)
unit4(doc)
unit5(doc)
unit6(doc)
hw_chapter(doc)
exam_chapter(doc)
solutions_chapter(doc)
laws_chapter(doc)
audit_chapter(doc)
sources_chapter(doc)

path = os.path.join(OUT, 'المرجع-التفاعلي-الدوائر-الكهربائية.docx')
doc.save(path)
print('saved', path, os.path.getsize(path) // 1024, 'KB')

# إحصاء سريع
from docx import Document
d = Document(path)
print('paragraphs:', len(d.paragraphs), '| tables:', len(d.tables))
import zipfile
z = zipfile.ZipFile(path)
media = [n for n in z.namelist() if n.startswith('word/media/')]
print('embedded images:', len(media))
