# Codex master prompt — Sell-Off Trader v2

You are implementing Sell-Off Trader v2, a private two-user mobile-first web app for tactical sell-off trading.

Read these files first and treat them as product requirements:
- README-v2.md
- docs/PRD.md
- docs/UX-UI.md
- docs/ARCHITECTURE.md
- docs/FORMULAS.md
- docs/CODEX-EXECUTION.md
- docs/DATA-MODEL.sql

Then execute Phase 1 from docs/CODEX-EXECUTION.md.

Non-negotiable rules:
1. Do not use an absolute minimum stock-drop percentage as a gate.
2. Use ATR/ATRP-normalized dislocation and 5D/10D/20D anchors.
3. Market cap >= $2B is a hard gate.
4. Structural business/regulatory damage, material distress, fraud/restatement, or unacceptable falling-knife risk can hard-veto a trade.
5. Falling-knife calculations must use trend data ending BEFORE the shock day.
6. Every BUY candidate must show entry, invalidation, position size, T1/T2/T3, expected return, recovery %, dollars, and proposed shares to sell.
7. A failed tactical trade never becomes a long automatically; it enters REUNDERWRITE.
8. Settings are per-user. One user is cash/no-margin with ~3% target and ~$30k base size; the other may use margin and a higher return target.
9. Mobile UX is first-class. Use Dashboard / Scanner / Trades / History / Settings only as primary navigation.
10. Tooltips must work by hover/focus on desktop and tap on mobile.
11. Always display data freshness and session state.
12. Every stock view/card/row must display 52-week Low, Current, High, and a proportional current-price marker within the 52-week range; also show % above low and % below high where space allows.
13. Start in mock mode and keep provider interfaces clean. Do not block Phase 1 on paid API keys.
14. No brokerage execution or auto-trading in the first release.
15. Do not expose service-role keys or market-data keys to client bundles.
16. Keep the UI calm and decision-first; avoid terminal-style density.

For every phase:
- make the smallest coherent implementation;
- run tests/typecheck/build;
- fix failures before moving on;
- summarize changed files and outstanding blockers;
- do not silently change formulas or thresholds; if a requirement seems wrong, flag it instead of rewriting it.

Phase 1 deliverable:
- working Next.js TypeScript app;
- responsive shell;
- mock Dashboard and Scanner;
- candidate detail page;
- Settings form with two example profiles;
- formula tooltips;
- 52-week range component on candidate cards/rows/detail;
- trade-plan card with proposed sell ladder;
- PWA manifest;
- tests for formulas;
- clean build.
