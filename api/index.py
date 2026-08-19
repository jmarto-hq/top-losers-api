from fastapi import FastAPI
import yfinance as yf

app = FastAPI()

@app.get("/top-losers")
def get_top_losers():
    try:
        # Consultar el screener de caídas de Yahoo Finance
        screener = yf.Screener()
        data = screener.get_screeners(["day_losers"], count=100)
        
        quotes = data.get("day_losers", {}).get("quotes", [])
        
        filtered_losers = []
        # Umbral: 2.5 Billion USD (2,500,000,000)
        min_market_cap = 2_500_000_000 
        
        for item in quotes:
            market_cap = item.get("marketCap", 0) or 0
            if market_cap >= min_market_cap:
                filtered_losers.append({
                    "ticker": item.get("symbol"),
                    "name": item.get("shortName"),
                    "price": item.get("regularMarketPrice"),
                    "change_percent": item.get("regularMarketChangePercent"),
                    "market_cap_usd": market_cap
                })
        
        # Devolver los primeros 25 resultados filtrados
        return {
            "total_encontrados": len(filtered_losers),
            "top_losers": filtered_losers[:25]
        }
    except Exception as e:
        return {"error": str(e)}
