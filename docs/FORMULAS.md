# Formula specification

ATRP14 = ATR14 / previous_close * 100

drawdown_pct = (current_price / anchor_high - 1) * 100

shock_atr = abs(relevant_drawdown_pct) / ATRP14

recovery_pct = (target_price - entry_price) / (anchor_price - entry_price) * 100

Baseline targets: T1 = entry + 0.75 * ATR14; T2 = entry + 1.00 * ATR14; T3 = entry + 1.50 * ATR14.

profile_target = entry * (1 + target_return_pct / 100)

Show ATR-derived targets and profile-return target. Never silently replace one with the other.

Pre-event slope windows end at t-1 relative to shock/event day. Use linear-regression slopes on 5/20/50 closes and normalize daily percentage slope by ATRP14.

captured_recovery_pct = (exit - entry) / (anchor - entry) * 100

MFE = max favorable excursion after entry before close. MAE = max adverse excursion after entry before close.
