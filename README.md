# NewsImage20

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/fiqirealme52-max/NewsImage20/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/fiqirealme52-max/NewsImage20/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page that sums up the world's news of **Friday 20 November 2026** in one 1024×1024 image: a lead story on Trump's delayed Iran decision, a second lead on the overnight missile attack on Kyiv, plus nine more stories from weather, politics, culture and sport — each numbered, with a section label, a small drawn illustration, a bold headline and a 2–3 line body, plus an IN BRIEF strip recapping all eleven stories.

## The eleven stories

1. **Trump delays Iran decision** — no rush on war; he will "see what happens" after 1 January and decide in 2027.
2. **Missiles hit Kyiv overnight** — Russia launches a mass missile attack on Kyiv overnight; fires burn in several districts; a three-storey building in Obolonskyi catches fire after missile debris hits it; no casualties reported at first. (Reuters, Kyiv Independent, 20 Nov 2026.)
3. **Cyclone Akvan hits Odisha** — 300,000 evacuated as the storm hits the coast.
4. **Justice Varma's letter** — resignation is no admission of guilt, he says.
5. **ASEAN summit closes** — digital trade deal sealed; sea code still unresolved.
6. **Haiti troop deal** — Salvadoran troops approved as gang strikes widen.
7. **GTA VI's NPCs** — the crowd that makes the game's huge world feel real.
8. **India v NZ, day 2** — Nicholls' unbeaten 113 builds New Zealand's lead.
9. **Bavuma ruled out** — Proteas captain misses the Bangladesh series decider.
10. **Carlsen forfeit** — shock walkout leaves the chess world fuming.
11. **Oman National Day** — the Sultanate marks 56 years of independence.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG magic bytes, the 1024×1024 IHDR dimensions and the 1 MiB size limit. `draw.py` (Python 3 + PIL) regenerates the image from scratch if you want to redraw it.

## Determinism

The program is deterministic: it copies fixed bytes, uses no network, no clock and no randomness, so repeated runs write byte-identical output.

<sub>Entered on [make.fun](https://make.fun/?ref=vfa7ye18&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
