# Product Requirements Document

## Users
Two private users.

User A: no margin; smaller frequent tactical returns; default target ~3%; base unit ~$30k.
User B: margin enabled; larger target return and risk budget; same quality gates with different trade-plan parameters.

All calculations use the signed-in user's profile.

## Goal
Surface a short list of U.S.-listed stocks experiencing abnormal sell-offs, explain why each qualifies or fails, and output an executable plan including proposed sell orders.

## Hard gates
No BUY when market cap < $2B; material distress/bankruptcy risk; going-concern warning; default/covenant breach; fraud/restatement/material accounting crisis; delisting risk; structural regulatory damage; permanent core earnings-power impairment; unacceptable falling-knife state; or stale/insufficient data.

## Fallback quality 0–100
solvency/balance 25; business durability 20; structural-news safety 20; trend/knife quality 15; valuation/earnings support 10; liquidity/market cap 10.

85–100 A; 75–84 B; 65–74 Tactical only; <65 Reject. Hard veto overrides score.

## Sell-off anomaly
No absolute % decline threshold. Compute ATR14, ATRP14, day shock/ATRP, and 5D/10D/20D drawdown/ATRP.

Research buckets: <0.75 normal; 0.75–1.20 pullback; 1.20–1.50 dislocation; 1.50–2.50 preferred sell-off; 2.50–3.50 panic; >3.50 extreme with stronger structural review.

## Falling knife
Use data ending BEFORE current shock: 5D/20D/50D slope; normalized slope / ATRP; MA20/50/200; repeated new lows; relative trend vs sector/SPY; estimate revisions when available. Risk LOW / MEDIUM / HIGH / VETO.

## Catalyst
TEMPORARY_TECHNICAL; PERCEPTUAL_OVERREACTION; FUNDAMENTAL_REPAIRABLE; MIXED; STRUCTURAL; UNKNOWN. STRUCTURAL => VETO unless explicit audited override.

## Trade plan
Baseline T1 ~ Entry + 0.75 ATR; T2 ~ Entry + 1.00 ATR; T3 ~ Entry + 1.50 ATR or nearest valid resistance/anchor. Show price, return, recovery %, dollars and shares for each exit. Initial research allocation 40% / 40% / 20%.

## Post-entry
Invalidation before entry; tighten profit protection after T1/material rebound; day 5 review; session 10–14 mandatory review; ~28 sessions max unless explicitly re-underwritten.

## Re-underwrite
A failed trade never becomes a long automatically. Require intact fundamentals, no structural change, fallback still passes, valuation supports 12–24 month thesis, and user would buy from zero today.

## Learning loop
Store exact entry time, session, size, ATRP, shock, drawdowns, knife/fallback scores, catalyst, targets, exits, MFE, MAE, time-to-target, recovery captured and opportunity left after exit.
