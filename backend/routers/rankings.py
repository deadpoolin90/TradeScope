from fastapi import APIRouter, Query
from datetime import date, timedelta
from data.fetcher import fetch_ohlcv
from strategies import ma_crossover, macd, rsi, bollinger, momentum, mean_reversion

router = APIRouter()

# 랭킹 계산에 사용할 대표 종목 (시장별)
DEFAULT_TICKERS = {
    "us":     ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"],
    "kr":     ["005930", "000660", "035420", "051910", "006400"],
    "crypto": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD"],
}

STRATEGIES = {
    "ma-crossover":   ma_crossover.run,
    "macd":           macd.run,
    "rsi":            rsi.run,
    "bollinger-bands": bollinger.run,
    "momentum":       momentum.run,
    "mean-reversion": mean_reversion.run,
}

PERIOD_MAP = {
    "1M": 30, "3M": 90, "6M": 180,
    "1Y": 365, "3Y": 365*3, "5Y": 365*5,
}

@router.get("/rankings")
def get_rankings(
    period: str  = Query("1Y", description="1M / 3M / 6M / 1Y / 3Y / 5Y"),
    market: str  = Query("us", description="us / kr / crypto / all"),
    ticker: str  = Query(None, description="특정 종목 지정 시"),
):
    days = PERIOD_MAP.get(period, 365)
    end_date   = date.today().isoformat()
    start_date = (date.today() - timedelta(days=days)).isoformat()

    tickers = (
        [ticker] if ticker
        else DEFAULT_TICKERS.get(market, sum(DEFAULT_TICKERS.values(), []))
    )

    ranking_rows = []
    for t in tickers:
        try:
            df = fetch_ohlcv(t, start_date, end_date)
        except Exception:
            continue
        for slug, fn in STRATEGIES.items():
            try:
                r = fn(df)
                ranking_rows.append({
                    "ticker":       t,
                    "strategy":     slug,
                    "total_return": r["total_return"],
                    "sharpe":       r["sharpe"],
                    "max_drawdown": r["max_drawdown"],
                    "win_rate":     r["win_rate"],
                })
            except Exception:
                continue

    # 수익률 기준 내림차순
    ranking_rows.sort(key=lambda x: x["total_return"], reverse=True)
    return {
        "period": period,
        "market": market,
        "start":  start_date,
        "end":    end_date,
        "rankings": ranking_rows,
    }
