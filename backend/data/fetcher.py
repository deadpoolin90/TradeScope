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
        raise ValueError(f"데이터를 가져올 수 없습니다: {ticker} — Yahoo Finance 일시적 오류이거나 잘못된 티커입니다.")

    if raw.empty:
        raise ValueError(f"데이터 없음: {ticker}")

    if isinstance(raw.columns, pd.MultiIndex):
        raw = raw.droplevel(1, axis=1)

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
