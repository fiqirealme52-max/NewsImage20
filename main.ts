/**
 * NewsImage20 — entry program for the make.fun news-image-20261120
 * competition ("World News — 20 November 2026").
 *
 * The picture is drawn ahead of time by draw.py and shipped as entry.png
 * next to this file. This program only copies those exact bytes into the
 * output directory, after two sanity checks: the file must start with the
 * PNG signature and must fit inside the competition's 1 MiB cap.
 *
 * Deterministic by construction: the same input bytes always produce the
 * same output bytes. No network, no clock, no randomness, standard library
 * only (node:fs and node:path).
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024; // 1 MiB, the competition limit

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const bytes = readFileSync(source);

if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error("entry.png does not start with the PNG magic bytes");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, bytes);

// One line on stdout so a run's result is visible in the grader log.
console.log(`Wrote ${target} (${bytes.length} bytes, sha256 ${createHash("sha256").update(bytes).digest("hex").slice(0, 16)}…)`);
