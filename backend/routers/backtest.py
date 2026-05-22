from fastapi import APIRouter, HTTPException, Query
from data.fetcher import fetch_ohlcv, resolve_ticker_name
from strategies import ma_crossover, macd, rsi, bollinger, momentum, mean_reversion
from strategies.ml import xgboost_strategy
import traceback

router = APIRouter()

# 전략 슬러그 → 실행 함수 매핑
STRATEGY_MAP = {
    "ma-crossover":  ma_crossover.run,
    "macd":          macd.run,
    "rsi":           rsi.run,
    "bollinger-bands": bollinger.run,
    "momentum":      momentum.run,
    "mean-reversion": mean_reversion.run,
    "xgboost":       xgboost_strategy.run,
}

@router.get("/backtest")
def run_backtest(
    ticker:   str = Query(..., description="종목 코드 (예: AAPL, 005930, BTC-USD)"),
    start:    str = Query(..., description="시작일 (YYYY-MM-DD)"),
    end:      str = Query(..., description="종료일 (YYYY-MM-DD)"),
    strategy: str = Query(..., description="전략 슬러그"),
):
    if strategy not in STRATEGY_MAP:
        raise HTTPException(400, f"지원하지 않는 전략: {strategy}")
    try:
        df     = fetch_ohlcv(ticker, start, end)
        result = STRATEGY_MAP[strategy](df)
        return {
            "ticker":      ticker,
            "ticker_name": resolve_ticker_name(ticker),
            "strategy":    strategy,
            "start":       start,
            "end":         end,
            **result,
        }
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception:
        raise HTTPException(500, traceback.format_exc())


@router.get("/backtest/compare")
def compare_backtest(
    ticker:     str  = Query(...),
    start:      str  = Query(...),
    end:        str  = Query(...),
    strategies: str  = Query(..., description="쉼표로 구분된 전략 슬러그"),
):
    """여러 전략을 동시에 백테스팅해 비교 반환"""
    strategy_list = [s.strip() for s in strategies.split(",")]
    invalid = [s for s in strategy_list if s not in STRATEGY_MAP]
    if invalid:
        raise HTTPException(400, f"지원하지 않는 전략: {invalid}")

    try:
        df = fetch_ohlcv(ticker, start, end)
    except ValueError as e:
        raise HTTPException(422, str(e))

    results = []
    for slug in strategy_list:
        try:
            r = STRATEGY_MAP[slug](df)
            results.append({"strategy": slug, **r})
        except Exception as e:
            results.append({"strategy": slug, "error": str(e)})

    return {
        "ticker":      ticker,
        "ticker_name": resolve_ticker_name(ticker),
        "start":       start,
        "end":         end,
        "results":     results,
    }
