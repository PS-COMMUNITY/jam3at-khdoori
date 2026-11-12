#!/bin/bash
# تحويل المرجع إلى PDF — خط الأنابيب المجرّب: نسخ → تبديل الخط → إعادة الضغط → LibreOffice
set -e
SRC="/tmp/my-project/ref_out/المرجع-التفاعلي-الدوائر-الكهربائية.docx"
WORK="/tmp/my-project/ref_out/pdfwork"
OUTP="/tmp/my-project/ref_out/المرجع-التفاعلي-الدوائر-الكهربائية.pdf"

rm -rf "$WORK"; mkdir -p "$WORK"
cp "$SRC" "$WORK/doc.docx"
cd "$WORK"
unzip -q doc.docx -d extracted
# تبديل Arial (Liberation المحلي بلا حروف عربية كافية) بـ DejaVu Sans (يدعم العربية)
for f in extracted/word/document.xml extracted/word/styles.xml extracted/word/fontTable.xml extracted/word/settings.xml; do
  if [ -f "$f" ]; then
    sed -i 's/Arial/DejaVu Sans/g' "$f"
  fi
done
cd extracted && zip -q -r -X ../doc-pdftarget.docx . && cd ..
soffice --headless --convert-to pdf --outdir "$WORK" doc-pdftarget.docx >/dev/null 2>&1
mv "$WORK/doc-pdftarget.pdf" "$OUTP"
pdfinfo "$OUTP" | grep -E "Pages|Page size|File size"
echo "PDF DONE: $OUTP"
