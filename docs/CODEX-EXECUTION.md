# Codex execution plan

## Mission
Turn this branch into a deployable private web app without changing core rules in PRD.md.

## Phase 1
Convert legacy root to Next.js TypeScript; Tailwind + Radix/shadcn; responsive 5-tab shell; mock market/news providers; Dashboard/Scanner/Trades/History/Settings; formula tooltips; PWA manifest; tests for formulas; lint/typecheck/test/build passing.

## Phase 2
Supabase email/password; create profile on first login; RLS; persist settings/candidates/trades/exits.

## Phase 3
Live MarketDataProvider behind env switch; source timestamp + delayed state; ATR14/ATRP; 5/10/20D anchors; pre-event slopes; stale warnings.

## Phase 4
Hard gates; fallback quality; knife risk; tactical score; adaptive target engine; saved scanner views.

## Phase 5
NewsProvider; structural classification explicit/auditable; UNKNOWN cannot auto-BUY.

## Phase 6
Protected idempotent jobs: /api/jobs/refresh-universe, /premarket, /regular, /afterhours, /nightly, /orchestrator.

## Phase 7
History analytics: win rate, expectancy, return distribution, shock ATR buckets, entry-time buckets, recovery captured, fallback grade, MFE/MAE.

## Constraints
No brokerage execution/auto-trading initially. No absolute minimum drop %. Never hide stale data. Structural veto overrides score. Trade never becomes long automatically. Every BUY has sell orders. Settings per-user. Mobile one-hand usable.

## First usable build done when
Login works; two profiles differ; scanner renders; candidate detail has required metrics; BUY includes entry/invalidation/sell ladder; manual trade lifecycle works; exact timestamps stored; jobs run; PWA installs; no client secret leakage.
