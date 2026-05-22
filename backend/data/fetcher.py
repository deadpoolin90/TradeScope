import time
import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from data.cache import get_cached, set_cached

def _make_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })
    return s

POPULAR_NAMES = {
    "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc.",
    "NVDA": "NVIDIA Corp.", "TSLA": "Tesla Inc.", "AMZN": "Amazon.com Inc.",
    "META": "Meta Platforms", "BTC-USD": "Bitcoin", "ETH-USD": "Ethereum",
    "BNB-USD": "BNB", "SOL-USD": "Solana",
    "005930": "삼성전자", "000660": "SK하이닉스", "035420": "NAVER",
    "051910": "LG화학", "006400": "삼성SDI",
}

# 한국 종목은 pykrx 사용 (KRX 거래소)
try:
    from pykrx import stock as krx
    KRX_AVAILABLE = True
except ImportError:
    KRX_AVAILABLE = False


def fetch_ohlcv(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    티커·기간으로 OHLCV 데이터를 반환.
    - 한국 종목(6자리 숫자): pykrx
    - 그 외(미국, 암호화폐): yfinance
    캐시 히트 시 네트워크 요청 없이 반환.
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
    # 한국 종목코드: 6자리 숫자 (예: 005930)
    return ticker.isdigit() and len(ticker) == 6


def _fetch_stooq(ticker: str, start: str, end: str) -> pd.DataFrame:
    """stooq.com fallback — Yahoo Finance 차단 시 사용"""
    s = start.replace("-", "")
    e = end.replace("-", "")
    stooq_ticker = ticker.replace("-", ".").upper()
    # 암호화폐는 stooq 미지원
    if "." in ticker and ticker.endswith("USD"):
        return pd.DataFrame()
    url = f"https://stooq.com/q/d/l/?s={stooq_ticker}&d1={s}&d2={e}&i=d"
    try:
        session = _make_session()
        resp = session.get(url, timeout=10)
        from io import StringIO
        df = pd.read_csv(StringIO(resp.text), index_col=0, parse_dates=True)
        if df.empty or "No data" in resp.text:
            return pd.DataFrame()
        df.index = pd.to_datetime(df.index)
        return df.sort_index()
    except Exception:
        return pd.DataFrame()


def _fetch_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame:
    delays = [0, 3, 8]
    raw = None
    last_exc = None
    for delay in delays:
        if delay:
            time.sleep(delay)
        try:
            session = _make_session()
            t = yf.Ticker(ticker, session=session)
            raw = t.history(start=start, end=end, auto_adjust=True)
            if not raw.empty:
                break
        except Exception as e:
            last_exc = e
            raw = None

    # yfinance 실패 시 stooq fallback
    if raw is None or raw.empty:
        raw = _fetch_stooq(ticker, start, end)
        if raw is not None and not raw.empty:
            raw = raw.rename(columns={"Open": "Open", "High": "High", "Low": "Low",
                                       "Close": "Close", "Volume": "Volume"})

    if raw is None or raw.empty:
        raise ValueError(f"데이터를 가져올 수 없습니다: {ticker} — 잘못된 티커이거나 데이터 소스 오류입니다.")

    if isinstance(raw.columns, pd.MultiIndex):
        raw = raw.droplevel(1, axis=1)

    col_map = {c: c.capitalize() for c in raw.columns}
    raw = raw.rename(columns=col_map)

    df = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index = pd.to_datetime(df.index)
    return df.dropna()


def _fetch_krx(ticker: str, start: str, end: str) -> pd.DataFrame:
    if not KRX_AVAILABLE:
        raise ImportError("pykrx가 설치되지 않았습니다")
    # pykrx는 날짜 형식 YYYYMMDD
    s = start.replace("-", "")
    e = end.replace("-", "")
    raw = krx.get_market_ohlcv_by_date(s, e, ticker)
    if raw.empty:
        raise ValueError(f"KRX 데이터 없음: {ticker}")
    df = raw.rename(columns={"시가": "open", "고가": "high", "저가": "low",
                              "종가": "close", "거래량": "volume"})
    df.index = pd.to_datetime(df.index)
    return df[["open", "high", "low", "close", "volume"]].dropna()


def resolve_ticker_name(ticker: str) -> str:
    """티커의 회사명 반환 (표시용) — 로컬 캐시 우선, Yahoo Finance 미호출"""
    if ticker in POPULAR_NAMES:
        return POPULAR_NAMES[ticker]
    if _is_krx(ticker):
        try:
            return krx.get_market_ticker_name(ticker) if KRX_AVAILABLE else ticker
        except Exception:
            return ticker
    return ticker
