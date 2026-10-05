export function atrp(atr:number, previousClose:number){ if(previousClose<=0) throw new Error("previousClose must be > 0"); return atr/previousClose*100; }
export function drawdownPct(current:number, anchorHigh:number){ if(anchorHigh<=0) throw new Error("anchorHigh must be > 0"); return (current/anchorHigh-1)*100; }
export function shockMultiple(drawdownPercent:number, atrpPercent:number){ if(atrpPercent<=0) throw new Error("ATRP must be > 0"); return Math.abs(drawdownPercent)/atrpPercent; }
export function recoveryPct(entry:number,target:number,anchor:number){ const d=anchor-entry; if(d===0) throw new Error("anchor and entry cannot be equal"); return (target-entry)/d*100; }
export function atrTargets(entry:number,atr:number){ return {t1:entry+.75*atr,t2:entry+atr,t3:entry+1.5*atr}; }
export function profileTarget(entry:number,targetReturnPct:number){ return entry*(1+targetReturnPct/100); }
