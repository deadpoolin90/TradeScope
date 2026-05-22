from fastapi import APIRouter, Query
import yfinance as yf

router = APIRouter()

# 자주 검색되는 종목 사전 정의
POPULAR = [
    {"ticker": "AAPL",    "name": "Apple Inc.",          "market": "us"},
    {"ticker": "MSFT",    "name": "Microsoft Corp.",     "market": "us"},
    {"ticker": "GOOGL",   "name": "Alphabet Inc.",       "market": "us"},
    {"ticker": "NVDA",    "name": "NVIDIA Corp.",        "market": "us"},
    {"ticker": "TSLA",    "name": "Tesla Inc.",          "market": "us"},
    {"ticker": "AMZN",    "name": "Amazon.com Inc.",     "market": "us"},
    {"ticker": "META",    "name": "Meta Platforms",      "market": "us"},
    {"ticker": "005930",  "name": "삼성전자",             "market": "kr"},
    {"ticker": "000660",  "name": "SK하이닉스",           "market": "kr"},
    {"ticker": "035420",  "name": "NAVER",               "market": "kr"},
    {"ticker": "051910",  "name": "LG화학",               "market": "kr"},
    {"ticker": "006400",  "name": "삼성SDI",              "market": "kr"},
    {"ticker": "BTC-USD", "name": "Bitcoin",             "market": "crypto"},
    {"ticker": "ETH-USD", "name": "Ethereum",            "market": "crypto"},
    {"ticker": "BNB-USD", "name": "BNB",                 "market": "crypto"},
    {"ticker": "SOL-USD", "name": "Solana",              "market": "crypto"},
]

@router.get("/search/ticker")
def search_ticker(q: str = Query(..., min_length=1)):
    q_lower = q.lower()
    # 사전 정의 목록에서 먼저 검색
    local = [
        t for t in POPULAR
        if q_lower in t["ticker"].lower() or q_lower in t["name"].lower()
    ]
    if local:
        return {"results": local[:8]}

    # yfinance로 검색 (미국/글로벌)
    try:
        info = yf.Ticker(q.upper()).info
        if info.get("regularMarketPrice"):
            return {"results": [{
                "ticker": q.upper(),
                "name":   info.get("shortName", q.upper()),
                "market": "us",
            }]}
    except Exception:
        pass

    return {"results": []}


@router.get("/search/popular")
def popular_tickers(market: str = Query("all")):
    if market == "all":
        return {"results": POPULAR}
    return {"results": [t for t in POPULAR if t["market"] == market]}
