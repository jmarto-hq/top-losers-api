"""Yahoo-backed market data with explicit sessions; canonical universe stays unchanged."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from math import isfinite
import re
from api.data import DataError, MAX_ROWS, now_iso, universe_payload, chart_quote
from fastapi.responses import JSONResponse
import requests
from fastapi import FastAPI, HTTPException, Query, Response

app = FastAPI(title="Sell-Off Trader Data", version="1.9")

@app.exception_handler(DataError)
async def data_error_handler(request, exc):
    return JSONResponse(status_code=502, content={"detail": exc.detail}, headers={"Cache-Control":"no-store"})
MAX_ROWS = 250
MIN_CAP = 2_000_000_000
HEADERS = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"}
SCREENER = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"


def fetch_json(url, params=None):
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=(3, 8))
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Expected object")
        return data
    except requests.Timeout as exc:
        raise HTTPException(504, detail={"code": "UPSTREAM_TIMEOUT", "message": "Yahoo no respondió a tiempo."}) from exc
    except (requests.RequestException, ValueError) as exc:
        raise HTTPException(502, detail={"code": "UPSTREAM_ERROR", "message": "Yahoo no entregó datos utilizables."}) from exc


@app.get("/top-losers")
def get_top_losers(response: Response):
    response.headers["Cache-Control"] = "no-store"
    data = fetch_json(SCREENER, {"formatted": "false", "lang": "en-US", "region": "US", "scrIds": "day_losers", "count": MAX_ROWS})
    return universe_payload(data, now_iso())


def one_quote(symbol):
    try:
        data = fetch_json(f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}", {"range": "5d", "interval": "1m", "includePrePost": "true"})
        return chart_quote(symbol, data)
    except (HTTPException, ValueError, TypeError, KeyError) as exc:
        return {"ticker": symbol, "error": "QUOTE_UNAVAILABLE", "message": "No se pudieron obtener barras utilizables para este símbolo.", "sessions": {"REGULAR": None, "PRE": None, "POST": None}}


@app.get("/quotes")
def get_quotes(response: Response, symbols: str = Query(..., max_length=300)):
    response.headers["Cache-Control"] = "no-store"
    names = list(dict.fromkeys(s.strip().upper() for s in symbols.split(",") if s.strip()))
    if not names or len(names) > 20 or any(not re.fullmatch(r"[A-Z0-9^][A-Z0-9.\-^=]{0,14}", s) for s in names):
        raise HTTPException(422, detail="Indica entre 1 y 20 símbolos válidos separados por comas.")
    with ThreadPoolExecutor(max_workers=5) as pool:
        rows = list(pool.map(one_quote, names))
    return {"generated_at": now_iso(), "source": "Yahoo Finance chart", "quotes": rows,
            "requested": len(names), "available": sum(not r.get("error") for r in rows)}


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.9", "max_rows": MAX_ROWS, "generated_at": now_iso()}
