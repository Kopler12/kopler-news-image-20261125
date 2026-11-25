// The World Today — entry for make.fun news-image-20261125.
// The image is drawn once (see render.py) and shipped beside this file as
// entry.png; this program's only job is to place that exact image at the
// path the grader reads. It runs offline and writes identical bytes on
// every run, because it copies the same file every time.
//
// Node 22, standard library only. Outside the grader's container,
// MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const image = readFileSync(new URL('./entry.png', import.meta.url));

mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), image);
