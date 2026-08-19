from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/top-losers")
def get_top_losers():
    try:
        url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?formatted=false&lang=en-US&region=US&scrIds=day_losers&count=200"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        results = data.get("finance", {}).get("result", [])
        if not results:
            return {"total_encontrados": 0, "top_losers": []}
            
        quotes = results[0].get("quotes", [])
        
        filtered_losers = []
        min_market_cap = 2_000_000_000  # $2.0 Billones USD
        
        for item in quotes:
            market_cap = item.get("marketCap", 0) or 0
            if market_cap >= min_market_cap:
                filtered_losers.append({
                    "ticker": item.get("symbol"),
                    "name": item.get("shortName") or item.get("longName"),
                    "price": item.get("regularMarketPrice"),
                    "change_percent": item.get("regularMarketChangePercent"),
                    "market_cap_usd": market_cap
                })
        
        return {
            "total_encontrados": len(filtered_losers),
            "top_losers": filtered_losers[:100]
        }
    except Exception as e:
        return {"error": str(e)}
