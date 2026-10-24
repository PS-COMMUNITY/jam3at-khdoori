import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

const CHUNK_DIR = '/tmp/asr_chunks';
const OUT_DIR = '/tmp/asr_results';

process.on('unhandledRejection', (r) => console.log('[UNHANDLED]', String(r).slice(0, 120)));
process.on('uncaughtException', (e) => console.log('[UNCAUGHT]', String(e).slice(0, 120)));

const numChunks = 86;
const zai = await ZAI.create();
let consecutive429 = 0;

for (let i = 0; i < numChunks; i++) {
  const id = String(i).padStart(3, '0');
  const f = `${CHUNK_DIR}/c_${id}.wav`;
  const out = `${OUT_DIR}/t_${id}.json`;

  if (fs.existsSync(out) && fs.readFileSync(out, 'utf8').includes('"text"')) continue;
  if (!fs.existsSync(f)) continue;

  let done = false;
  for (let attempt = 0; attempt < 5 && !done; attempt++) {
    try {
      const b64 = fs.readFileSync(f).toString('base64');
      const resp = await zai.audio.asr.create({ file_base64: b64 });
      const text = resp.text || '';
      fs.writeFileSync(out, JSON.stringify({ chunk: i, start: i * 28, text }));
      console.log(`[OK] ${i}: ${text.slice(0, 50)}`);
      done = true;
      consecutive429 = 0;
      await new Promise(r => setTimeout(r, 4000));
    } catch (e) {
      const msg = String(e.message || e);
      if (msg.includes('429') || msg.toLowerCase().includes('too many')) {
        consecutive429++;
        const wait = Math.min(20000 + consecutive429 * 10000, 60000);
        console.log(`[429] ${i} attempt ${attempt}, waiting ${wait / 1000}s`);
        await new Promise(r => setTimeout(r, wait));
      } else {
        console.log(`[ERR] ${i} attempt ${attempt}: ${msg.slice(0, 90)}`);
        await new Promise(r => setTimeout(r, 6000));
      }
    }
  }
  if (!done) {
    fs.writeFileSync(out, JSON.stringify({ chunk: i, start: i * 28, text: '', error: true }));
    await new Promise(r => setTimeout(r, 5000));
  }
}
console.log('ALL DONE');
