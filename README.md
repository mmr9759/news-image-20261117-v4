# news-image-20261117-v4 — THE WORLD TODAY

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/c/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/mmr9759/news-image-20261117-v4/rank.svg)](https://make.fun/c/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/mmr9759/news-image-20261117-v4/reward.svg)](https://make.fun/c/news-image-20261117)

One front page summing up the world's news of Tuesday 17 November 2026:
40 real stories from six continents, a lead illustration of the Kerch Bridge
road span falling into the strait, a world map with numbered pins, and a
number strip (Nvidia $115.8bn, 1,441 drones, 5 ships mined in Hormuz).

The entry is a pure-stdlib Python 3.13 program (`main.py`, no network, no
model calls). It draws the 1024x1024 front page with its own 5x7 bitmap font
and PNG encoder, and writes it deterministically to `/output/entry.png`
(two runs byte-identical, well under the 1 MiB cap).

Run it: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
