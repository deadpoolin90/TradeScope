from dataclasses import dataclass
import pandas as pd
import numpy as np

@dataclass
class BacktestResult:
    strategy:       str
    ticker:         str
    start:          str
    end:            str
    total_return:   float   # 총 수익률 (%)
    cagr:           float   # 연환산 수익률 (%)
    sharpe:         float   # 샤프 비율
    max_drawdown:   float   # 최대 낙폭 (%)
    win_rate:       float   # 승률 (%)
    trade_count:    int     # 거래 횟수
    equity_curve:   list    # 누적 수익률 시계열 [{date, value}]
    signals:        list    # 매수/매도 시점 [{date, type, price}]


def calc_metrics(prices: pd.Series, signals: pd.Series) -> dict:
    """
    prices: 종가 시계열
    signals: 1(매수), -1(매도/공매도), 0(중립) 시계열
    공통 성과 지표 계산
    """
    # 포지션: 매수 후 다음 매도까지 1 유지
    position = signals.replace(0, np.nan).ffill().fillna(0)
    position = position.clip(0, 1)  # 롱 온리

    # 일일 수익률
    daily_ret = prices.pct_change().fillna(0)
    strat_ret = daily_ret * position.shift(1).fillna(0)

    # 누적 수익률
    cum_ret = (1 + strat_ret).cumprod()
    total_return = (cum_ret.iloc[-1] - 1) * 100

    # CAGR
    n_years = len(prices) / 252
    cagr = ((cum_ret.iloc[-1]) ** (1 / max(n_years, 0.01)) - 1) * 100 if n_years > 0 else 0

    # 샤프 비율 (무위험 이자율 0 가정)
    sharpe = (strat_ret.mean() / strat_ret.std() * np.sqrt(252)) if strat_ret.std() > 0 else 0

    # 최대 낙폭
    rolling_max = cum_ret.cummax()
    drawdown = (cum_ret - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    # 개별 거래 수익률로 승률 계산
    buy_idx  = signals[signals == 1].index
    sell_idx = signals[signals == -1].index
    wins = 0
    trades = 0
    for b in buy_idx:
        future_sells = sell_idx[sell_idx > b]
        if len(future_sells) == 0:
            continue
        s = future_sells[0]
        ret = prices[s] / prices[b] - 1
        wins += 1 if ret > 0 else 0
        trades += 1

    win_rate = (wins / trades * 100) if trades > 0 else 0

    # 누적 수익률 곡선 (JSON 직렬화용)
    equity_curve = [
        {"date": str(d.date()), "value": round(float(v), 4)}
        for d, v in cum_ret.items()
    ]

    # 시그널 목록
    signal_list = []
    for d, v in signals.items():
        if v == 1:
            signal_list.append({"date": str(d.date()), "type": "buy",  "price": float(prices[d])})
        elif v == -1:
            signal_list.append({"date": str(d.date()), "type": "sell", "price": float(prices[d])})

    return {
        "total_return":  round(total_return, 2),
        "cagr":          round(cagr, 2),
        "sharpe":        round(float(sharpe), 3),
        "max_drawdown":  round(max_drawdown, 2),
        "win_rate":      round(win_rate, 2),
        "trade_count":   trades,
        "equity_curve":  equity_curve,
        "signals":       signal_list,
    }
