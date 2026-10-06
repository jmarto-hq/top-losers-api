# Top Losers API — Sell-Off Trader

`GET /top-losers` preserves Yahoo Finance `day_losers` order, filters market cap >= USD 2B and returns **up to 250** rows. Existing `total_encontrados`, `top_losers`, `price` and `change_percent` remain compatible. Added fields report fetch time, available source timestamps, regular-session basis, upstream/invalid counts and unknown feed delay. Never substitute another screener on failure. Zero eligible usable rows returns an explicit upstream error.

`GET /quotes?symbols=PEP,AMAT` returns available one-minute bars grouped into REGULAR/PRE/POST for up to 20 symbols. Extended-session data is not a pre-market universe screener, has no guaranteed latency and is never substituted for regular prices. Missing sessions remain null; per-symbol failures are explicit. Percent changes identify their reference price. Yahoo access can be rate-limited or unavailable.

`GET /health` reports version and maximum rows. Every data request fetches Yahoo on demand; no cron or persistent cache is configured here. HTTP errors and timeouts are distinct from successful data.

Run regression tests: `python -m unittest discover -s tests -v`.

For Sites: persist the canonical universe snapshot; refresh quotes separately for watchlist symbols; show both fetch time and price/bar time. Run unattended updates through authenticated Site service access and keep secrets out of browser code.
