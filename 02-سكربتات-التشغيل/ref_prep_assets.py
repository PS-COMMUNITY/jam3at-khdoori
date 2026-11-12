# -*- coding: utf-8 -*-
"""تجهيز أصول الصور للمرجع التفاعلي: لوحات مختارة + صفحات الواجب والحل + صفحات الكتاب."""
import os, shutil, subprocess
from PIL import Image, ImageEnhance

BOARD_DIR = '/home/z/transfer/work-repo/السنة الاولى/الفصل الاول/3081071-الدوائر الكهربائية/صور-اللوح-الكاملة-82-لوحة-1211'
UPLOAD = '/home/z/my-project/upload'
MOODLE = '/home/z/transfer/work-repo/السنة الاولى/الفصل الاول/10-مودل-تنزيلات-كاملة-2410/الدوائر الكهربائية'
OUT = '/tmp/my-project/ref_assets/img'
os.makedirs(OUT, exist_ok=True)

# ---- اللوحات المختارة (رقم → مفتاح إنجليزي) ----
BOARDS = {
    'b01': 'لوحة-01.jpg',   # kWh=3600kJ — تحويلات الطاقة (و1/و2)
    'b05': 'لوحة-05.jpg',   # الشحنة + دارة أوم بالأميتر والفولتميتر (و1)
    'b06': 'لوحة-06.jpg',   # مثلث أوم + الميل dv/di (و2)
    'b10': 'لوحة-10.jpg',   # مثال المصباح/السخان الكامل 484/44.32/4.96 (و2)
    'b13': 'لوحة-13.jpg',   # اشتقاق مقسم الجهد + مثال 30V (و3)
    'b14': 'لوحة-14.jpg',   # التوازي واشتقاق مقسم التيار (و3)
    'b17': 'لوحة-17.jpg',   # مقسم التيار بدارة (و3)
    'b34': 'لوحة-34.jpg',   # المسألة الشاملة Vxy=14.5V (و3)
    'b44': 'لوحة-44.jpg',   # كيرشوف العقدة ΣI=0 (و5)
    'b51': 'لوحة-51.jpg',   # قواعد كيرشوف ومعادلات الحلقات الثلاث (و5/و6)
    'b59': 'لوحة-59.jpg',   # المسألة الذهبية كيرشوف + Mode→5→2 (و5)
    'b65': 'لوحة-65.jpg',   # التراكب الرقمي 2.33+1.65 (و5)
    'b52': 'لوحة-52.jpg',   # التراكب الرقمي 6V/12V (و5)
    'b53': 'لوحة-53.jpg',   # التراكب بمصدر تيار 515mA (و5)
    'b62': 'لوحة-62.jpg',   # ثيفنين الذهبية Vth=16V Rth=2Ω (و5)
    'b57': 'لوحة-57.jpg',   # ثيفنين مثال الكتاب Vth=7V Rth=53Ω (و5)
    'b63': 'لوحة-63.jpg',   # نورتون 0.2A/50Ω (و5)
    'b64': 'لوحة-64.jpg',   # ميلمان VEQ=8.89V (و5)
    'b66': 'لوحة-66.jpg',   # صيغ مثلث↔نجمة (و5)
    'b73': 'لوحة-73.jpg',   # جسر ويتستون محلول 1.25V/25mA (و5)
    'b68': 'لوحة-68.jpg',   # كرامر 2×2 Δ=85 (و6)
    'b71': 'لوحة-71.jpg',   # كرامر 3×3 Δ=−118 (و6)
    'b67': 'لوحة-67.jpg',   # العقد G·V=I وV₁=6V (و6)
    'b74': 'لوحة-74.jpg',   # معادلات الحلقات العامة 3 حلقات (و6)
    'b49': 'لوحة-49.jpg',   # حلقات شبكة 3 معادلات مرقمة (و6)
    'b81': 'لوحة-81.jpg',   # صورة آلة الحاسبة CASIO (قسم الحاسبة)
}

MAXW = 1600

def prep(src, dst, maxw=MAXW, quality=82, brighten=None):
    im = Image.open(src).convert('RGB')
    if brighten:
        im = ImageEnhance.Brightness(im).enhance(brighten)
        im = ImageEnhance.Contrast(im).enhance(1.12)
    if im.width > maxw:
        r = maxw / im.width
        im = im.resize((maxw, int(im.height * r)), Image.LANCZOS)
    im.save(dst, 'JPEG', quality=quality)
    return os.path.getsize(dst) // 1024

total = 0
for key, fname in BOARDS.items():
    src = os.path.join(BOARD_DIR, fname)
    kb = prep(src, os.path.join(OUT, f'{key}.jpg'))
    total += kb
    print(f'{key}: {fname} -> {kb} KB')

# ---- صفحات العروض الممسوحة من الكتاب (وحدة 4) ----
for s, dst in [('/tmp/my-project/ref_assets/slides/l9-2.png', 'book_l9_p2.jpg'),
               ('/tmp/my-project/ref_assets/slides/l10-2.png', 'book_l10_p2.jpg')]:
    kb = prep(s, os.path.join(OUT, dst), maxw=1400, quality=85)
    total += kb
    print(dst, kb, 'KB')

# ---- صفحة الواجب (السؤال الأصلي) ----
hw_src = os.path.join(UPLOAD, 'الواجب الأول.pdf')
if not os.path.exists(hw_src):
    hw_src = '/home/z/transfer/work-repo/السنة الاولى/الفصل الاول/3081071-الدوائر الكهربائية/الواجب الأول - نسخة الدكتور.pdf'
subprocess.run(['pdftoppm', '-png', '-r', '110', '-f', '1', '-l', '1', hw_src,
                '/tmp/my-project/ref_assets/_hwp'], check=True)
kb = prep('/tmp/my-project/ref_assets/_hwp-1.png', os.path.join(OUT, 'hw_page.jpg'), maxw=1300, quality=88)
print('hw_page', kb, 'KB')
total += kb

# ---- صفحات الحل اليدوي (تسليم 80283) ----
subprocess.run(['pdftoppm', '-png', '-r', '100', os.path.join(UPLOAD, '80283.pdf'),
                '/tmp/my-project/ref_assets/_hw'], check=True)
for i in range(1, 4):
    s = f'/tmp/my-project/ref_assets/_hw-{i}.png'
    if os.path.exists(s):
        kb = prep(s, os.path.join(OUT, f'sol_p{i}.jpg'), maxw=1200, quality=85)
        total += kb
        print(f'sol_p{i}', kb, 'KB')

print('TOTAL KB:', total)
print('files:', len(os.listdir(OUT)))
