export type MarketSession = "PREMARKET" | "REGULAR" | "AFTER_HOURS" | "CLOSED";
export type Decision = "BUY" | "WAIT" | "PASS" | "VETO";
export type KnifeRisk = "LOW" | "MEDIUM" | "HIGH" | "VETO";
export type CatalystClass = "TEMPORARY_TECHNICAL" | "PERCEPTUAL_OVERREACTION" | "FUNDAMENTAL_REPAIRABLE" | "MIXED" | "STRUCTURAL" | "UNKNOWN";
export interface TradingProfile { targetReturnPct:number; marginEnabled:boolean; basePositionUsd:number; maxPositionUsd:number; minMarketCapUsd:number; minFallbackScore:number; maxTacticalSessions:number; t1AllocationPct:number; t2AllocationPct:number; runnerAllocationPct:number; }
export interface Candidate { symbol:string; companyName:string; price:number; session:MarketSession; sessionChangePct:number; marketCapUsd:number; atr14:number; atrp14:number; drawdown5dPct:number; drawdown10dPct:number; drawdown20dPct:number; shockAtr:number; fallbackScore:number; fallbackGrade:"A"|"B"|"TACTICAL_ONLY"|"REJECT"; knifeRisk:KnifeRisk; catalystClass:CatalystClass; hardVeto:boolean; decision:Decision; updatedAt:string; }
