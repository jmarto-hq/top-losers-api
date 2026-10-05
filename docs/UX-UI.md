# UX / UI

## Principles
Decision-first. Progressive disclosure. Mobile first. Color is secondary. Every uncommon metric has an explanation. The app should answer "what deserves attention now?" within five seconds.

## Navigation
Mobile bottom nav / desktop left nav: Dashboard, Scanner, Trades, History, Settings.

## Mandatory 52-week context
Every stock representation must include a compact 52-week range visualization whenever space allows.

Minimum fields:
- 52W Low
- Current Price
- 52W High
- Current position within the 52W range

Preferred visual:
52W Low  ─────────●─────────  52W High
$XX.XX              $NOW       $YY.YY

The current-price marker must be positioned proportionally between the 52-week low and high.

On compact scanner rows, show a thin mini-range bar.
On candidate cards, show the full low/current/high bar.
On candidate detail, show the range near the top of the first viewport, before deep technical sections.

Also show:
- % above 52W low
- % below 52W high

Tooltip/tap explanation:
"Big picture: shows where today's price sits between the lowest and highest traded prices of the last 52 weeks. It is context, not a buy/sell signal by itself."

This component is mandatory because it prevents a one-day drop from being interpreted without longer-term context.

## Dashboard
Header: PREMARKET / OPEN / CLOSED; updated X sec ago; active profile chip such as Cash 3% or Margin 6%.
Best setups: 3–5 cards ranked by opportunity. Card fields: ticker, price, session change, 52-week range bar, shock ATR, fallback grade, knife risk, catalyst, decision, one-line reason.
Open trades show only action-relevant data: current return, next target, target distance, invalidation, days in trade, status.
Alerts: T1 hit, entry zone, structural veto, stale data, mandatory review.

## Scanner
Desktop table; mobile cards. Default fields: Ticker, Decision, Price, 52W Range, Day %, Shock ATR, 5D DD, 20D DD, Fallback, Knife, Catalyst, User Target, T1, T2, Updated.
Compact filters. Saved views: Best now; Premarket; Panic; Small but abnormal; Watch/wait; Vetoed.

## Candidate detail
First viewport: ticker/price/session/freshness; 52-week range; Why now? Best reason NOT to buy. Entry/invalidation. Proposed sell orders.
Below: Sell-off anatomy; Trend/knife; Fallback quality; News/catalyst; Chart; Fundamentals; Audit trail.

## Tooltips
Every formula has an info icon. Desktop hover/focus; mobile tap. Structure: plain-English meaning; formula; why it matters; example.
ATRP tooltip: "Typical daily trading range as a % of price. It lets us compare a 2% move in a stable stock with a 2% move in a volatile stock."

## Settings
Trading profile: target return %, margin on/off, base position $, max position $, max tactical days.
Risk: min fallback score, allowed knife risk, min market cap, max loss per trade.
Exit: T1/T2/runner allocations and profit-protection mode.
Notifications: entry zone, T1/T2, structural veto, stale data, mandatory review.

## Accessibility
No red/green-only meaning. Keyboard navigable. 44px touch targets. WCAG AA target. Tooltips accessible without mouse.

## Benchmark takeaways
Use watchlist/table scanning patterns similar to Koyfin, flexible screening like TradingView, fast overview/filtering like Finviz. Avoid terminal density, 20+ above-fold metrics, unexplained scores and hidden stale-data state.
