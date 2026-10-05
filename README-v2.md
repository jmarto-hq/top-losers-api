# Sell-Off Trader v2 — Private Web App

Private two-user web app for tactical sell-off detection, fallback quality, falling-knife control, and precomputed exit orders.

## Product thesis
Do not buy because a stock fell a lot. Buy when the move is abnormal relative to the stock's own volatility, the business passes quality/survival checks, structural damage is absent, and the exit plan is defined before entry.

## Navigation
Dashboard · Scanner · Trades · History · Settings

## Profiles
Each user has independent target return, margin mode, position size, quality thresholds and exit behavior.

## Stack
Next.js + TypeScript · Supabase Auth/Postgres · Vercel · provider adapters for market/news data.

## Development order
1. Mock-mode UX.
2. Supabase auth/persistence.
3. Live market data.
4. Live news/structural veto.
5. Scheduler.
6. Backtest against 2026 trades.
7. Refine thresholds from actual expectancy.

See docs/ for PRD, UX, formulas, data model and Codex execution plan.
