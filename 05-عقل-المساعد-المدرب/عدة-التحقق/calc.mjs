#!/usr/bin/env bun
// calc.mjs — عدة التحقق الحسابي للمساعد (صفر تبعيات — bun/node فقط)
// الغرض: تحقق مزدوج لكل حل رقمي قبل تسليمه للطالب (بروتوكول الحل الموثوق)
// أمثلة: bun calc.mjs cdiv "3+4i" "1-2i"   |   bun calc.mjs msolve "[[2,1],[1,3]]" "[5,10]"

import { argv } from "process";

/* ---------------- المحلل النحوي (Recursive Descent) ---------------- */
const FUNCS = {
  sqrt: Math.sqrt, sin: Math.sin, cos: Math.cos, tan: Math.tan,
  asin: Math.asin, acos: Math.acos, atan: Math.atan,
  sind: (x) => Math.sin((x * Math.PI) / 180),
  cosd: (x) => Math.cos((x * Math.PI) / 180),
  tand: (x) => Math.tan((x * Math.PI) / 180),
  exp: Math.exp, ln: Math.log, log: Math.log10, abs: Math.abs,
  floor: Math.floor, ceil: Math.ceil, atan2: Math.atan2, pow: Math.pow,
};
const CONSTS = { pi: Math.PI, e: Math.E };

