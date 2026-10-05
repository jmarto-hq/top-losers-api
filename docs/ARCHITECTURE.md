# Architecture

## Stack
Next.js App Router + TypeScript; Tailwind; Radix/shadcn; Supabase Auth + Postgres; Vercel + Cron; provider adapters for market/news.

## Provider rule
UI never calls vendors directly. Define MarketDataProvider(getUniverse/getSnapshot/getBars/getTickerDetails) and NewsProvider(getRecentNews). Start with mock providers, plug in live providers with environment switches.

## Jobs
Nightly 20:30 ET: universe, cap/liquidity, rolling indicators, fundamental cache, watch seeds.
Premarket 04:00–09:29 ET: 5-min universe/candidate scan; 1-min active shortlist if plan supports.
Regular 09:30–16:00 ET: 2–5 min scanner; 1-min watchlist/open trades.
After-hours 16:00–20:00 ET: 10-min updates; earnings/news.
Overnight: MFE/MAE, history compaction, archive.

Vercel cron is UTC; orchestrator resolves America/New_York market session and exchange holidays.

## Freshness
Every record stores source, source_timestamp, ingested_at, session, delayed flag and stale threshold. UI always shows freshness.

## Security
Supabase RLS by user_id. Service role server-only. Provider keys never in browser. Cron protected by CRON_SECRET. Audit manual veto overrides. No brokerage execution in v1.

## PWA
Installable responsive web app. No native mobile app until usage proves need.
