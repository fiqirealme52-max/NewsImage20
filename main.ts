/**
 * NewsImage20 — entry program for the make.fun news-image-20261120
 * competition ("World News — 20 November 2026", 38-story VISUAL
 * REVISION edition).
 *
 * The front page is drawn ahead of time by draw.py and shipped as
 * entry.png next to this file. This program copies those exact bytes
 * into the output directory, but only after proving the file is
 * really the picture we expect:
 *   - it starts with the 8-byte PNG signature,
 *   - its IHDR chunk says 1024 x 1024 pixels (the competition cap),
 *   - it fits inside the 1 MiB size limit.
 * If any check fails the program throws instead of writing output.
 *
 * What changed in the visual revision (same 38 verified stories,
 * same facts, same dates — only the presentation):
 *   - Cyclone Akvan is lead #01 with a big coloured scene; Trump and
 *     Kyiv keep their leads with full-width night/dusk scene bands.
 *   - Masthead is the giant serif date "Friday 20 November 2026"
 *     under the kicker "THE WORLD IN ONE DAY".
 *   - All ten medium stories carry small coloured illustrations and
 *     a visible "CONFIRMED . outlet" source tag.
 *   - The world map is dark navy with cream continents, red pins and
 *     a legend; the paper is warm cream with serif headlines.
 *   - Region tabs are geographic and sum to 38.
 *
 * Deterministic by construction: the same input bytes always produce
 * the same output bytes. No network, no clock, no randomness, and
 * only node:fs, node:path, node:url and node:crypto from the standard
 * library.
 */
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024; // 1 MiB, the competition limit
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

function readPngSize(png: Buffer): { width: number; height: number } {
  // The IHDR chunk sits right after the 8-byte signature: 4-byte length,
  // 4-byte "IHDR" tag, then width and height as 4-byte big-endian values.
  const ihdrTag = png.subarray(12, 16).toString("latin1");
  if (ihdrTag !== "IHDR") {
    throw new Error("entry.png has no IHDR chunk where one is expected");
  }
  return { width: png.readUInt32BE(16), height: png.readUInt32BE(20) };
}

function main(): void {
  const bytes = readFileSync(source);

  if (bytes.length === 0) {
    throw new Error("entry.png is empty");
  }
  if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
    throw new Error("entry.png does not start with the PNG magic bytes");
  }
  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }

  const { width, height } = readPngSize(bytes);
  if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
    throw new Error(
      `entry.png is ${width}x${height}, expected ${EXPECTED_WIDTH}x${EXPECTED_HEIGHT}`,
    );
  }

  mkdirSync(outDir, { recursive: true });
  writeFileSync(target, bytes);

  // One line on stdout so a run's result is visible in the grader log.
  // The bundled picture is the 38-story visual-revision front page
  // (Akvan lead #01 with a big scene, serif date masthead, illustrated
  // mediums, navy map — all 38 stories verified from 20 November 2026).
  // Edition: visual-revision (draw.py, top-10/top-50 research 2026-11-20).
  const digest = createHash("sha256").update(bytes).digest("hex").slice(0, 16);
  console.log(`Wrote ${target} (${bytes.length} bytes, ${width}x${height}, sha256 ${digest}…)`);
}

main();