function tokenize(src) {
  const toks = [];
  let i = 0;
  while (i < src.length) {
    const c = src[i];
    if (c === " ") { i++; continue; }
    if (/[0-9.]/.test(c)) {
      let m = /^[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?/.exec(src.slice(i))[0];
      toks.push({ t: "num", v: parseFloat(m) }); i += m.length; continue;
    }
    if (/[a-zA-Z_]/.test(c)) {
      let m = /^[a-zA-Z_][a-zA-Z_0-9]*/.exec(src.slice(i))[0];
      toks.push({ t: "id", v: m }); i += m.length; continue;
    }
    if ("+-*/^(),".includes(c)) { toks.push({ t: c }); i++; continue; }
    throw new Error(`رمز غير معروف: '${c}'`);
  }
  return toks;
}

function parseExpr(src) {
  const toks = tokenize(src);
  let pos = 0;
  const peek = () => toks[pos];
  const eat = (t) => { if (toks[pos] && toks[pos].t === t) { pos++; return true; } return false; };

  function expr() {
    let node = term();
    while (peek() && (peek().t === "+" || peek().t === "-")) {
      const op = toks[pos++].t;
      node = { k: "bin", op, a: node, b: term() };
    }
    return node;
  }
  function term() {
    let node = unary();
    while (peek() && (peek().t === "*" || peek().t === "/")) {
      const op = toks[pos++].t;
      node = { k: "bin", op, a: node, b: unary() };
    }
    return node;
  }
  function unary() {
    if (eat("-")) return { k: "neg", a: unary() };
    if (eat("+")) return unary();
    return power();
  }
  function power() {
    const base = atom();
    if (eat("^")) return { k: "bin", op: "^", a: base, b: unary() }; // يمين-ترابطي
    return base;
  }
  function atom() {
    const tk = peek();
    if (!tk) throw new Error("تعبير ناقص");
    if (tk.t === "num") { pos++; return { k: "num", v: tk.v }; }
    if (tk.t === "(") { pos++; const n = expr(); if (!eat(")")) throw new Error("قوس غير مغلق"); return n; }
    if (tk.t === "id") {
      pos++;
      if (eat("(")) {
        const args = [expr()];
        while (eat(",")) args.push(expr());
        if (!eat(")")) throw new Error("قوس دالة غير مغلق");
        return { k: "call", f: tk.v, args };
      }
      return { k: "var", name: tk.v };
    }
    throw new Error(`غير متوقع: '${tk.t}'`);
  }
  const ast = expr();
  if (pos < toks.length) throw new Error(`رمز زائد عند: '${toks[pos].t}'`);
  return ast;
}

function evalAst(node, vars) {
  switch (node.k) {
    case "num": return node.v;
    case "var": {
      const name = node.name;
      if (vars && name in vars) return vars[name];
      if (name in CONSTS) return CONSTS[name];
      throw new Error(`متغير غير معروف: ${name}`);
    }
    case "neg": return -evalAst(node.a, vars);
    case "bin": {
      const a = evalAst(node.a, vars), b = evalAst(node.b, vars);
      if (node.op === "+") return a + b;
      if (node.op === "-") return a - b;
      if (node.op === "*") return a * b;
      if (node.op === "/") return a / b;
      if (node.op === "^") return Math.pow(a, b);
    }
    case "call": {
      if (!(node.f in FUNCS)) throw new Error(`دالة غير معروفة: ${node.f}`);
      return FUNCS[node.f](...node.args.map((x) => evalAst(x, vars)));
    }
  }
}
const compile = (src) => { const ast = parseExpr(src); return (vars) => evalAst(ast, vars); };

/* ---------------- الأعداد المركبة ---------------- */
function parseComplex(s) {
  const str = s.replace(/\s+/g, "").replace(/j/g, "i");
  const num = "[+-]?(?:\\d+\\.?\\d*|\\.\\d+)(?:[eE][+-]?\\d+)?";
  const re = new RegExp(`([+-]?[^+-]+)`, "g");
  let Re = 0, Im = 0, m;
  while ((m = re.exec(str)) !== null) {
    const p = m[1];
    if (/i$/.test(p)) {
      const coef = p.slice(0, -1);
      Im += coef === "" || coef === "+" ? 1 : coef === "-" ? -1 : parseFloat(coef);
    } else {
      if (!new RegExp(`^${num}$`).test(p)) throw new Error(`جزء غير مفهوم: '${p}'`);
      Re += parseFloat(p);
    }
  }
  if (str === "i" || str === "-i" || str === "+i") { Re = 0; Im = str.startsWith("-") ? -1 : 1; }
  return { Re, Im };
}
const cfmt = (z) => `${round(z.Re)} ${z.Im < 0 ? "-" : "+"} ${round(Math.abs(z.Im))}i`;
const round = (x) => {
  const r = Math.round(x * 1e6) / 1e6;
  return Number.isInteger(r) ? String(r) : String(r);
};
const cadd = (a, b) => ({ Re: a.Re + b.Re, Im: a.Im + b.Im });
const csub = (a, b) => ({ Re: a.Re - b.Re, Im: a.Im - b.Im });
const cmul = (a, b) => ({ Re: a.Re * b.Re - a.Im * b.Im, Im: a.Re * b.Im + a.Im * b.Re });
const cdiv = (a, b) => {
  const d = b.Re ** 2 + b.Im ** 2;
  return { Re: (a.Re * b.Re + a.Im * b.Im) / d, Im: (a.Im * b.Re - a.Re * b.Im) / d };
};

/* ---------------- المصفوفات ---------------- */
const parseMat = (s) => { const m = JSON.parse(s); if (!Array.isArray(m) || !m.every((r) => Array.isArray(r))) throw new Error("صيغة مصفوفة: [[a,b],[c,d]]"); return m; };
function gaussSolve(A0, b0) {
  const n = A0.length;
  const A = A0.map((r, i) => [...r, b0[i]]);
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
    if (Math.abs(A[p][c]) < 1e-14) throw new Error("المصفوفة مفردة (لا حل وحيد)");
    [A[c], A[p]] = [A[p], A[c]];
    for (let r = 0; r < n; r++) {
      if (r === c) continue;
      const f = A[r][c] / A[c][c];
      for (let k = c; k <= n; k++) A[r][k] -= f * A[c][k];
    }
  }
  return A.map((r, i) => r[n] / r[i]);
}
function mdet(A) {
  const n = A.length, M = A.map((r) => [...r]); let det = 1;
  for (let c = 0; c < n; c++) {
    let p = c;
    for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
    if (Math.abs(M[p][c]) < 1e-14) return 0;
    if (p !== c) { [M[c], M[p]] = [M[p], M[c]]; det = -det; }
    det *= M[c][c];
    for (let r = c + 1; r < n; r++) { const f = M[r][c] / M[c][c]; for (let k = c; k < n; k++) M[r][k] -= f * M[c][k]; }
  }
  return det;
}

/* ---------------- تحليل عددي ---------------- */
function simpson(f, a, b, N = 20000) {
  if (N % 2) N++;
  const h = (b - a) / N;
  let s = f(a) + f(b);
  for (let i = 1; i < N; i++) s += f(a + i * h) * (i % 2 ? 4 : 2);
  return (s * h) / 3;
}

/* ---------------- المقاومات ---------------- */
const rser = (xs) => xs.reduce((a, b) => a + b, 0);
const rpar = (xs) => 1 / xs.reduce((a, b) => a + 1 / b, 0);

