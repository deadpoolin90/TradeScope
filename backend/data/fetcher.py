import time
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from data.cache import get_cached, set_cached

POPULAR_NAMES = {
    "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.",
    "NVDA": "NVIDIA Corp.", "TSLA": "Tesla Inc.", "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms", "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum",
    "BNB-USD": "BNB", "SOL-USD": "Solana",
    "005930": "?쇱꽦?꾩옄", "000660": "SK?섏씠?됱뒪", "035420": "NAVER",
    "051910": "LG?뷀븰", "006400": "?쇱꽦SDI",
}

# ?쒓뎅 醫낅ぉ? pykrx ?ъ슜 (KRX 嫄곕옒??
try:
    from pykrx import stock as krx
    KRX_AVAILABLE = True
except ImportError:
    KRX_AVAILABLE = False


def fetch_ohlcv(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    ?곗빱쨌湲곌컙?쇰줈 OHLCV ?곗씠?곕? 諛섑솚.
    - ?쒓뎅 醫낅ぉ(6?먮━ ?レ옄): pykrx
    - 洹???誘멸뎅, ?뷀샇?뷀룓): yfinance
    罹먯떆 ?덊듃 ???ㅽ듃?뚰겕 ?붿껌 ?놁씠 諛섑솚.
    """
    cache_key = f"{ticker}_{start}_{end}"
    cached = get_cached(cache_key)
    if cached is not None:
        return cached

    if _is_krx(ticker):
        df = _fetch_krx(ticker, start, end)
    else:
        df = _fetch_yfinance(ticker, start, end)

    set_cached(cache_key, df)
    return df


def _is_krx(ticker: str) -> bool:
    # ?쒓뎅 醫낅ぉ肄붾뱶: 6?먮━ ?レ옄 (?? 005930)
    return ticker.isdigit() and len(ticker) == 6


def _fetch_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame:
    for attempt in range(3):
        try:
            raw = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
            if not raw.empty:
                break
        except Exception:
            pass
        if attempt < 2:
            time.sleep(2 ** attempt)
    else:
        raise ValueError(f"?곗씠?곕? 媛?몄삱 ???놁뒿?덈떎: {ticker} ??Yahoo Finance ?쇱떆???ㅻ쪟?닿굅???섎せ???곗빱?낅땲??")

    if raw.empty:
        raise ValueError(f"?곗씠???놁쓬: {ticker}")

    if isinstance(raw.columns, pd.MultiIndex):
        raw = raw.droplevel(1, axis=1)

    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index = pd.to_datetime(df.index)
    return df.dropna()


def _fetch_krx(ticker: str, start: str, end: str) -> pd.DataFrame:
    if not KRX_AVAILABLE:
        raise ImportError("pykrx媛 ?ㅼ튂?섏? ?딆븯?듬땲??)
    # pykrx???좎쭨 ?뺤떇 YYYYMMDD
    s = start.replace("-", "")
    e = end.replace("-", "")
    raw = krx.get_market_ohlcv_by_date(s, e, ticker)
    if raw.empty:
        raise ValueError(f"KRX ?곗씠???놁쓬: {ticker}")
    df = raw.rename(columns={"?쒓?": "open", "怨좉?": "high", "?媛": "low",
                              "醫낃?": "close", "嫄곕옒??: "volume"})
    df.index = pd.to_datetime(df.index)
    return df[["open", "high", "low", "close", "volume"]].dropna()


def resolve_ticker_name(ticker: str) -> str:
    """?곗빱???뚯궗紐?諛섑솚 (?쒖떆?? ??濡쒖뺄 罹먯떆 ?곗꽑, Yahoo Finance 誘명샇異?""
    if ticker in POPULAR_NAMES:
        return POPULAR_NAMES[ticker]
    if _is_krx(ticker):
        try:
            return krx.get_market_ticker_name(ticker) if KRX_AVAILABLE else ticker
        except Exception:
            return ticker
    return ticker
