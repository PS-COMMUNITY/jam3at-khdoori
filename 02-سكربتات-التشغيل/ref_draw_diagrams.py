# -*- coding: utf-8 -*-
"""
مكتبة رسم الدوائر الكهربائية النظيفة للمرجع التفاعلي — نسخة 2.
قواعد صارمة:
 1) بلا أي نص عربي داخل الرسم (يُضعف RTL في matplotlib) — كل الشروحات تُكتب أسفل الصورة في المستند.
 2) رموز قياسية: مقاومة متعرجة، بطارية (لوحان)، مصدر تيار (دائرة+سهم)، أسهم تيار زرقاء، open/short بالإنجليزية.
 3) ألوان وظيفية فقط: أزرق للتيارات، أخضر للعنصر المطلوب، أحمر لإشارات القطبية.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = '/tmp/my-project/ref_assets/diagrams'
os.makedirs(OUT, exist_ok=True)

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

BLK = '#111111'
BLUE = '#1a5fb4'
RED = '#c01c28'
GRN = '#1d6f42'
GRY = '#777777'
LW = 2.0


def new_ax(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=110)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, name):
    p = os.path.join(OUT, name + '.png')
    fig.savefig(p, bbox_inches='tight', facecolor='white', pad_inches=0.06)
    plt.close(fig)
    print('saved', name)


def wire(ax, pts, color=BLK, lw=LW):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle='round', zorder=2)


def resistor(ax, x0, y0, x1, y1, label=None, lab_dx=0.0, lab_dy=0.30, color=BLK, fs=11.5, side='auto'):
    dx, dy = x1 - x0, y1 - y0
    L = np.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    t = np.linspace(0, L, 13)
    off = np.array([0, 0.09, 0.22, 0.09, -0.09, -0.22, -0.09, 0.09, 0.22, 0.09, -0.09, 0, 0])
    px = x0 + ux * t - uy * off
    py = y0 + uy * t + ux * off
    ax.plot(px, py, color=color, lw=1.7, zorder=3)
    if label:
        if abs(dx) < 1e-9:
            ax.text(x1 + (0.30 if side == 'auto' else (lab_dx or 0.30)), (y0 + y1) / 2, label,
                    fontsize=fs, ha='left', va='center', color=color)
        else:
            ax.text((x0 + x1) / 2 + (lab_dx or 0), (y0 + y1) / 2 + (lab_dy or 0.30), label,
                    fontsize=fs, ha='center', va='bottom', color=color)


def battery_v(ax, xc, yc, label=None, lab_dx=0.42, plus_top=True, fs=11.5, color=BLK):
    hl, hs, g = 0.36, 0.16, 0.16
    y1, y0 = yc + g, yc - g
    # الطرف الموجب = اللوح الطويل دائماً
    if plus_top:
        ax.plot([xc - hl, xc + hl], [y1, y1], color=color, lw=2.4, zorder=3)
        ax.plot([xc - hs, xc + hs], [y0, y0], color=color, lw=3.2, zorder=3)
        ax.text(xc + 0.10, y1 + 0.12, '+', fontsize=10.5, color=RED, ha='left', va='bottom')
        ax.text(xc + 0.10, y0 - 0.32, '−', fontsize=12, color=RED, ha='left', va='bottom')
    else:
        ax.plot([xc - hs, xc + hs], [y1, y1], color=color, lw=3.2, zorder=3)
        ax.plot([xc - hl, xc + hl], [y0, y0], color=color, lw=2.4, zorder=3)
        ax.text(xc + 0.10, y0 + 0.12, '+', fontsize=10.5, color=RED, ha='left', va='bottom')
        ax.text(xc + 0.10, y1 + 0.12, '−', fontsize=12, color=RED, ha='left', va='bottom')
    ax.plot([xc, xc], [y1, y1 + 1.0], color=color, lw=LW, zorder=2)
    ax.plot([xc, xc], [y0 - 1.0, y0], color=color, lw=LW, zorder=2)
    if label:
        ax.text(xc + lab_dx, yc, label, fontsize=fs, ha='left', va='center', color=color)


def battery_h(ax, xc, yc, label=None, plus_right=True, fs=11.5, color=BLK, wire_len=1.0):
    hl, hs, g = 0.16, 0.34, 0.14
    x1, x0 = xc + g, xc - g
    if plus_right:
        ax.plot([x1, x1], [yc - hl, yc + hl], color=color, lw=2.4, zorder=3)  # طولي = +
        ax.plot([x0, x0], [yc - hs, yc + hs], color=color, lw=3.2, zorder=3)
        ax.text(x1 + 0.10, yc + 0.14, '+', fontsize=10.5, color=RED, ha='left', va='bottom')
        ax.text(x0 - 0.28, yc + 0.14, '−', fontsize=12, color=RED, ha='right', va='bottom')
    else:
        ax.plot([x0, x0], [yc - hl, yc + hl], color=color, lw=2.4, zorder=3)
        ax.plot([x1, x1], [yc - hs, yc + hs], color=color, lw=3.2, zorder=3)
        ax.text(x0 - 0.28, yc + 0.14, '+', fontsize=10.5, color=RED, ha='right', va='bottom')
        ax.text(x1 + 0.10, yc + 0.14, '−', fontsize=12, color=RED, ha='left', va='bottom')
    ax.plot([xc - wire_len, x0], [yc, yc], color=color, lw=LW, zorder=2)
    ax.plot([x1, xc + wire_len], [yc, yc], color=color, lw=LW, zorder=2)
    if label:
        ax.text(xc, yc - 0.55, label, fontsize=fs, ha='center', va='top', color=color)


def csource_v(ax, xc, yc, label=None, up=True, lab_dx=0.5, fs=11.5, color=BLK, r=0.30):
    t = np.linspace(0, 2 * np.pi, 60)
    ax.plot(xc + r * np.cos(t), yc + r * np.sin(t), color=color, lw=1.8, zorder=3)
    s = 0.15 if up else -0.15
    ax.annotate('', xy=(xc, yc + s), xytext=(xc, yc - s),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=1.8), zorder=4)
    ax.plot([xc, xc], [yc + r, yc + r + 1.0], color=color, lw=LW, zorder=2)
    ax.plot([xc, xc], [yc - r - 1.0, yc - r], color=color, lw=LW, zorder=2)
    if label:
        ax.text(xc + lab_dx, yc, label, fontsize=fs, ha='left', va='center', color=color)


def varrow(ax, x, y, up=True, color=BLUE, label=None, fs=11, lab_dx=0.16):
    ax.annotate('', xy=(x, y + 0.55 if up else y - 0.55), xytext=(x, y),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=2.0))
    if label:
        ax.text(x + lab_dx, y + (0.32 if up else -0.30), label, fontsize=fs, color=color,
                ha='left' if lab_dx > 0 else 'right', va='center')


def harrow(ax, x, y, right=True, color=BLUE, label=None, fs=11):
    ax.annotate('', xy=(x + 0.55 if right else x - 0.55, y), xytext=(x, y),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=2.0))
    if label:
        ax.text(x + (0.14 if right else -0.14), y + 0.20, label, fontsize=fs, color=color,
                ha='left' if right else 'right')


def vspan(ax, x, y0, y1, label, color=GRY, fs=11):
    ax.annotate('', xy=(x, y1), xytext=(x, y0),
                arrowprops=dict(arrowstyle='<|-|>', color=color, lw=1.3, shrinkA=0, shrinkB=0))
    ax.text(x + 0.12, (y0 + y1) / 2, label, fontsize=fs, color=color, ha='left', va='center')


def node(ax, x, y, label=None, dx=0.0, dy=0.16, fs=12, color=BLK):
    ax.plot([x], [y], marker='o', ms=5.5, color=BLK, zorder=5)
    if label:
        ax.text(x + dx, y + dy, label, fontsize=fs, ha='center', color=color)


def meter_v(ax, x, y, r=0.30):
    t = np.linspace(0, 2 * np.pi, 60)
    ax.plot(x + r * np.cos(t), y + r * np.sin(t), color=BLK, lw=1.6, zorder=3)
    ax.text(x, y, 'V', fontsize=12, ha='center', va='center', style='italic')
    ax.plot([x, x], [y + r, y + r + 0.9], color=BLK, lw=LW, zorder=2)
    ax.plot([x, x], [y - r - 0.9, y - r], color=BLK, lw=LW, zorder=2)


def meter_v_bridge(ax, x0, x1, yt, h=0.75, r=0.26):
    """فولتميتر فوق عنصر أفقي بين x0 و x1 على المستوى yt — جسر ⊓."""
    xm = (x0 + x1) / 2
    ax.plot([x0, x0, xm - r], [yt, yt + h, yt + h], color=BLK, lw=1.6, zorder=2)
    ax.plot([xm + r, x1, x1], [yt + h, yt + h, yt], color=BLK, lw=1.6, zorder=2)
    t = np.linspace(0, 2 * np.pi, 60)
    ax.plot(xm + r * np.cos(t), yt + h + r * np.sin(t), color=BLK, lw=1.6, zorder=3)
    ax.text(xm, yt + h, 'V', fontsize=11.5, ha='center', va='center', style='italic')
    node(ax, x0, yt)
    node(ax, x1, yt)


def meter_a(ax, x, y, r=0.30):
    t = np.linspace(0, 2 * np.pi, 60)
    ax.plot(x + r * np.cos(t), y + r * np.sin(t), color=BLK, lw=1.6, zorder=3)
    ax.text(x, y, 'A', fontsize=12, ha='center', va='center', style='italic')


def loop_arrow(ax, cx, cy, r=0.5, ccw=False, label=None, color=BLUE, fs=12):
    """سهم حلقي دائري مع اختياري تسمية."""
    th = np.linspace(np.pi * 0.25, np.pi * 1.6 if not ccw else np.pi * 1.9, 40)
    if ccw:
        th = np.linspace(np.pi * 0.4, np.pi * 1.75, 40)
    xs = cx + r * np.cos(th)
    ys = cy + r * np.sin(th)
    ax.plot(xs, ys, color=color, lw=1.8, zorder=4)
    ax.annotate('', xy=(xs[-1], ys[-1]), xytext=(xs[-6], ys[-6]),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=1.8))
    if label:
        ax.text(cx, cy + r + 0.15, label, fontsize=fs, color=color, ha='center')


# ================================================================ دارة أوم بالأجهزة
def d_ohm_circuit():
    fig, ax = new_ax(5.6, 4.0)
    yb, yt = 0.5, 2.6
    wire(ax, [(0.6, yb), (5.6, yb)])
    wire(ax, [(0.6, yt), (5.6, yt)])
    wire(ax, [(0.6, yb), (0.6, yt)])
    battery_v(ax, 0.6, 1.55, 'E')
    resistor(ax, 2.1, yt, 3.4, yt, 'R')
    meter_a(ax, 4.9, yt)
    meter_v_bridge(ax, 2.1, 3.4, yt, h=0.8)
    harrow(ax, 1.35, yt, True, BLUE, 'I', 12)
    save(fig, 'ohm_circuit')


# ================================================================ دارة المصباح
def d_heater():
    fig, ax = new_ax(5.0, 3.5)
    yb, yt = 0.4, 2.4
    wire(ax, [(0.5, yb), (4.8, yb)])
    wire(ax, [(0.5, yt), (4.8, yt)])
    wire(ax, [(0.5, yb), (0.5, yt)])
    battery_v(ax, 0.5, 1.4, '220 V')
    cx, cy, r = 2.6, yt, 0.32
    t = np.linspace(0, 2 * np.pi, 60)
    wire(ax, [(1.7, yt), (cx - r, yt)])
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color=BLK, lw=1.8, zorder=3)
    ax.plot([cx - 0.2, cx + 0.2], [cy - 0.2, cy + 0.2], color=BLK, lw=1.5, zorder=4)
    ax.plot([cx - 0.2, cx + 0.2], [cy + 0.2, cy - 0.2], color=BLK, lw=1.5, zorder=4)
    wire(ax, [(cx + r, yt), (4.8, yt)])
    ax.text(cx, cy + 0.52, '100 W', fontsize=11.5, ha='center')
    harrow(ax, 3.9, yt, True, BLUE, 'I', 11.5)
    save(fig, 'heater_circuit')


# ================================================================ التوالي العام
def d_series():
    fig, ax = new_ax(7.4, 3.5)
    yb, yt = 0.5, 2.7
    wire(ax, [(0.6, yb), (7.2, yb)])
    wire(ax, [(0.6, yt), (7.2, yt)])
    wire(ax, [(0.6, yb), (0.6, yt)])
    battery_v(ax, 0.6, 1.6, 'E')
    resistor(ax, 1.9, yt, 3.1, yt, 'R₁')
    resistor(ax, 3.8, yt, 5.0, yt, 'R₂')
    resistor(ax, 5.7, yt, 6.9, yt, 'R₃')
    harrow(ax, 1.35, yt, True, BLUE, 'I', 12)
    vspan(ax, 1.9, yt + 0.55, yt + 1.30, 'V₁')
    vspan(ax, 3.8, yt + 0.55, yt + 1.30, 'V₂')
    vspan(ax, 5.7, yt + 0.55, yt + 1.30, 'V₃')
    ax.text(3.9, 0.05, 'E = V₁ + V₂ + V₃', fontsize=12, ha='center', color=BLK, weight='bold')
    save(fig, 'series_circuit')


# ================================================================ مثال مقسم الجهد 30V
def d_vdiv_ex():
    fig, ax = new_ax(5.6, 3.5)
    yb, yt = 0.5, 2.6
    wire(ax, [(0.6, yb), (5.2, yb)])
    wire(ax, [(0.6, yt), (5.2, yt)])
    wire(ax, [(0.6, yb), (0.6, yt)])
    battery_v(ax, 0.6, 1.55, '30 V')
    resistor(ax, 2.0, yt, 3.0, yt, '5 Ω')
    resistor(ax, 3.9, yt, 4.9, yt, '10 Ω')
    node(ax, 3.0, yt)
    node(ax, 3.9, yt)
    node(ax, 5.2, yt)
    harrow(ax, 1.4, yt, True, BLUE, 'I = 2 A', 11)
    vspan(ax, 2.0, yt + 0.5, yt + 1.15, 'V₁ = 10 V')
    vspan(ax, 3.9, yt + 0.5, yt + 1.15, 'V₂ = 20 V')
    save(fig, 'vdiv_ex')


# ================================================================ التوازي العام
def d_parallel():
    fig, ax = new_ax(6.4, 4.1)
    yb, yt = 0.5, 3.3
    wire(ax, [(0.7, yb), (5.9, yb)])
    wire(ax, [(0.7, yt), (5.9, yt)])
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 1.9, 'E')
    for xx, rl in [(2.3, 'R₁'), (3.6, 'R₂'), (4.9, 'R₃')]:
        wire(ax, [(xx, yt), (xx, 2.65)])
        resistor(ax, xx, 2.65, xx, 1.15, rl, lab_dx=0.30, lab_dy=0)
        wire(ax, [(xx, 1.15), (xx, yb)])
        node(ax, xx, yt)
        node(ax, xx, yb)
    harrow(ax, 1.4, yt, True, BLUE, 'I_T', 12)
    ax.text(3.3, 0.05, 'I_T = I₁ + I₂ + I₃', fontsize=12, ha='center', weight='bold')
    save(fig, 'parallel_circuit')


# ================================================================ مثال مقسم التيار 150mA
def d_idiv_ex():
    fig, ax = new_ax(5.6, 4.1)
    yb, yt = 0.5, 3.4
    wire(ax, [(0.8, yb), (5.0, yb)])
    wire(ax, [(0.8, yt), (5.0, yt)])
    csource_v(ax, 0.8, 1.95, None, up=True)
    ax.text(0.40, 1.95, 'I = 150 mA', fontsize=11.5, ha='right')
    wire(ax, [(0.8, yb), (0.8, yt)])
    for xx, rl in [(2.4, '100 Ω'), (4.2, '50 Ω')]:
        wire(ax, [(xx, yt), (xx, 2.75)])
        resistor(ax, xx, 2.75, xx, 1.15, rl, lab_dx=0.34, lab_dy=0)
        wire(ax, [(xx, 1.15), (xx, yb)])
        node(ax, xx, yt)
        node(ax, xx, yb)
    varrow(ax, 1.55, 2.5, True, BLUE, 'I₁ = 50 mA', 10.5)
    varrow(ax, 3.35, 2.5, True, BLUE, 'I₂ = 100 mA', 10.5)
    save(fig, 'idiv_ex')


# ================================================================ مثال مركب 60V
def d_compound_ex5():
    fig, ax = new_ax(6.6, 4.3)
    yb, yt = 0.5, 3.5
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 2.0, '60 V')
    wire(ax, [(0.7, yt), (1.9, yt)])
    resistor(ax, 1.9, yt, 3.0, yt, 'R₁ = 10 Ω')
    node(ax, 3.0, yt)
    wire(ax, [(3.0, yt), (5.9, yt)])
    wire(ax, [(5.9, yt), (5.9, yb)])
    wire(ax, [(3.0, yb), (5.9, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 2.85)])
    resistor(ax, 3.0, 2.85, 3.0, 1.15, '100 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(3.0, 1.15), (3.0, yb)])
    node(ax, 3.0, yb)
    mid = (3.0 + 5.9) / 2
    node(ax, mid, yt)
    wire(ax, [(mid, yt), (mid, 2.85)])
    resistor(ax, mid, 2.85, mid, 1.15, '100 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(mid, 1.15), (mid, yb)])
    node(ax, mid, yb)
    node(ax, 5.9, yt)
    node(ax, 5.9, yb)
    harrow(ax, 1.45, yt, True, BLUE, None)
    ax.text(1.55, yt - 0.42, 'I₁ = 1 A', fontsize=10.5, color=BLUE, ha='left')
    varrow(ax, mid - 0.55, 2.4, True, BLUE, 'I₂ = 0.5 A', 10.5, lab_dx=-0.15)
    varrow(ax, 5.35, 2.4, True, BLUE, 'I₃ = 0.5 A', 10.5, lab_dx=0.18)
    save(fig, 'compound_ex5')


# ================================================================ تدريب الوحدة 3 المستقل
def d_compound_u3():
    fig, ax = new_ax(6.6, 4.3)
    yb, yt = 0.5, 3.5
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 2.0, '12 V')
    wire(ax, [(0.7, yt), (1.9, yt)])
    resistor(ax, 1.9, yt, 3.0, yt, '4 Ω')
    node(ax, 3.0, yt)
    wire(ax, [(3.0, yt), (5.9, yt)])
    wire(ax, [(5.9, yt), (5.9, yb)])
    wire(ax, [(3.0, yb), (5.9, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 2.85)])
    resistor(ax, 3.0, 2.85, 3.0, 1.15, '20 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(3.0, 1.15), (3.0, yb)])
    node(ax, 3.0, yb)
    mid = (3.0 + 5.9) / 2
    node(ax, mid, yt)
    wire(ax, [(mid, yt), (mid, 2.85)])
    resistor(ax, mid, 2.85, mid, 1.15, '30 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(mid, 1.15), (mid, yb)])
    node(ax, mid, yb)
    node(ax, 5.9, yt)
    node(ax, 5.9, yb)
    harrow(ax, 1.45, yt, True, BLUE, 'I', 12)
    varrow(ax, mid - 0.55, 2.4, True, BLUE, 'I₁ = ?', 10.5, lab_dx=-0.15)
    varrow(ax, 5.35, 2.4, True, BLUE, 'I₂ = ?', 10.5, lab_dx=0.18)
    save(fig, 'compound_u3')


# ================================================================ مصدر جهد حقيقي
def d_vsource_real():
    fig, ax = new_ax(6.0, 3.9)
    yb, yt = 0.5, 3.0
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 1.75, 'E')
    wire(ax, [(0.7, yt), (1.9, yt)])
    resistor(ax, 1.9, yt, 2.9, yt, 'ri', lab_dy=0.26)
    node(ax, 2.9, yt, 'A', dx=0.18, dy=0.14)
    node(ax, 2.9, yb, 'B', dx=0.18, dy=-0.48)
    wire(ax, [(2.9, yt), (5.0, yt)])
    wire(ax, [(2.9, yb), (5.0, yb)])
    wire(ax, [(0.7, yb), (2.9, yb)])
    wire(ax, [(5.0, yt), (5.0, 2.4)])
    resistor(ax, 5.0, 2.4, 5.0, 1.1, 'RL', lab_dx=0.32, lab_dy=0)
    wire(ax, [(5.0, 1.1), (5.0, yb)])
    node(ax, 5.0, yt)
    node(ax, 5.0, yb)
    vspan(ax, 5.75, yb, yt, 'Vo')
    save(fig, 'vsource_real')


# ================================================================ مصدر تيار حقيقي
def d_csource_real():
    fig, ax = new_ax(6.0, 3.9)
    yb, yt = 0.5, 3.0
    wire(ax, [(0.8, yb), (5.4, yb)])
    wire(ax, [(0.8, yt), (5.4, yt)])
    csource_v(ax, 0.8, 1.75, None, up=True)
    ax.text(0.40, 1.75, 'Is', fontsize=12.5, ha='right', style='italic')
    resistor(ax, 2.0, 2.35, 2.0, 1.15, 'ri', lab_dx=0.32, lab_dy=0)
    node(ax, 2.0, yt)
    node(ax, 2.0, yb)
    node(ax, 5.4, yt, 'A', dx=0.18, dy=0.14)
    node(ax, 5.4, yb, 'B', dx=0.18, dy=-0.48)
    wire(ax, [(5.4, yt), (5.4, 2.4)])
    resistor(ax, 5.4, 2.4, 5.4, 1.1, 'RL', lab_dx=0.32, lab_dy=0)
    wire(ax, [(5.4, 1.1), (5.4, yb)])
    save(fig, 'csource_real')


# ================================================================ التحويل بين المصدرين
def d_source_transform():
    fig, ax = new_ax(9.4, 3.8)
    yb, yt = 0.5, 2.9
    wire(ax, [(0.6, yb), (0.6, yt)])
    battery_v(ax, 0.6, 1.7, 'E')
    wire(ax, [(0.6, yt), (1.8, yt)])
    resistor(ax, 1.8, yt, 2.8, yt, 'ri')
    node(ax, 2.8, yt, 'A', dx=0.18, dy=0.14)
    node(ax, 2.8, yb, 'B', dx=0.18, dy=-0.48)
    wire(ax, [(2.8, yt), (3.6, yt)])
    wire(ax, [(0.6, yb), (3.6, yb)])
    ax.text(2.1, 0.02, 'Voltage source', fontsize=11, ha='center', color=GRY)
    ax.annotate('', xy=(5.45, 1.7), xytext=(4.05, 1.7),
                arrowprops=dict(arrowstyle='<|-|>', color=GRN, lw=2.4))
    ax.text(4.75, 1.98, 'equal', fontsize=10.5, ha='center', color=GRN)
    x0 = 5.6
    wire(ax, [(x0, yb), (x0 + 3.0, yb)])
    wire(ax, [(x0, yt), (x0 + 3.0, yt)])
    csource_v(ax, x0, 1.7, None, up=True)
    ax.text(x0 - 0.36, 1.7, 'Is', fontsize=12.5, ha='right', style='italic')
    resistor(ax, x0 + 1.4, 2.25, x0 + 1.4, 1.15, 'ri', lab_dx=0.32, lab_dy=0)
    node(ax, x0 + 1.4, yt)
    node(ax, x0 + 1.4, yb)
    node(ax, x0 + 3.0, yt, 'A', dx=0.18, dy=0.14)
    node(ax, x0 + 3.0, yb, 'B', dx=0.18, dy=-0.48)
    ax.text(x0 + 1.5, 0.02, 'Current source   (Is = E ÷ ri)', fontsize=11, ha='center', color=GRY)
    save(fig, 'source_transform')


# ================================================================ عقدة كيرشوف
def d_kcl_node():
    fig, ax = new_ax(6.4, 3.3)
    cx, cy = 3.0, 1.6
    node(ax, cx, cy)
    wire(ax, [(cx - 2.4, cy), (cx - 0.10, cy)])
    harrow(ax, cx - 1.85, cy, True, BLUE, 'I₁', 12.5)
    wire(ax, [(cx, cy + 1.5), (cx, cy + 0.10)])
    varrow(ax, cx + 0.35, cy + 0.85, False, BLUE, 'I₃', 12.5)
    wire(ax, [(cx + 0.10, cy), (cx + 2.4, cy)])
    harrow(ax, cx + 1.15, cy, True, BLUE, 'I₂', 12.5)
    wire(ax, [(cx, cy - 0.10), (cx, cy - 1.35)])
    varrow(ax, cx + 0.35, cy - 0.7, False, BLUE, 'I₄', 12.5)
    ax.text(cx, cy - 1.72, 'I₁ + I₃ = I₂ + I₄', fontsize=13.5, ha='center', weight='bold')
    save(fig, 'kcl_node')


# ================================================================ حلقة كيرشوف وإشارات
def d_kvl_loop():
    fig, ax = new_ax(6.6, 3.9)
    yb, yt = 0.5, 2.9
    wire(ax, [(0.7, yb), (6.0, yb)])
    wire(ax, [(0.7, yt), (6.0, yt)])
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 1.7, 'E')
    resistor(ax, 2.0, yt, 3.0, yt, 'R₁')
    resistor(ax, 3.7, yt, 4.7, yt, 'R₂')
    resistor(ax, 5.4, yt, 6.4, yt, 'R₃')
    harrow(ax, 1.45, yt, True, BLUE, 'I', 12)
    for x0 in [2.0, 3.7, 5.4]:
        ax.text(x0 - 0.16, yt + 0.22, '+', fontsize=10, color=RED, ha='center')
        ax.text(x0 + 1.16, yt + 0.22, '−', fontsize=12, color=RED, ha='center')
    ax.text(3.35, 0.05, 'E = V₁ + V₂ + V₃', fontsize=12, ha='center', weight='bold')
    save(fig, 'kvl_loop')


# ================================================================ مثال كيرشوف 16/20V
def d_kirchhoff_ex():
    fig, ax = new_ax(7.8, 4.5)
    yb, yt = 0.5, 3.6
    node(ax, 3.0, yt, 'A', dx=-0.22, dy=0.15)
    node(ax, 3.0, yb, 'B', dx=-0.22, dy=-0.48)
    wire(ax, [(3.0, yt), (3.0, 2.95)])
    resistor(ax, 3.0, 2.95, 3.0, 1.15, '20 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(3.0, 1.15), (3.0, yb)])
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 2.85)])
    resistor(ax, 0.7, 2.85, 0.7, 1.25, '10 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 0.7, 0.95, None, plus_top=True)
    ax.text(1.06, 0.95, '16 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 0.25), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (5.3, yt)])
    wire(ax, [(5.3, yt), (5.3, 2.85)])
    resistor(ax, 5.3, 2.85, 5.3, 1.25, '12 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 5.3, 0.95, None, plus_top=True)
    ax.text(5.66, 0.95, '20 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(5.3, 0.25), (5.3, yb)])
    wire(ax, [(3.0, yb), (5.3, yb)])
    varrow(ax, 0.7, 3.30, True, BLUE, 'I₁ = 0.2 A', 10.5, lab_dx=0.18)
    varrow(ax, 3.0, 3.30, False, BLUE, 'I₃ = 0.7 A', 10.5, lab_dx=-0.22)
    varrow(ax, 5.3, 3.30, True, BLUE, 'I₂ = 0.5 A', 10.5, lab_dx=0.18)
    save(fig, 'kirchhoff_ex')


# ================================================================ المسألة الذهبية
def d_golden_main():
    fig, ax = new_ax(8.0, 4.7)
    yb, yt = 0.5, 3.8
    node(ax, 3.0, yt, 'c', dx=-0.24, dy=0.13)
    node(ax, 3.0, yb, 'd', dx=-0.24, dy=-0.5)
    wire(ax, [(3.0, yt), (3.0, 3.15)])
    resistor(ax, 3.0, 3.15, 3.0, 1.15, '2 Ω', lab_dx=0.34, lab_dy=0, color=GRN)
    wire(ax, [(3.0, 1.15), (3.0, yb)])
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.05)])
    resistor(ax, 0.7, 3.05, 0.7, 1.25, '6 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 0.7, 0.95, None, plus_top=True)
    ax.text(1.06, 0.95, '28 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 0.25), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (5.3, yt)])
    wire(ax, [(5.3, yt), (5.3, 3.05)])
    resistor(ax, 5.3, 3.05, 5.3, 1.25, '3 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 5.3, 0.95, None, plus_top=True)
    ax.text(5.66, 0.95, '10 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(5.3, 0.25), (5.3, yb)])
    wire(ax, [(3.0, yb), (5.3, yb)])
    varrow(ax, 0.7, 3.50, True, BLUE, 'I₁', 12, lab_dx=0.18)
    varrow(ax, 3.0, 3.50, False, BLUE, 'I₃', 12, lab_dx=-0.24)
    varrow(ax, 5.3, 3.50, True, BLUE, 'I₂', 12, lab_dx=0.18)
    ax.text(4.3, 0.05, 'Find: I₃ (through the 2 Ω) = 4 A  (4 methods, same answer)', fontsize=10,
            ha='center', color=GRY)
    save(fig, 'golden_main')


# ================================================================ الذهبية — نزع الحمل
def d_golden_open():
    fig, ax = new_ax(7.6, 4.5)
    yb, yt = 0.5, 3.6
    node(ax, 3.0, yt, 'c', dx=-0.24, dy=0.13)
    node(ax, 3.0, yb, 'd', dx=-0.24, dy=-0.5)
    wire(ax, [(3.0, yt), (3.0, 2.6)])
    wire(ax, [(3.0, 2.0), (3.0, yb)])
    ax.text(3.30, 2.3, 'open', fontsize=10.5, color=GRN)
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.0)])
    resistor(ax, 0.7, 3.0, 0.7, 1.3, '6 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 0.7, 1.0, None, plus_top=True)
    ax.text(1.06, 1.0, '28 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 0.3), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (5.3, yt)])
    wire(ax, [(5.3, yt), (5.3, 3.0)])
    resistor(ax, 5.3, 3.0, 5.3, 1.3, '3 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 5.3, 1.0, None, plus_top=True)
    ax.text(5.66, 1.0, '10 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(5.3, 0.3), (5.3, yb)])
    wire(ax, [(3.0, yb), (5.3, yb)])
    varrow(ax, 0.7, 3.30, True, BLUE, 'I₀', 12, lab_dx=0.18)
    ax.text(4.3, 0.05, 'I₀ = (28−10) ÷ (6+3) = 2 A', fontsize=11.5, ha='center', weight='bold')
    save(fig, 'golden_open')


# ================================================================ الذهبية — Rth
def d_golden_rth():
    fig, ax = new_ax(7.6, 4.3)
    yb, yt = 0.5, 3.4
    node(ax, 3.0, yt, 'c', dx=-0.24, dy=0.13)
    node(ax, 3.0, yb, 'd', dx=-0.24, dy=-0.5)
    wire(ax, [(3.0, yt), (3.0, 2.5)])
    wire(ax, [(3.0, 1.5), (3.0, yb)])
    ax.text(3.30, 2.0, 'open', fontsize=10.5, color=GRN)
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 2.8)])
    resistor(ax, 0.7, 2.8, 0.7, 1.2, '6 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(0.7, 1.2), (0.7, yb)])
    ax.plot([0.52, 0.88], [0.95, 0.95], color=BLK, lw=2.2)
    ax.text(1.06, 0.95, 'short', fontsize=10, color=GRY, ha='left', va='center')
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (5.3, yt)])
    wire(ax, [(5.3, yt), (5.3, 2.8)])
    resistor(ax, 5.3, 2.8, 5.3, 1.2, '3 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(5.3, 1.2), (5.3, yb)])
    ax.plot([5.12, 5.48], [0.95, 0.95], color=BLK, lw=2.2)
    ax.text(5.66, 0.95, 'short', fontsize=10, color=GRY, ha='left', va='center')
    wire(ax, [(3.0, yb), (5.3, yb)])
    ax.text(4.3, 0.05, 'Rth = (6×3) ÷ (6+3) = 2 Ω', fontsize=11.5, ha='center', weight='bold')
    save(fig, 'golden_rth')


# ================================================================ الذهبية — الدارة المكافئة
def d_golden_equiv():
    fig, ax = new_ax(6.6, 4.3)
    yb, yt = 0.5, 3.4
    node(ax, 2.6, yt, 'c', dx=-0.24, dy=0.13)
    node(ax, 2.6, yb, 'd', dx=-0.24, dy=-0.5)
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 1.95, 'Vth = 16 V')
    wire(ax, [(0.7, yt), (1.75, yt)])
    resistor(ax, 1.75, yt, 2.6, yt, 'Rth = 2 Ω')
    node(ax, 2.6, yt)
    wire(ax, [(2.6, yt), (2.6, 2.75)])
    resistor(ax, 2.6, 2.75, 2.6, 1.15, '2 Ω', lab_dx=0.62, lab_dy=0, color=GRN)
    wire(ax, [(2.6, 1.15), (2.6, yb)])
    node(ax, 2.6, yb)
    varrow(ax, 2.6, 2.4, False, BLUE, 'I₃ = 4 A', 11, lab_dx=0.18)
    ax.text(3.5, 0.05, 'I₃ = Vth ÷ (Rth + RL) = 16 ÷ (2+2) = 4 A', fontsize=12,
            ha='center', weight='bold')
    save(fig, 'golden_equiv')


# ================================================================ التراكب 6V/12V
def d_sup_main():
    fig, ax = new_ax(9.0, 4.9)
    yb, yt = 0.5, 3.9
    node(ax, 3.0, yt)
    node(ax, 5.6, yt)
    node(ax, 3.0, yb)
    node(ax, 5.6, yb)
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.2)])
    battery_v(ax, 0.7, 2.9, None, plus_top=True)
    ax.text(1.06, 2.9, '6 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 2.2), (0.7, 2.0)])
    resistor(ax, 0.7, 2.0, 0.7, 1.5, '0.5 Ω', lab_dx=0.4, lab_dy=0)
    wire(ax, [(0.7, 1.5), (0.7, 1.3)])
    resistor(ax, 0.7, 1.3, 0.7, 0.8, '2.5 Ω', lab_dx=0.44, lab_dy=0)
    wire(ax, [(0.7, 0.8), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 3.2)])
    resistor(ax, 3.0, 3.2, 3.0, 1.2, '6 Ω', lab_dx=0.34, lab_dy=0, color=GRN)
    wire(ax, [(3.0, 1.2), (3.0, yb)])
    wire(ax, [(5.6, yt), (8.3, yt)])
    wire(ax, [(8.3, yt), (8.3, 3.2)])
    resistor(ax, 8.3, 3.2, 8.3, 2.7, '1 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 8.3, 2.35, None, plus_top=True)
    ax.text(8.66, 2.35, '12 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(8.3, 1.65), (8.3, 1.5)])
    resistor(ax, 8.3, 1.5, 8.3, 1.0, '2 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(8.3, 1.0), (8.3, yb)])
    wire(ax, [(5.6, yb), (8.3, yb)])
    wire(ax, [(3.0, yb), (5.6, yb)])
    wire(ax, [(3.0, yt), (5.6, yt)])
    save(fig, 'sup_main')


def d_sup_s1():
    fig, ax = new_ax(8.6, 4.7)
    yb, yt = 0.5, 3.7
    node(ax, 3.0, yt)
    node(ax, 5.4, yt)
    node(ax, 3.0, yb)
    node(ax, 5.4, yb)
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.0)])
    battery_v(ax, 0.7, 2.7, None, plus_top=True)
    ax.text(1.06, 2.7, '6 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 2.0), (0.7, 1.8)])
    resistor(ax, 0.7, 1.8, 0.7, 1.3, '0.5 Ω', lab_dx=0.4, lab_dy=0)
    wire(ax, [(0.7, 1.3), (0.7, 1.1)])
    resistor(ax, 0.7, 1.1, 0.7, 0.6, '2.5 Ω', lab_dx=0.44, lab_dy=0)
    wire(ax, [(0.7, 0.6), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 3.0)])
    resistor(ax, 3.0, 3.0, 3.0, 1.1, '6 Ω', lab_dx=0.34, lab_dy=0, color=GRN)
    wire(ax, [(3.0, 1.1), (3.0, yb)])
    wire(ax, [(5.4, yt), (7.9, yt)])
    wire(ax, [(7.9, yt), (7.9, 3.0)])
    resistor(ax, 7.9, 3.0, 7.9, 2.5, '1 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(7.9, 2.5), (7.9, 1.8)])
    ax.plot([7.72, 8.08], [1.8, 1.8], color=BLK, lw=2.4)
    ax.text(8.24, 1.8, 'short', fontsize=10, color=GRY, ha='left', va='center')
    wire(ax, [(7.9, 1.8), (7.9, 1.6)])
    resistor(ax, 7.9, 1.6, 7.9, 1.1, '2 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(7.9, 1.1), (7.9, yb)])
    wire(ax, [(5.4, yb), (7.9, yb)])
    wire(ax, [(3.0, yb), (5.4, yb)])
    wire(ax, [(3.0, yt), (5.4, yt)])
    ax.text(4.3, 0.05, 'Stage 1: only 6 V works (12 V shorted) → I′ = 0.4 A', fontsize=11, ha='center', weight='bold')
    save(fig, 'sup_s1')


def d_sup_s2():
    fig, ax = new_ax(8.6, 4.7)
    yb, yt = 0.5, 3.7
    node(ax, 3.0, yt)
    node(ax, 5.4, yt)
    node(ax, 3.0, yb)
    node(ax, 5.4, yb)
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.0)])
    wire(ax, [(0.7, 3.0), (0.7, 2.0)])
    ax.plot([0.52, 0.88], [2.0, 2.0], color=BLK, lw=2.4)
    ax.text(1.06, 2.0, 'short', fontsize=10, color=GRY, ha='left', va='center')
    wire(ax, [(0.7, 2.0), (0.7, 1.8)])
    resistor(ax, 0.7, 1.8, 0.7, 1.3, '0.5 Ω', lab_dx=0.4, lab_dy=0)
    wire(ax, [(0.7, 1.3), (0.7, 1.1)])
    resistor(ax, 0.7, 1.1, 0.7, 0.6, '2.5 Ω', lab_dx=0.44, lab_dy=0)
    wire(ax, [(0.7, 0.6), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 3.0)])
    resistor(ax, 3.0, 3.0, 3.0, 1.1, '6 Ω', lab_dx=0.34, lab_dy=0, color=GRN)
    wire(ax, [(3.0, 1.1), (3.0, yb)])
    wire(ax, [(5.4, yt), (7.9, yt)])
    wire(ax, [(7.9, yt), (7.9, 3.0)])
    resistor(ax, 7.9, 3.0, 7.9, 2.5, '1 Ω', lab_dx=0.34, lab_dy=0)
    battery_v(ax, 7.9, 2.15, None, plus_top=True)
    ax.text(8.26, 2.15, '12 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(7.9, 1.45), (7.9, 1.3)])
    resistor(ax, 7.9, 1.3, 7.9, 0.8, '2 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(7.9, 0.8), (7.9, yb)])
    wire(ax, [(5.4, yb), (7.9, yb)])
    wire(ax, [(3.0, yb), (5.4, yb)])
    wire(ax, [(3.0, yt), (5.4, yt)])
    ax.text(4.3, 0.05, 'Stage 2: only 12 V works (6 V shorted) → I″ = 0.8 A', fontsize=11, ha='center', weight='bold')
    save(fig, 'sup_s2')


# ================================================================ ثيفنين مثال الكتاب 5
def d_thev_book5():
    fig, ax = new_ax(9.6, 4.9)
    yb, yt = 0.5, 3.9
    node(ax, 3.0, yt, 'A', dx=-0.24, dy=0.13)
    node(ax, 3.0, yb, 'B', dx=-0.26, dy=-0.5)
    node(ax, 6.0, yt, 'C', dx=0.0, dy=0.15)
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.15)])
    battery_v(ax, 0.7, 2.85, None, plus_top=True)
    ax.text(1.06, 2.85, '20 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 2.15), (0.7, 2.0)])
    resistor(ax, 0.7, 2.0, 0.7, 1.5, '50 Ω', lab_dx=0.4, lab_dy=0)
    wire(ax, [(0.7, 1.5), (0.7, 1.35)])
    resistor(ax, 0.7, 1.35, 0.7, 0.85, '150 Ω', lab_dx=0.46, lab_dy=0)
    wire(ax, [(0.7, 0.85), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 3.2)])
    resistor(ax, 3.0, 3.2, 3.0, 1.2, '100 Ω', lab_dx=0.34, lab_dy=0, color=GRN)
    ax.text(3.34, 1.62, 'load', fontsize=10, color=GRN, ha='left')
    wire(ax, [(3.0, 1.2), (3.0, yb)])
    wire(ax, [(3.0, yb), (9.2, yb)])
    wire(ax, [(9.2, yb), (9.2, 0.85)])
    resistor(ax, 9.2, 0.85, 9.2, 1.35, '80 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(9.2, 1.35), (9.2, 1.5)])
    battery_v(ax, 9.2, 1.85, None, plus_top=True)
    ax.text(9.56, 1.85, '10 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(9.2, 2.15), (9.2, 2.0)])
    resistor(ax, 9.2, 2.0, 9.2, 2.5, '20 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(9.2, 2.5), (9.2, 3.15)])
    node(ax, 9.2, 3.15)
    wire(ax, [(9.2, 3.15), (6.0, 3.15)])
    node(ax, 6.0, 3.15)
    wire(ax, [(6.0, 3.15), (6.0, yt)])
    node(ax, 6.0, yt)
    wire(ax, [(6.0, yb), (6.0, 1.0)])
    wire(ax, [(3.0, yt), (6.0, yt)])
    ax.text(4.9, 0.05, 'Vth = 15 − 8 = 7 V ,   Rth = 37.5 + 16 = 53.5 Ω ,   I = 45.6 mA',
            fontsize=10.5, ha='center', weight='bold')
    save(fig, 'thev_book5')


# ================================================================ نورتون — مثال نظيف
def d_norton_ex():
    fig, ax = new_ax(7.4, 4.5)
    yb, yt = 0.5, 3.6
    node(ax, 2.0, yt)
    node(ax, 2.0, yb)
    node(ax, 5.6, yt, 'A', dx=-0.24, dy=0.13)
    node(ax, 5.6, yb, 'B', dx=-0.24, dy=-0.5)
    wire(ax, [(2.0, yb), (5.6, yb)])
    wire(ax, [(2.0, yt), (5.6, yt)])
    csource_v(ax, 2.0, 2.05, None, up=True)
    ax.text(1.56, 2.05, '1 A', fontsize=12, ha='right')
    resistor(ax, 2.0, 2.95, 2.0, 1.15, '20 Ω', lab_dx=0.32, lab_dy=0)
    wire(ax, [(2.0, yt), (2.0, 2.95)])
    wire(ax, [(2.0, 1.15), (2.0, yb)])
    wire(ax, [(2.0, yt), (4.3, yt)])
    resistor(ax, 4.3, yt, 5.6, yt, '30 Ω')
    node(ax, 4.3, yt)
    wire(ax, [(5.6, yt), (5.6, 2.9)])
    resistor(ax, 5.6, 2.9, 5.6, 1.2, '50 Ω', lab_dx=0.62, lab_dy=0, color=GRN)
    ax.text(6.22, 2.05, 'load', fontsize=10, color=GRN, ha='left')
    wire(ax, [(5.6, 1.2), (5.6, yb)])
    ax.text(3.8, 0.05, 'IN = 1×20÷(20+30) = 0.4 A ,   RN = 20+30 = 50 Ω ,   I = 0.4×50÷100 = 0.2 A',
            fontsize=10.5, ha='center', weight='bold')
    save(fig, 'norton_ex')


def d_norton_equiv():
    fig, ax = new_ax(6.2, 4.1)
    yb, yt = 0.5, 3.2
    node(ax, 3.4, yt, 'A', dx=-0.24, dy=0.13)
    node(ax, 3.4, yb, 'B', dx=-0.24, dy=-0.5)
    wire(ax, [(0.9, yb), (5.8, yb)])
    wire(ax, [(0.9, yt), (5.8, yt)])
    csource_v(ax, 0.9, 1.85, None, up=True)
    ax.text(0.46, 1.85, 'IN', fontsize=12, ha='right', style='italic')
    ax.text(0.46, 1.30, '0.4 A', fontsize=10.5, ha='right')
    resistor(ax, 2.0, 2.55, 2.0, 1.15, 'RN = 50 Ω', lab_dx=0.34, lab_dy=0)
    node(ax, 2.0, yt)
    node(ax, 2.0, yb)
    wire(ax, [(2.0, yt), (2.0, 2.55)])
    wire(ax, [(2.0, 1.15), (2.0, yb)])
    wire(ax, [(3.4, yt), (3.4, 2.55)])
    resistor(ax, 3.4, 2.55, 3.4, 1.15, '50 Ω', lab_dx=0.32, lab_dy=0, color=GRN)
    wire(ax, [(3.4, 1.15), (3.4, yb)])
    node(ax, 3.4, yt)
    node(ax, 3.4, yb)
    varrow(ax, 3.05, 2.0, False, BLUE, 'I = 0.2 A', 10.5, lab_dx=-0.24)
    save(fig, 'norton_equiv')


# ================================================================ ميلمان
def d_millman():
    fig, ax = new_ax(9.2, 4.7)
    yb, yt = 0.5, 3.8
    node(ax, 2.2, yt, 'A', dx=0.0, dy=0.16)
    node(ax, 2.2, yb, 'B', dx=0.0, dy=-0.5)
    xs = [0.7, 2.2, 3.7]
    vals = [('10 V', '200 Ω'), ('5 V', '150 Ω'), ('15 V', '300 Ω')]
    for xx, (ev, rv) in zip(xs, vals):
        wire(ax, [(xx, yt), (xx, 3.0)])
        battery_v(ax, xx, 2.65, None, plus_top=True)
        ax.text(xx + 0.34, 2.65, ev, fontsize=10.5, ha='left', va='center')
        wire(ax, [(xx, 2.0), (xx, 1.85)])
        resistor(ax, xx, 1.85, xx, 1.2, rv, lab_dx=0.38, lab_dy=0)
        wire(ax, [(xx, 1.2), (xx, yb)])
        node(ax, xx, yt)
        node(ax, xx, yb)
    wire(ax, [(0.7, yt), (3.7, yt)])
    wire(ax, [(0.7, yb), (3.7, yb)])
    wire(ax, [(2.2, yb), (6.2, yb)])
    wire(ax, [(2.2, yt), (6.2, yt)])
    wire(ax, [(6.2, yt), (6.2, 3.0)])
    resistor(ax, 6.2, 3.0, 6.2, 1.2, '100 Ω', lab_dx=0.62, lab_dy=0, color=GRN)
    ax.text(6.82, 2.1, 'load', fontsize=10, color=GRN, ha='left')
    wire(ax, [(6.2, 1.2), (6.2, yb)])
    node(ax, 6.2, yt)
    node(ax, 6.2, yb)
    ax.text(3.4, 0.05, 'REQ = 66.67 Ω ,  VEQ = 8.89 V  →  I_L = 8.89 ÷ (66.67+100) = 53.3 mA',
            fontsize=10.5, ha='center', weight='bold')
    save(fig, 'millman')


# ================================================================ مثلث ونجمة
def d_deltay():
    fig, ax = new_ax(9.8, 4.2)
    A = (1.0, 0.9); B = (3.4, 0.9); C = (2.2, 2.9)
    for p, q in [(A, B), (B, C), (C, A)]:
        wire(ax, [p, q])
    node(ax, *A, 'A', dx=-0.24, dy=-0.06)
    node(ax, *B, 'B', dx=0.24, dy=-0.06)
    node(ax, *C, 'C', dx=0.0, dy=0.16)
    ax.text(1.30, 2.15, 'RA', fontsize=11.5, ha='center', rotation=52)
    ax.text(3.10, 2.15, 'RB', fontsize=11.5, ha='center', rotation=-52)
    ax.text(2.2, 0.62, 'RC', fontsize=11.5, ha='center')
    ax.text(2.2, 3.35, 'Delta  Δ', fontsize=12, ha='center', weight='bold')
    O = (7.4, 1.2)
    for p, lbl in [((7.4, 2.9), 'R₁'), ((5.6, 0.5), 'R₂'), ((9.2, 0.5), 'R₃')]:
        wire(ax, [O, p])
        resistor(ax, O[0] + (p[0] - O[0]) * 0.25, O[1] + (p[1] - O[1]) * 0.25,
                 O[0] + (p[0] - O[0]) * 0.75, O[1] + (p[1] - O[1]) * 0.75, None)
        ax.text((O[0] + p[0]) / 2 + 0.30, (O[1] + p[1]) / 2, lbl, fontsize=11.5, ha='left')
        node(ax, *p, None)
    ax.text(7.4, 3.14, 'A', fontsize=12, ha='center')
    ax.text(5.36, 0.34, 'B', fontsize=12, ha='center')
    ax.text(9.44, 0.34, 'C', fontsize=12, ha='center')
    node(ax, *O, 'O', dx=0.0, dy=0.0)
    ax.text(7.4, 3.35, 'Star  Y', fontsize=12, ha='center', weight='bold')
    ax.text(4.85, 1.75, 'Δ  ⇄  Y', fontsize=13, ha='center', color=GRN, weight='bold')
    save(fig, 'deltay')


# ================================================================ جسر ويتستون
def d_wheatstone():
    fig, ax = new_ax(7.8, 4.9)
    A = (1.0, 0.8); B = (2.6, 4.0); C = (6.6, 0.8); D = (5.0, 4.0)
    node(ax, *A, 'A', dx=-0.24, dy=-0.1)
    node(ax, *B, 'B', dx=-0.24, dy=0.13)
    node(ax, *C, 'C', dx=0.26, dy=-0.1)
    node(ax, *D, 'D', dx=0.26, dy=0.13)
    wire(ax, [A, B]); wire(ax, [B, C]); wire(ax, [A, D]); wire(ax, [D, C])
    def seg_res(p, q, lbl, off=0.36):
        mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = np.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        ax.text(mx + nx * off, my + ny * off, lbl, fontsize=11.5, ha='center')
    seg_res(A, B, '20 Ω', 0.38)
    seg_res(B, C, '10 Ω', 0.38)
    seg_res(A, D, '30 Ω', 0.38)
    seg_res(D, C, '5 Ω', 0.38)
    wire(ax, [B, D])
    mx, my = (B[0] + D[0]) / 2, (B[1] + D[1]) / 2
    t = np.linspace(0, 2 * np.pi, 60)
    ax.plot(mx + 0.28 * np.cos(t), my + 0.28 * np.sin(t), color=GRN, lw=1.8, zorder=4)
    ax.text(mx, my, 'G', fontsize=11.5, ha='center', va='center', color=GRN, zorder=5)
    ax.text(mx, my - 0.52, '50 Ω', fontsize=10.5, ha='center', color=GRN)
    wire(ax, [A, C])
    battery_h(ax, 3.8, 0.8, 'E = 8 V', plus_right=True, wire_len=1.4)
    save(fig, 'wheatstone')


def d_wheatstone_after():
    fig, ax = new_ax(7.8, 4.7)
    A = (0.8, 3.4); O = (3.6, 2.3); B = (6.6, 3.4); C = (6.6, 0.8)
    node(ax, *A, 'A', dx=-0.26, dy=0.0)
    node(ax, *O, 'O', dx=-0.30, dy=0.05)
    node(ax, *B, 'B', dx=0.26, dy=0.0)
    node(ax, *C, 'C', dx=0.28, dy=-0.12)
    # RA: A→O (6 Ω)
    wire(ax, [(A[0] + 0.12, A[1] - 0.12), (O[0] - 0.14, O[1] + 0.12)])
    resistor(ax, A[0] + 0.12, A[1] - 0.12, O[0] - 0.14, O[1] + 0.12, None)
    ax.text(1.85, 2.95, '6 Ω', fontsize=11.5, ha='center')
    # RB: O→B ثم 10Ω من B نزولاً إلى C
    wire(ax, [(O[0] + 0.14, O[1] + 0.12), (B[0] - 0.12, B[1] - 0.12)])
    resistor(ax, O[0] + 0.14, O[1] + 0.12, B[0] - 0.12, B[1] - 0.12, None)
    ax.text(5.35, 2.95, '10 Ω', fontsize=11.5, ha='center')
    wire(ax, [(B[0], B[1]), (B[0], 2.7)])
    resistor(ax, B[0], 2.7, B[0], 1.5, '10 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(B[0], 1.5), (B[0], C[1])])
    # من O نزولاً: 15Ω ثم D ثم 5Ω إلى C
    wire(ax, [(O[0], O[1] - 0.12), (O[0], 1.7)])
    resistor(ax, O[0], 1.7, O[0], 1.2, '15 Ω', lab_dx=0.36, lab_dy=0)
    node(ax, O[0], 0.95)
    ax.text(O[0] - 0.28, 0.95, 'D', fontsize=12, ha='right')
    wire(ax, [(O[0], 0.95), (O[0], 0.8)])
    resistor(ax, O[0], 0.8, 4.9, 0.8, None)
    ax.text(4.7, 1.0, '5 Ω', fontsize=11, ha='center')
    wire(ax, [(4.9, 0.8), (C[0], C[1])])
    # المصدر أسفل بين A و C
    wire(ax, [(A[0], A[1]), (A[0], 0.12)])
    wire(ax, [(A[0], 0.12), (2.7, 0.12)])
    battery_h(ax, 3.05, 0.12, None, plus_right=True, wire_len=0.55)
    ax.text(3.05, -0.42, 'E = 8 V', fontsize=11.5, ha='center')
    wire(ax, [(3.4, 0.12), (C[0], 0.12)])
    wire(ax, [(C[0], 0.12), (C[0], C[1])])
    ax.text(3.9, 4.15, '(10+10) ∥ (15+5) = 20 ∥ 20 = 10 Ω   →   Req = 6 + 10 = 16 Ω',
            fontsize=10.5, ha='center', weight='bold')
    save(fig, 'wheatstone_after')


# ================================================================ عقدة واحدة
def d_nodal_ex4():
    fig, ax = new_ax(8.6, 4.5)
    yb, yt = 0.5, 3.6
    node(ax, 4.0, yt, 'A', dx=0.0, dy=0.16)
    node(ax, 4.0, yb)
    wire(ax, [(4.0, yt), (1.2, yt)])
    wire(ax, [(1.2, yt), (1.2, 2.9)])
    battery_v(ax, 1.2, 2.6, None, plus_top=True)
    ax.text(1.56, 2.6, '10 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(1.2, 1.9), (1.2, 1.75)])
    resistor(ax, 1.2, 1.75, 1.2, 1.15, '40 Ω', lab_dx=0.4, lab_dy=0)
    wire(ax, [(1.2, 1.15), (1.2, yb)])
    wire(ax, [(4.0, yt), (6.8, yt)])
    wire(ax, [(6.8, yt), (6.8, 2.9)])
    battery_v(ax, 6.8, 2.6, None, plus_top=True)
    ax.text(7.16, 2.6, '6 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(6.8, 1.9), (6.8, 1.75)])
    resistor(ax, 6.8, 1.75, 6.8, 1.15, '30 Ω', lab_dx=0.4, lab_dy=0)
    wire(ax, [(6.8, 1.15), (6.8, yb)])
    wire(ax, [(4.0, yt), (4.0, 2.9)])
    resistor(ax, 4.0, 2.9, 4.0, 1.15, '60 Ω', lab_dx=0.36, lab_dy=0)
    wire(ax, [(4.0, 1.15), (4.0, yb)])
    wire(ax, [(1.2, yb), (6.8, yb)])
    ax.plot([3.75, 4.25], [yb, yb], color=BLK, lw=2.6)
    ax.plot([3.87, 4.13], [yb - 0.15, yb - 0.15], color=BLK, lw=2.0)
    ax.plot([3.97, 4.03], [yb - 0.30, yb - 0.30], color=BLK, lw=1.8)
    ax.text(4.45, yb - 0.34, 'ground = 0 V', fontsize=10, color=GRY, ha='left')
    ax.text(4.3, -0.55, '(10−VA)÷40 + (6−VA)÷30 = VA÷60   →   VA = 6 V',
            fontsize=11, ha='center', weight='bold')
    save(fig, 'nodal_ex4')


# ================================================================ مثال الحلقات المستقل
def d_mesh_ex():
    fig, ax = new_ax(8.2, 4.7)
    yb, yt = 0.5, 3.8
    node(ax, 3.0, yt)
    node(ax, 3.0, yb)
    wire(ax, [(3.0, yt), (3.0, 3.1)])
    resistor(ax, 3.0, 3.1, 3.0, 1.2, '1 Ω', lab_dx=0.32, lab_dy=0)
    wire(ax, [(3.0, 1.2), (3.0, yb)])
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.0)])
    resistor(ax, 0.7, 3.0, 0.7, 1.3, '2 Ω', lab_dx=0.32, lab_dy=0)
    battery_v(ax, 0.7, 1.0, None, plus_top=True)
    ax.text(1.06, 1.0, '7 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 0.3), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (5.3, yt)])
    wire(ax, [(5.3, yt), (5.3, 3.0)])
    resistor(ax, 5.3, 3.0, 5.3, 1.3, '2 Ω', lab_dx=0.32, lab_dy=0)
    battery_v(ax, 5.3, 1.0, None, plus_top=True)
    ax.text(5.66, 1.0, '5 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(5.3, 0.3), (5.3, yb)])
    wire(ax, [(3.0, yb), (5.3, yb)])
    loop_arrow(ax, 1.7, 2.3, r=0.42, ccw=False, label='I₁')
    loop_arrow(ax, 4.3, 2.3, r=0.42, ccw=False, label='I₂')
    save(fig, 'mesh_ex')


# ================================================================ امتحان: كيرشوف
def d_exam_kirchhoff():
    fig, ax = new_ax(8.2, 4.7)
    yb, yt = 0.5, 3.8
    node(ax, 3.0, yt)
    node(ax, 3.0, yb)
    wire(ax, [(3.0, yt), (3.0, 3.1)])
    resistor(ax, 3.0, 3.1, 3.0, 1.2, '10 Ω', lab_dx=0.38, lab_dy=0)
    wire(ax, [(3.0, 1.2), (3.0, yb)])
    wire(ax, [(3.0, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.0)])
    resistor(ax, 0.7, 3.0, 0.7, 1.3, '5 Ω', lab_dx=0.32, lab_dy=0)
    battery_v(ax, 0.7, 1.0, None, plus_top=True)
    ax.text(1.06, 1.0, '10 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 0.3), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (5.3, yt)])
    wire(ax, [(5.3, yt), (5.3, 3.0)])
    resistor(ax, 5.3, 3.0, 5.3, 1.3, '5 Ω', lab_dx=0.32, lab_dy=0)
    battery_v(ax, 5.3, 1.0, None, plus_top=True)
    ax.text(5.66, 1.0, '10 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(5.3, 0.3), (5.3, yb)])
    wire(ax, [(3.0, yb), (5.3, yb)])
    varrow(ax, 0.7, 3.50, True, BLUE, 'I₁', 12, lab_dx=0.18)
    varrow(ax, 3.0, 3.50, False, BLUE, 'I₃ = ?', 11, lab_dx=-0.35)
    varrow(ax, 5.3, 3.50, True, BLUE, 'I₂', 12, lab_dx=0.18)
    save(fig, 'exam_kirchhoff')


# ================================================================ امتحان: ثيفنين
def d_exam_thevenin():
    fig, ax = new_ax(7.6, 4.5)
    yb, yt = 0.5, 3.6
    node(ax, 3.2, yt, 'A', dx=-0.24, dy=0.13)
    node(ax, 3.2, yb, 'B', dx=-0.24, dy=-0.5)
    wire(ax, [(3.2, yb), (6.0, yb)])
    wire(ax, [(3.2, yt), (6.0, yt)])
    wire(ax, [(6.0, yt), (6.0, 2.9)])
    resistor(ax, 6.0, 2.9, 6.0, 1.2, '4 Ω', lab_dx=0.60, lab_dy=0, color=GRN)
    ax.text(6.60, 2.05, 'load', fontsize=10, color=GRN, ha='left')
    wire(ax, [(6.0, 1.2), (6.0, yb)])
    node(ax, 6.0, yt)
    node(ax, 6.0, yb)
    wire(ax, [(3.2, yt), (0.7, yt)])
    wire(ax, [(0.7, yt), (0.7, 3.0)])
    battery_v(ax, 0.7, 2.7, None, plus_top=True)
    ax.text(1.06, 2.7, '18 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(0.7, 2.0), (0.7, 1.85)])
    resistor(ax, 0.7, 1.85, 0.7, 1.25, '6 Ω', lab_dx=0.32, lab_dy=0)
    wire(ax, [(0.7, 1.25), (0.7, yb)])
    wire(ax, [(0.7, yb), (3.2, yb)])
    wire(ax, [(3.2, yt), (3.2, 3.05)])
    resistor(ax, 3.2, 3.05, 3.2, 1.15, '12 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(3.2, 1.15), (3.2, yb)])
    save(fig, 'exam_thevenin')


# ================================================================ امتحان: ميلمان
def d_exam_millman():
    fig, ax = new_ax(8.0, 4.5)
    yb, yt = 0.5, 3.6
    node(ax, 2.0, yt)
    node(ax, 2.0, yb)
    for xx, ev, rv in [(0.8, '12 V', '6 Ω'), (3.2, '6 V', '3 Ω')]:
        wire(ax, [(xx, yt), (xx, 3.0)])
        battery_v(ax, xx, 2.65, None, plus_top=True)
        ax.text(xx + 0.34, 2.65, ev, fontsize=11, ha='left', va='center')
        wire(ax, [(xx, 2.0), (xx, 1.85)])
        resistor(ax, xx, 1.85, xx, 1.2, rv, lab_dx=0.38, lab_dy=0)
        wire(ax, [(xx, 1.2), (xx, yb)])
        node(ax, xx, yt)
        node(ax, xx, yb)
    wire(ax, [(0.8, yt), (3.2, yt)])
    wire(ax, [(0.8, yb), (3.2, yb)])
    wire(ax, [(2.0, yb), (6.4, yb)])
    wire(ax, [(2.0, yt), (6.4, yt)])
    wire(ax, [(6.4, yt), (6.4, 2.9)])
    resistor(ax, 6.4, 2.9, 6.4, 1.2, '2 Ω', lab_dx=0.58, lab_dy=0, color=GRN)
    ax.text(6.98, 2.05, 'load', fontsize=10, color=GRN, ha='left')
    wire(ax, [(6.4, 1.2), (6.4, yb)])
    node(ax, 6.4, yt)
    node(ax, 6.4, yb)
    save(fig, 'exam_millman')


# ================================================================ امتحان: مقسم جهد
def d_exam_vdiv():
    fig, ax = new_ax(5.8, 3.5)
    yb, yt = 0.5, 2.6
    wire(ax, [(0.6, yb), (5.4, yb)])
    wire(ax, [(0.6, yt), (5.4, yt)])
    wire(ax, [(0.6, yb), (0.6, yt)])
    battery_v(ax, 0.6, 1.55, '24 V')
    resistor(ax, 2.0, yt, 3.1, yt, 'R₁ = 6 kΩ')
    resistor(ax, 3.9, yt, 5.0, yt, 'R₂ = 2 kΩ')
    node(ax, 3.1, yt)
    node(ax, 3.9, yt)
    harrow(ax, 1.4, yt, True, BLUE, 'I', 12)
    vspan(ax, 3.9, yt + 0.5, yt + 1.12, 'V₂ = ?')
    save(fig, 'exam_vdiv')


# ================================================================ امتحان: مقسم تيار
def d_exam_idiv():
    fig, ax = new_ax(5.8, 4.1)
    yb, yt = 0.5, 3.4
    wire(ax, [(0.8, yb), (5.2, yb)])
    wire(ax, [(0.8, yt), (5.2, yt)])
    csource_v(ax, 0.8, 1.95, None, up=True)
    ax.text(0.36, 1.95, 'I = 6 A', fontsize=11.5, ha='right')
    wire(ax, [(0.8, yb), (0.8, yt)])
    for xx, rl in [(2.6, '30 Ω'), (4.4, '60 Ω')]:
        wire(ax, [(xx, yt), (xx, 2.75)])
        resistor(ax, xx, 2.75, xx, 1.15, rl, lab_dx=0.34, lab_dy=0)
        wire(ax, [(xx, 1.15), (xx, yb)])
        node(ax, xx, yt)
        node(ax, xx, yb)
    varrow(ax, 1.7, 2.5, True, BLUE, 'I₁ = ?', 10.5)
    varrow(ax, 3.55, 2.5, True, BLUE, 'I₂ = ?', 10.5)
    save(fig, 'exam_idiv')


# ================================================================ امتحان: مصباح
def d_exam_heater():
    fig, ax = new_ax(5.4, 3.5)
    yb, yt = 0.4, 2.4
    wire(ax, [(0.5, yb), (4.8, yb)])
    wire(ax, [(0.5, yt), (4.8, yt)])
    wire(ax, [(0.5, yb), (0.5, yt)])
    battery_v(ax, 0.5, 1.4, '220 V')
    cx, cy, r = 2.6, yt, 0.32
    t = np.linspace(0, 2 * np.pi, 60)
    wire(ax, [(1.7, yt), (cx - r, yt)])
    ax.plot(cx + r * np.cos(t), cy + r * np.sin(t), color=BLK, lw=1.8, zorder=3)
    ax.plot([cx - 0.2, cx + 0.2], [cy - 0.2, cy + 0.2], color=BLK, lw=1.5, zorder=4)
    ax.plot([cx - 0.2, cx + 0.2], [cy + 0.2, cy - 0.2], color=BLK, lw=1.5, zorder=4)
    wire(ax, [(cx + r, yt), (4.8, yt)])
    ax.text(cx, cy + 0.52, '60 W', fontsize=11.5, ha='center')
    save(fig, 'exam_heater')


# ================================================================ الواجب س1 — إعادة رسم مطابقة للشكل الأصلي
def d_hw_q1():
    fig, ax = new_ax(9.6, 5.2)
    yt, ym, yb = 4.0, 2.4, 0.7
    # العقد
    node(ax, 0.8, yb, 'a', dx=-0.28, dy=-0.16)
    node(ax, 0.8, ym, 'b', dx=-0.28, dy=0.14)
    node(ax, 3.4, ym, 'k', dx=0.0, dy=-0.42)
    node(ax, 3.4, yt, 'h', dx=-0.28, dy=0.12)
    node(ax, 5.0, yt, 'g', dx=0.26, dy=0.12)
    node(ax, 8.0, yt, 'e', dx=0.26, dy=0.14)
    node(ax, 8.0, yb, 'f', dx=0.28, dy=-0.16)
    node(ax, 6.0, yb, 'd', dx=0.0, dy=-0.5)
    node(ax, 3.4, 1.9, 'c', dx=-0.30, dy=-0.36)
    # الفرع الأيسر: a →(10Ω)→ b  و I₁ صاعد
    wire(ax, [(0.8, yb), (0.8, ym + 1.0)])
    resistor(ax, 0.8, ym + 1.0, 0.8, ym - 0.4, '10 Ω', lab_dx=0.36, lab_dy=0)
    wire(ax, [(0.8, ym - 0.4), (0.8, ym)])
    varrow(ax, 0.8, ym + 1.25, True, BLUE, 'I₁', 11.5, lab_dx=0.18)
    # من b يميناً: 20Ω حتى k
    wire(ax, [(0.8, ym), (2.0, ym)])
    resistor(ax, 2.0, ym, 3.4, ym, '20 Ω', lab_dy=0.28)
    node(ax, 3.4, ym)
    # بطارية 20 عمودية من k صاعداً إلى h: الموجب أسفل (جهة k)
    battery_v(ax, 3.4, 3.2, None, plus_top=False)
    ax.text(3.78, 3.2, '20 V', fontsize=11, ha='left', va='center')
    # السلك العلوي: h → g → (10Ω) → e
    wire(ax, [(3.4, yt), (4.3, yt)])
    resistor(ax, 4.3, yt, 5.8, yt, '10 Ω', lab_dy=0.28)
    wire(ax, [(5.8, yt), (8.0, yt)])
    node(ax, 4.0, yt)
    harrow(ax, 7.3, yt, False, BLUE, 'I₂', 11)
    # الفرع الأيمن: e ينزل إلى f
    wire(ax, [(8.0, yt), (8.0, yb)])
    varrow(ax, 8.0, 2.4, False, BLUE, '', 10)
    # الأسفل: a → بطارية 40 (الموجب عند a) → f مع عقدة d
    wire(ax, [(0.8, yb), (3.6, yb)])
    battery_h(ax, 3.95, yb, None, plus_right=False, wire_len=0.55)
    ax.text(3.95, yb - 0.66, '40 V', fontsize=11, ha='center')
    wire(ax, [(4.3, yb), (8.0, yb)])
    node(ax, 6.0, yb)
    # الوسط: c موصولة بسلك صاعد إلى k ثم (30Ω) يميناً حتى d
    wire(ax, [(3.4, ym), (3.4, 1.9)])
    node(ax, 3.4, 1.9)
    wire(ax, [(3.4, 1.9), (3.9, 1.9)])
    resistor(ax, 3.9, 1.9, 5.4, 1.9, '30 Ω', lab_dy=0.28)
    wire(ax, [(5.4, 1.9), (6.0, 1.9)])
    wire(ax, [(6.0, 1.9), (6.0, yb)])
    node(ax, 6.0, 1.9)
    varrow(ax, 4.65, 1.9, True, BLUE, 'I', 11.5)
    save(fig, 'hw_q1')


# ================================================================ الواجب س1 — نزع 30
def d_hw_q1_open():
    fig, ax = new_ax(8.8, 4.5)
    yt, yb = 3.5, 0.7
    node(ax, 4.4, yt, 'c', dx=0.24, dy=0.1)
    node(ax, 4.4, yb, 'd', dx=0.26, dy=-0.48)
    wire(ax, [(4.4, yt), (4.4, 2.7)])
    wire(ax, [(4.4, 2.0), (4.4, yb)])
    ax.text(4.72, 2.35, 'open (removed 30 Ω)', fontsize=10, color=GRN)
    wire(ax, [(4.4, yt), (1.0, yt)])
    wire(ax, [(1.0, yt), (1.0, 2.9)])
    resistor(ax, 1.0, 2.9, 1.0, 2.4, '10 Ω', lab_dx=0.32, lab_dy=0)
    wire(ax, [(1.0, 2.4), (1.0, 2.25)])
    resistor(ax, 1.0, 2.25, 1.0, 1.75, '20 Ω', lab_dx=0.32, lab_dy=0)
    battery_v(ax, 1.0, 1.3, None, plus_top=True)
    ax.text(1.36, 1.3, '40 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(1.0, 0.6), (1.0, yb)])
    wire(ax, [(1.0, yb), (4.4, yb)])
    wire(ax, [(4.4, yt), (7.6, yt)])
    wire(ax, [(7.6, yt), (7.6, 2.9)])
    resistor(ax, 7.6, 2.9, 7.6, 2.4, '10 Ω', lab_dx=0.32, lab_dy=0)
    battery_v(ax, 7.6, 2.05, None, plus_top=True)
    ax.text(7.96, 2.05, '20 V', fontsize=11.5, ha='left', va='center')
    wire(ax, [(7.6, 1.35), (7.6, yb)])
    wire(ax, [(4.4, yb), (7.6, yb)])
    varrow(ax, 1.0, 3.2, True, BLUE, 'I₀', 12, lab_dx=0.16)
    ax.text(4.3, 0.05, 'I₀ = (40−20) ÷ (30+10) = 0.5 A   →   Vth = 40 − (0.5×30) = 25 V',
            fontsize=10.5, ha='center', weight='bold')
    save(fig, 'hw_q1_open')


# ================================================================ الواجب س1 — Rth
def d_hw_q1_rth():
    fig, ax = new_ax(8.0, 4.1)
    yt, yb = 3.3, 0.7
    node(ax, 4.0, yt, 'c', dx=0.24, dy=0.1)
    node(ax, 4.0, yb, 'd', dx=0.26, dy=-0.48)
    wire(ax, [(4.0, yt), (4.0, 2.5)])
    wire(ax, [(4.0, 1.5), (4.0, yb)])
    ax.text(4.32, 2.0, 'open', fontsize=10, color=GRN)
    wire(ax, [(4.0, yt), (1.0, yt)])
    wire(ax, [(1.0, yt), (1.0, 2.5)])
    resistor(ax, 1.0, 2.5, 1.0, 1.5, '30 Ω', lab_dx=0.32, lab_dy=0)
    wire(ax, [(1.0, 1.5), (1.0, yb)])
    ax.plot([0.82, 1.18], [1.15, 1.15], color=BLK, lw=2.4)
    ax.text(1.34, 1.15, 'short', fontsize=10, color=GRY, ha='left', va='center')
    wire(ax, [(1.0, yb), (4.0, yb)])
    wire(ax, [(4.0, yt), (7.0, yt)])
    wire(ax, [(7.0, yt), (7.0, 2.5)])
    resistor(ax, 7.0, 2.5, 7.0, 1.5, '10 Ω', lab_dx=0.32, lab_dy=0)
    wire(ax, [(7.0, 1.5), (7.0, yb)])
    ax.plot([6.82, 7.18], [1.15, 1.15], color=BLK, lw=2.4)
    ax.text(7.34, 1.15, 'short', fontsize=10, color=GRY, ha='left', va='center')
    wire(ax, [(4.0, yb), (7.0, yb)])
    ax.text(4.0, 0.05, 'Rth = (30×10) ÷ (30+10) = 7.5 Ω', fontsize=11.5, ha='center', weight='bold')
    save(fig, 'hw_q1_rth')


# ================================================================ الواجب س1 — المكافئ
def d_hw_q1_equiv():
    fig, ax = new_ax(6.8, 4.1)
    yt, yb = 3.2, 0.6
    node(ax, 2.8, yt, 'c', dx=-0.24, dy=0.1)
    node(ax, 2.8, yb, 'd', dx=-0.24, dy=-0.46)
    wire(ax, [(0.8, yb), (0.8, yt)])
    battery_v(ax, 0.8, 1.9, 'Vth = 25 V')
    wire(ax, [(0.8, yt), (1.9, yt)])
    resistor(ax, 1.9, yt, 2.8, yt, 'Rth = 7.5 Ω')
    node(ax, 2.8, yt)
    wire(ax, [(2.8, yt), (2.8, 2.5)])
    resistor(ax, 2.8, 2.5, 2.8, 1.1, '30 Ω', lab_dx=0.34, lab_dy=0, color=GRN)
    wire(ax, [(2.8, 1.1), (2.8, yb)])
    node(ax, 2.8, yb)
    varrow(ax, 2.45, 1.95, False, BLUE, 'I₃ = 0.67 A', 10.5, lab_dx=-0.26)
    save(fig, 'hw_q1_equiv')


# ================================================================ الواجب س2
def d_hw_q2():
    fig, ax = new_ax(7.6, 4.3)
    yb, yt = 0.6, 3.2
    wire(ax, [(0.8, yb), (7.0, yb)])
    wire(ax, [(0.8, yt), (7.0, yt)])
    wire(ax, [(0.8, yb), (0.8, yt)])
    battery_v(ax, 0.8, 1.9, None, plus_top=True)
    ax.text(1.18, 1.9, 'ε', fontsize=13.5, ha='left', va='center', style='italic')
    wire(ax, [(0.8, yt), (2.0, yt)])
    resistor(ax, 2.0, yt, 2.9, yt, 'r', lab_dy=0.26)
    # V عبر المصدر كاملاً (ε + r): فرع عمودي بعد r
    wire(ax, [(3.3, yt), (3.3, 2.0)])
    meter_v(ax, 3.3, 1.3)
    wire(ax, [(3.3, 0.6), (3.3, yb)])
    node(ax, 3.3, yt)
    node(ax, 3.3, yb)
    # المفتاح
    wire(ax, [(3.7, yb), (4.5, yb)])
    ax.plot([4.5, 5.05], [yb, yb + 0.38], color=BLK, lw=2.2)
    ax.text(4.78, yb + 0.55, 'S', fontsize=12.5, ha='center')
    wire(ax, [(5.05, yb), (7.0, yb)])
    # R و A
    resistor(ax, 5.4, yb, 6.3, yb, 'R', lab_dy=-0.60)
    meter_a(ax, 6.7, yb, r=0.3)
    save(fig, 'hw_q2')


if __name__ == '__main__':
    d_ohm_circuit(); d_heater(); d_series(); d_vdiv_ex(); d_parallel(); d_idiv_ex()
    d_compound_ex5(); d_compound_u3(); d_vsource_real(); d_csource_real(); d_source_transform()
    d_kcl_node(); d_kvl_loop(); d_kirchhoff_ex()
    d_golden_main(); d_golden_open(); d_golden_rth(); d_golden_equiv()
    d_sup_main(); d_sup_s1(); d_sup_s2(); d_thev_book5()
    d_norton_ex(); d_norton_equiv(); d_millman(); d_deltay()
    d_wheatstone(); d_wheatstone_after(); d_nodal_ex4(); d_mesh_ex()
    d_exam_kirchhoff(); d_exam_thevenin(); d_exam_millman(); d_exam_vdiv(); d_exam_idiv(); d_exam_heater()
    d_hw_q1(); d_hw_q1_open(); d_hw_q1_rth(); d_hw_q1_equiv(); d_hw_q2()
    print('ALL DONE:', len(os.listdir(OUT)), 'files')


# ================================================================ امتحان: مركب 18V
def d_exam_compound():
    fig, ax = new_ax(6.6, 4.3)
    yb, yt = 0.5, 3.5
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 2.0, '18 V')
    wire(ax, [(0.7, yt), (1.9, yt)])
    resistor(ax, 1.9, yt, 3.0, yt, '6 Ω')
    node(ax, 3.0, yt)
    wire(ax, [(3.0, yt), (5.9, yt)])
    wire(ax, [(5.9, yt), (5.9, yb)])
    wire(ax, [(3.0, yb), (5.9, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 2.85)])
    resistor(ax, 3.0, 2.85, 3.0, 1.15, '20 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(3.0, 1.15), (3.0, yb)])
    node(ax, 3.0, yb)
    mid = (3.0 + 5.9) / 2
    node(ax, mid, yt)
    wire(ax, [(mid, yt), (mid, 2.85)])
    resistor(ax, mid, 2.85, mid, 1.15, '30 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(mid, 1.15), (mid, yb)])
    node(ax, mid, yb)
    node(ax, 5.9, yt)
    node(ax, 5.9, yb)
    harrow(ax, 1.45, yt, True, BLUE, 'I', 12)
    varrow(ax, mid - 0.55, 2.4, True, BLUE, 'I₁ = ?', 10.5, lab_dx=-0.15)
    varrow(ax, 5.35, 2.4, True, BLUE, 'I₂ = ?', 10.5, lab_dx=0.18)
    save(fig, 'exam_compound')


# ================================================================ امتحان: تحدي ورقة فارغة 24V
def d_exam_blank():
    fig, ax = new_ax(6.6, 4.3)
    yb, yt = 0.5, 3.5
    wire(ax, [(0.7, yb), (0.7, yt)])
    battery_v(ax, 0.7, 2.0, '24 V')
    wire(ax, [(0.7, yt), (1.9, yt)])
    resistor(ax, 1.9, yt, 3.0, yt, '2 Ω')
    node(ax, 3.0, yt)
    wire(ax, [(3.0, yt), (5.9, yt)])
    wire(ax, [(5.9, yt), (5.9, yb)])
    wire(ax, [(3.0, yb), (5.9, yb)])
    wire(ax, [(0.7, yb), (3.0, yb)])
    wire(ax, [(3.0, yt), (3.0, 2.85)])
    resistor(ax, 3.0, 2.85, 3.0, 1.15, '8 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(3.0, 1.15), (3.0, yb)])
    node(ax, 3.0, yb)
    mid = (3.0 + 5.9) / 2
    node(ax, mid, yt)
    wire(ax, [(mid, yt), (mid, 2.85)])
    resistor(ax, mid, 2.85, mid, 1.15, '8 Ω', lab_dx=0.34, lab_dy=0)
    wire(ax, [(mid, 1.15), (mid, yb)])
    node(ax, mid, yb)
    node(ax, 5.9, yt)
    node(ax, 5.9, yb)
    harrow(ax, 1.45, yt, True, BLUE, 'I', 12)
    save(fig, 'exam_blank')
