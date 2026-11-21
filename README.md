# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/sayaaku12/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/sayaaku12/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

**The World in One Page** — a program that draws one image summing up Saturday 21 November 2026 world news as a newspaper front page, to `/output/entry.png`.

## What it is

A 1024×1024 broadsheet front page. One lead story, four grid stories, one wide band, and an "Also today" strip — the day's news as reported by mid-day 21 November 2026 (WIB).

**Lead — Russian missiles land in Poland as Ukraine is pounded.** Russia fired 400+ drones and 110+ missiles at Ukraine overnight — the largest strike of November 2026 — killing at least eight in Kyiv. Two Kh-101 missiles and a suspected jet drone came down in Poland; PM Tusk called it a deliberate provocation and NATO's Rutte a grave violation. (AP, ISW, OneTurn)

**Grid 1 — AI sell-off pushes the S&P 500 into correction.** US stocks fell 3.7% on Friday; the Nasdaq erased its 2026 gains; Anthropic slid ~11% a day after its record IPO; the Nikkei fell 5%+. (BBC, Guardian, UPI via OneTurn)

**Grid 2 — Magnitude 6.7 quake shakes central Peru.** A strong quake in the Junin Andes, felt in Lima 320 km away; no damage or casualties reported at first. (Straits Times, The Hindu, Daily Short/IGP via OneTurn)

**Grid 3 — Pill hailed as a pancreatic cancer breakthrough.** Trial pill daraxonrasib made tumours undetectable in 1 in 12 patients; nearly all saw tumours stop growing; experts call it the biggest breakthrough in decades. (Guardian, BBC via OneTurn)

**Grid 4 — GTA VI earns $3.8B on its first day.** Rockstar says day-one sales beat every game launch and single-day film box-office record. The game came out on 18 November. (BBC, Guardian, Le Monde via OneTurn)

**Band — Gulf: Houthi missiles aimed at Riyadh shot down.** The Saudi-led coalition shot down three Houthi ballistic missiles headed for Riyadh, the third night of alerts; Iran says it downed a US MQ-9 drone over Hormuz as talks stall. (Al Jazeera, Middle East Eye, Japan Times via OneTurn)

**Also today:** COP31 climate talks run past deadline over fossil fuels; the UK and EU sign their biggest post-Brexit agreements in Brussels; BepiColombo reaches Mercury orbit after eight years in space; the FBI crime database is reportedly hacked and Trump fires his cyber chief; Trump defends ties to Putin and Xi while Zelensky calls Putin "a killer"; a man is convicted of starting the deadly Palisades fire (12 killed, 6,800 buildings).

## How it was built

The front page is drawn entirely in code with Pillow — off-white broadsheet, ink type, one red accent, a navy band, no gradients, no glow, no emoji. Layout: masthead, lead block, 2×2 grid, wide band, "Also today" strip, footer. Every summary's full glyph box must end at least 5px inside its cell, so no text is ever clipped.

`main.py` (128 lines, standard library only, no network) is the repo entrypoint: it copies the bundled `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`) with a pinned SHA-256 guard, so the bytes it writes are exactly the bytes that were measured.

## Tests

- `python3 main.py --self-test` passes: the program runs twice into fresh temp dirs and both outputs are byte-identical.
- `python3 -m py_compile main.py` passes.
- No network calls in `main.py` (no socket, urllib, requests, http.client, subprocess, or os.system).

## Measured

- Output: 1024×1024 PNG, 142,922 bytes (limit 1,048,576)
- SHA-256: `4dba1d2b679151360f9e6792701bd61e1bcb121e1d8ebf7b9912359137cb1963`
- Determinism: two runs byte-identical, same SHA-256

## Run it

```sh
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=c0tz9ttj&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
