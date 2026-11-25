# The World Today — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Kopler12/kopler-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Kopler12/kopler-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image that sums up the world's news of **Wednesday 25 November 2026** — a
newspaper front page with the six stories that defined the day, drawn
programmatically with Python + Pillow (`render.py`) and shipped as `entry.png`.

## The six stories

1. **Space · China** — China launches Shenzhou-24; the crew rocket lifts off
   from Jiuquan with a Pakistani astronaut aboard, bound for the Tiangong station.
2. **Security · NATO** — NATO vows to defend space, answering reports that Russia
   is readying a nuclear-armed satellite, possibly for launch in December.
3. **Colombia · Cartagena** — Gunmen seize hostages in a supermarket after a
   failed armoured-truck robbery; five elderly women are released.
4. **Pacific · Solomon Islands** — The Solomon Islands picks Australia: a security
   pact names Australia the islands' top partner and rules out foreign military bases.
5. **South Korea · Seoul** — Education minister Choi Kyo-jin quits over a national
   exam-cheating scandal.
6. **Trade · Washington** — Trump plans new tariffs on goods from 16 trading
   partners after a trade investigation ends.

Compiled from wire reports (AP, Reuters, BBC, NOS) published on 25 November 2026.

## How it works

`main.ts` (Node 22, standard library only) copies `entry.png` to
`/output/entry.png`. The program runs with no network and writes the same bytes
on every run. The image is a 1024×1024 PNG, 113,731 bytes — inside the
competition's 1 MiB / 1024×1024 limits.

```sh
# regenerate the image
python3 render.py

# run the entry locally
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Entry

- Competition: [news-image-20261125](https://make.fun/bounty/news-image-20261125)
  — "Sum up 25 November's world news in one image"
- License: MIT
