from fastapi import APIRouter, Query
import yfinance as yf

router = APIRouter()

# ?먯＜ 寃?됰릺??醫낅ぉ ?ъ쟾 ?뺤쓽
POPULAR = [
    {"ticker": "AAPL",    "name": "Apple Inc.",          "market": "us"},
    {"ticker": "MSFT",    "name": "Microsoft Corp.",     "market": "us"},
    {"ticker": "GOOGL",   "name": "Alphabet Inc.",       "market": "us"},
    {"ticker": "NVDA",    "name": "NVIDIA Corp.",        "market": "us"},
    {"ticker": "TSLA",    "name": "Tesla Inc.",          "market": "us"},
    {"ticker": "AMZN",    "name": "Amazon.com Inc.",     "market": "us"},
    {"ticker": "META",    "name": "Meta Platforms",      "market": "us"},
    {"ticker": "005930",  "name": "?쇱꽦?꾩옄",             "market": "kr"},
    {"ticker": "000660",  "name": "SK?섏씠?됱뒪",           "market": "kr"},
    {"ticker": "035420",  "name": "NAVER",               "market": "kr"},
    {"ticker": "051910",  "name": "LG?뷀븰",               "market": "kr"},
    {"ticker": "006400",  "name": "?쇱꽦SDI",              "market": "kr"},
    {"ticker": "BTC-USD", "name": "Bitcoin",             "market": "crypto"},
    {"ticker": "ETH-USD", "name": "Ethereum",            "market": "crypto"},
    {"ticker": "BNB-USD", "name": "BNB",                 "market": "crypto"},
    {"ticker": "SOL-USD", "name": "Solana",              "market": "crypto"},
]

@router.get("/search/ticker")
def search_ticker(q: str = Query(..., min_length=1)):
    q_lower = q.lower()
    # ?ъ쟾 ?뺤쓽 紐⑸줉?먯꽌 癒쇱? 寃??    local = [
        t for t in POPULAR
        if q_lower in t["ticker"].lower() or q_lower in t["name"].lower()
    ]
    if local:
        return {"results": local[:8]}

    # 濡쒖뺄 留ㅼ묶 ?놁쑝硫??곗빱 ?뺤떇?대㈃ 洹몃?濡?諛섑솚 (Yahoo Finance ?몄텧 湲덉? - rate limit)
    q_upper = q.upper().strip()
    if q_upper:
        return {"results": [{"ticker": q_upper, "name": q_upper, "market": "us"}]}

    return {"results": []}


@router.get("/search/popular")
def popular_tickers(market: str = Query("all")):
    if market == "all":
        return {"results": POPULAR}
    return {"results": [t for t in POPULAR if t["market"] == market]}
