from datetime import datetime, timezone
from math import isfinite
from zoneinfo import ZoneInfo
NY=ZoneInfo("America/New_York")
MAX_ROWS=250
MIN_CAP=2_000_000_000

class DataError(Exception):
    def __init__(self, detail):
        self.detail=detail
        super().__init__(detail["message"])

def now_iso():
    return datetime.now(timezone.utc).isoformat()


def timestamp(value):
    try:
        return datetime.fromtimestamp(float(value), timezone.utc).isoformat() if value else None
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def number(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) and isfinite(value) else None


def universe_payload(data, generated_at):
    finance = data.get("finance") or {}
    results = finance.get("result")
    if finance.get("error") or not isinstance(results, list) or not results:
        raise DataError({"code": "UNUSABLE_UNIVERSE", "message": "No se recibió un universo utilizable."})
    quotes = results[0].get("quotes")
    if not isinstance(quotes, list):
        raise DataError({"code": "UNUSABLE_UNIVERSE", "message": "Falta el array quotes."})
    rows = []
    invalid = 0
    for item in quotes[:MAX_ROWS]:
        if not isinstance(item, dict):
            invalid += 1
            continue
        cap = number(item.get("marketCap"))
        if cap is None or cap < MIN_CAP:
            continue
        price, change = number(item.get("regularMarketPrice")), number(item.get("regularMarketChangePercent"))
        ticker = item.get("symbol")
        if not isinstance(ticker, str) or not ticker.strip() or price is None or price <= 0 or change is None:
            invalid += 1
            continue
        rows.append({
            "ticker": ticker, "name": item.get("shortName") or item.get("longName") or ticker,
            "price": price, "change_percent": change, "market_cap_usd": cap,
            "quote_as_of": timestamp(item.get("regularMarketTime")),
            "price_session": "REGULAR", "market_state": item.get("marketState"),
            "exchange": item.get("fullExchangeName") or item.get("exchange"),
            "quote_type": item.get("quoteType"), "currency": item.get("currency"),
        })
    if not rows:
        raise DataError({"code": "EMPTY_ELIGIBLE_UNIVERSE", "message": "No hay filas elegibles utilizables; no se sustituye el universo."})
    times = [r["quote_as_of"] for r in rows if r["quote_as_of"]]
    return {
        "total_encontrados": len(rows), "top_losers": rows[:MAX_ROWS],
        "max_rows": MAX_ROWS, "upstream_rows": len(quotes), "invalid_rows": invalid,
        "generated_at": generated_at, "source": "Yahoo Finance / day_losers",
        "price_session": "REGULAR", "universe_basis": "REGULAR_DAY_LOSERS",
        "quote_as_of_oldest": min(times) if times else None,
        "quote_as_of_newest": max(times) if times else None,
        "quote_timestamp_coverage": len(times), "delay_minutes": None,
        "minimum_market_cap_usd": MIN_CAP,
        "note": "El universo y sus variaciones corresponden a sesión regular; no es un screener de pre-market.",
    }


def chart_quote(symbol, data):
    chart = data.get("chart") or {}
    result = chart.get("result")
    if chart.get("error") or not isinstance(result, list) or not result:
        raise ValueError("No chart data")
    item = result[0]
    meta = item.get("meta") or {}
    periods = meta.get("currentTradingPeriod") or {}
    regular = periods.get("regular") or {}
    start, end = regular.get("start"), regular.get("end")
    if not isinstance(start, (int, float)) or not isinstance(end, (int, float)):
        raise ValueError("No session boundaries")
    stamps = item.get("timestamp") or []
    indicators = item.get("indicators") or {}
    quotes = indicators.get("quote") or [{}]
    closes = quotes[0].get("close") or []
    volumes = quotes[0].get("volume") or []
    target_day = datetime.fromtimestamp(start, NY).date()
    today = datetime.now(NY).date()
    session_rows = {"REGULAR": [], "PRE": [], "POST": []}
    previous = []
    pre_start = (periods.get("pre") or {}).get("start", start)
    post_end = (periods.get("post") or {}).get("end", end)
    for index, ts in enumerate(stamps):
        price = number(closes[index]) if index < len(closes) else None
        if price is None or price <= 0 or not isinstance(ts, (int, float)):
            continue
        dt = datetime.fromtimestamp(ts, NY)
        bar = {"price": price, "quote_as_of": timestamp(ts), "volume": volumes[index] if index < len(volumes) else None}
        if dt.date() < target_day and (dt.hour > 9 or (dt.hour == 9 and dt.minute >= 30)) and dt.hour < 16:
            previous.append((ts, bar))
        elif start <= ts < end:
            session_rows["REGULAR"].append((ts, bar))
        elif target_day == today and pre_start <= ts < start:
            session_rows["PRE"].append((ts, bar))
        elif target_day == today and end <= ts < post_end:
            session_rows["POST"].append((ts, bar))
    prev_close = max(previous, key=lambda x: x[0])[1]["price"] if previous else None
    regular_bar = max(session_rows["REGULAR"], key=lambda x: x[0])[1] if session_rows["REGULAR"] else None
    if regular_bar is None and previous:
        regular_bar = max(previous, key=lambda x: x[0])[1]
    baseline = regular_bar["price"] if regular_bar else None
    sessions = {}
    for name, values in session_rows.items():
        bar = max(values, key=lambda x: x[0])[1] if values else (regular_bar if name == "REGULAR" else None)
        reference = prev_close if name == "PRE" or (name == "REGULAR" and values) else (baseline if name == "POST" else None)
        sessions[name] = None if bar is None else {**bar, "change_percent": ((bar["price"] / reference - 1) * 100) if reference else None,
            "reference_price": reference, "kind": "ONE_MINUTE_BAR", "session": name}
    return {"ticker": symbol, "name": meta.get("shortName") or meta.get("longName") or symbol,
            "currency": meta.get("currency"), "source": "Yahoo Finance chart / 1m",
            "delay_minutes": None, "sessions": sessions, "regular_session_start": timestamp(start), "regular_session_end": timestamp(end),
            "note": "Últimas barras disponibles por sesión; no son bid/ask ni cotizaciones con latencia garantizada."}


