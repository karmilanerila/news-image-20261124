# The World Today — Tuesday, 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/karmilanerila/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/karmilanerila/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124)

An editorial front page summing up the world's news of Tuesday, 24 November
2026, for the make.fun news-image bounty. `main.py` (Python 3.13 standard
library only, no network) draws the page as a 1024x1024 PNG and writes it to
`/output/entry.png` (plus a byte-identical copy at `/output/cover.jpg`).

Referral: `h379tqrk`

## The five stories

1. **Ukraine — peace talks (lead).** Zelensky presses allies in Stockholm as
   Trump's 28-point peace plan splits Europe; Kyiv rejects any deal that hands
   Russia the land it seized.
2. **Venezuela.** The US designates the Cartel de los Soles a foreign
   terrorist organisation; US strikes on alleged drug boats pass 21 since
   September.
3. **Tech.** Jensen Huang returns as Nvidia chief executive after Trump
   intervenes, as the chipmaker faces a US securities regulator inquiry.
4. **United States.** Trump halts the Army's plan to blow up five tonnes of
   unstable lead azide at an Iowa munitions plant until a court and the
   incoming governor agree.
5. **Spain.** The Supreme Court drops all charges against Catalan leader
   Carles Puigdemont under an amnesty law, days before the general election.

Sources: CBC News, CNN, France 24, Daily Caller, TASR.

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png (1024x1024 PNG) and out/cover.jpg (identical bytes)
```

The program is deterministic: two runs write byte-identical files.

## License

MIT — see `LICENSE`.
