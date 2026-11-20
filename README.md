# NewsImage20

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/fiqirealme52-max/NewsImage20/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/fiqirealme52-max/NewsImage20/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page that sums up the world's news of **Friday 20 November 2026** in one 1024×1024 image — **38 stories**: a giant serif date masthead ("Friday 20 November 2026" under the kicker "THE WORLD IN ONE DAY"), a six-number strip, geographic region tabs (World 1 · Europe 8 · Americas 7 · Asia-Pacific 10 · Mideast 6 · Africa 3 · Oceania 3), three big scene-illustrated leads (Cyclone Akvan #01, Trump, Kyiv), ten medium stories with small coloured illustrations and visible "CONFIRMED · outlet" source tags, a dark navy world map with 13 numbered pins and a legend, an "Also on Friday" list of 25 more stories, a DATE CHECK box naming the other-day stories deliberately left out, a HOW SURE line, and a sources footer. Every fact comes only from sources dated 20 November 2026.

## The thirteen featured stories

1. **Cyclone Akvan hits Odisha** — 300,000 evacuated as the storm makes landfall on the coast.
2. **Trump delays Iran decision** — no rush on war; he will "see what happens" after 1 January and decide in 2027.
3. **Missiles hit Kyiv overnight** — Russia fires nearly 20 ballistic missiles at Kyiv; bridges are hit, fires burn in several districts; a three-storey building in Obolonskyi catches fire; no casualties reported at first. (Reuters, Kyiv Independent, Daily Baku, 20 Nov 2026.)
4. **COP31 drops fossil-fuel phase-out** — the climate summit closes in Antalya, but the final draft drops the call to phase out fossil fuels, sparking outcry.
5. **Wall Street sinks** — Dow falls below 50,000 to 49,097; S&P 500 −2.02% (fifth straight loss), Nasdaq −2.25% as the AI selloff deepens.
6. **5.6 quake near New Caledonia** — a 5.6-magnitude quake strikes 548 km south-east of Nouméa, 10 km deep.
7. **US war with Iran cost $48bn** — the Pentagon says the US war with Iran has cost over $48 billion so far.
8. **Pochettino joins United** — new Manchester United head coach calls for unity in his first address; United are 18th, first match Liverpool at Anfield on Sunday.
9. **India v NZ, day 2** — Nicholls' unbeaten 175 and Phillips' 118 lift New Zealand to 368 all out; India reach 52 without loss. (ESPNcricinfo, Reuters, 20 Nov 2026.)
10. **ASEAN summit closes** — digital trade deal sealed; sea code still unresolved.
11. **Haiti troop deal** — Salvadoran troops approved as gang strikes widen.
12. **GTA VI's NPCs** — the crowd that makes the game's huge world feel real. (NPR.)
13. **Justice Varma's letter** — resignation is no admission of guilt, he says.

## Also on Friday — 25 more stories

14. Bavuma ruled out (calf; misses the Centurion decider). 15. Carlsen forfeit. 16. Oman National Day, 56 years. 17. Harris meets Macron in Paris. 18. Congress faces a Dec 11 funding cliff and a crowded lame-duck list. 19. Japan core inflation 2.2% in October. 20. Telus shares jump 12% as a bidding war brews over Quebecor's C$31bn bid. 21. Kharkiv hospital drone strike, 4 injured. 22. Dorogobuzh chemical plant drone attack. 23. Cyclone Xavier: gale warning Suwarrow, storm alert Pukapuka. 24. BBC speaks to people in a besieged Yemeni city. 25. Africa wants $120bn a year to adapt; Europe says spend the money already pledged. 26. Jepchirchir three-year EPO ban. 27. Phillips centuries in all three formats vs India in one year. 28. Mhambrey in talks with Punjab Kings. 29. Dhoni Room No. 7 opens in Chennai. 30. Vasco da Gama 2-1 Internacional; Vitória 2-1 Bragantino. 31. Alcaraz faces Cobolli at the ATP Finals. 32. East Bengal host SC Delhi in the ISL on Friday. 33. Saudi defences destroy two Houthi drones. 34. Bengaluru host Mumbai City in the ISL. 35. UK and EU agree a Brexit reset in Brussels — 100,000 youth visas, food checks eased. 36. White House taps Kirsten Davies as cyber chief. 37. 13,000 protest in Tokyo against the Takaichi government. 38. Houthis claim drone and missile strikes on four Saudi targets.

## DATE CHECK — deliberately excluded (other days)

ICJ Rohingya ruling (19 Nov) · Trump–Xi–Putin peace declaration (19 Nov) · Crimean Bridge strike (19 Nov) · Anthropic IPO debut (19 Nov) · Gaza tank raid (18–19 Nov) · SAFF final (17 Nov) · Nvidia subpoena (19 Nov) · Fiona dies (19 Nov) · Denmark–Greenland deal (19 Nov) · Save the Children report (19 Nov) · Berlin summit (19 Nov) · Mélenchon–Greens (18 Nov).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` after checking the PNG magic bytes, the 1024×1024 IHDR dimensions and the 1 MiB size limit. `draw.py` (Python 3 + PIL) regenerates the image from scratch if you want to redraw it.

## Determinism

The program is deterministic: it copies fixed bytes, uses no network, no clock and no randomness, so repeated runs write byte-identical output. `draw.py` is likewise deterministic — two runs produce a byte-identical `entry.png`.

<sub>Entered on [make.fun](https://make.fun/?ref=vfa7ye18&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