/* ---------------- التنفيذ ---------------- */
const [cmd, ...rest] = argv.slice(2);
const A = (i) => rest[i];
try {
  switch (cmd) {
    case "eval": {
      const f = compile(A(0));
      const vars = {};
      for (let i = 1; i + 1 < rest.length; i += 2) vars[A(i)] = parseFloat(A(i + 1));
      console.log(round(f(vars))); break;
    }
    case "cadd": case "csub": case "cmul": case "cdiv": {
      const a = parseComplex(A(0)), b = parseComplex(A(1));
      const z = { cadd, csub, cmul, cdiv }[cmd](a, b);
      console.log(cfmt(z)); break;
    }
    case "cpolar": {
      const z = parseComplex(A(0));
      const r = Math.hypot(z.Re, z.Im), th = (Math.atan2(z.Im, z.Re) * 180) / Math.PI;
      console.log(`${round(r)} ∠ ${round(th)}°`); break;
    }
    case "crect": {
      const r = parseFloat(A(0)), th = (parseFloat(A(1)) * Math.PI) / 180;
      console.log(cfmt({ Re: r * Math.cos(th), Im: r * Math.sin(th) })); break;
    }
    case "msolve": {
      const A2 = parseMat(A(0)), b = JSON.parse(A(1));
      console.log(gaussSolve(A2, b).map(round).join("  ")); break;
    }
    case "mdet": console.log(round(mdet(parseMat(A(0))))); break;
    case "minv": {
      const M = parseMat(A(0)), n = M.length;
      const cols = [];
      for (let c = 0; c < n; c++) {
        const b = Array.from({ length: n }, (_, r) => (r === c ? 1 : 0));
        cols.push(gaussSolve(M, b));
      }
      const inv = Array.from({ length: n }, (_, r) => Array.from({ length: n }, (_, c) => cols[c][r]));
      console.log(inv.map((row) => `[${row.map(round).join(", ")}]`).join("\n")); break;
    }
    case "mmul": {
      const X = parseMat(A(0)), Y = parseMat(A(1));
      if (X[0].length !== Y.length) throw new Error("أبعاد غير متوافقة");
      const R = X.map((row) => Y[0].map((_, c) => row.reduce((s, v, k) => s + v * Y[k][c], 0)));
      console.log(R.map((row) => `[${row.map(round).join(", ")}]`).join("\n")); break;
    }
    case "sum": {
      const f = compile(A(0)), from = parseInt(A(1)), to = parseInt(A(2));
      let s = 0; for (let n = from; n <= to; n++) s += f({ n });
      console.log(round(s)); break;
    }
    case "integrate": {
      const f = compile(A(0)), a = parseFloat(A(1)), b = parseFloat(A(2));
      const N = A(3) ? parseInt(A(3)) : 20000;
      console.log(round(simpson((t) => f({ t }), a, b, N))); break;
    }
    case "deriv": {
      const f = compile(A(0)), at = parseFloat(A(1));
      const h = Math.max(1e-7, Math.abs(at) * 1e-7);
      console.log(round((f({ x: at + h }) - f({ x: at - h })) / (2 * h))); break;
    }
    case "laplace": {
      const f = compile(A(0)), s = parseFloat(A(1));
      if (s <= 0) throw new Error("للتحقق العددي استعمل s > 0");
      const T = Math.min(400, s >= 1 ? 40 / s + 10 : 40);
      console.log(round(simpson((t) => f({ t }) * Math.exp(-s * t), 0, T, 120000))); break;
    }
    case "rser": console.log(round(rser(rest.map(Number)))); break;
    case "rpar": console.log(round(rpar(rest.map(Number)))); break;
    default:
      console.log(`عدة التحقق — الأوامر:
  eval   <expr> [var val ...]     مثال: eval "2^3*sqrt(16)" | eval "x^2" x 5
  cadd/csub/cmul/cdiv "a+bi" "c+di"
  cpolar "a+bi"          → r∠θ°        crect <r> <θ°> → a+bi
  msolve "[[a,b],[c,d]]" "[e,f]"       minv "[[...]]"  mdet "[[...]]"  mmul A B
  sum    <expr n> <من> <إلى>           مثال: sum "1/2^n" 1 20
  integrate <expr t> <a> <b>           مثال: integrate "t^2" 0 2
  deriv  <expr x> <نقطة>              مثال: deriv "x^3" 2
  laplace <expr t> <s>                مثال: laplace "sin(t)" 2  (عددي للتحقق)
  rser <r1> <r2> ...   مقاومات تسلسل   rpar <r1> <r2> ...  توازي`);
  }
} catch (e) {
  console.error("خطأ:", e.message);
  process.exit(1);
}
