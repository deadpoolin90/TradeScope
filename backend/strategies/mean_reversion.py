import pandas as pd
from strategies.base import calc_metrics

# 평균 회귀 전략: 가격이 이동평균 대비 과도하게 하락하면 매수, 과도하게 상승하면 매도
def run(df: pd.DataFrame, period: int = 20, threshold: float = 0.03) -> dict:
    close = df["close"]
    ma    = close.rolling(period).mean()
    dev   = (close - ma) / ma  # 이동평균 대비 편차 비율

    signals = pd.Series(0, index=close.index)
    signals[(dev.shift(1) > -threshold) & (dev <= -threshold)] = 1   # 임계치 이하 하락 → 매수
    signals[(dev.shift(1) < threshold)  & (dev >= threshold)]  = -1  # 임계치 이상 상승 → 매도

    return calc_metrics(close, signals)


METADATA = {
    "slug":        "mean-reversion",
    "name":        "Mean Reversion",
    "name_ko":     "평균 회귀",
    "category":    "quant",
    "description": "가격이 장기 평균에서 크게 벗어나면 다시 평균으로 돌아온다는 원리를 이용합니다. 이동평균 대비 3% 이상 하락 시 매수, 3% 이상 상승 시 매도합니다.",
    "params":      [{"name": "period",    "default": 20,  "desc": "이동평균 기간(일)"},
                    {"name": "threshold", "default": 0.03, "desc": "진입 임계값 (비율)"}],
    "pros":        ["횡보장에서 안정적 수익", "명확한 진입·청산 기준"],
    "cons":        ["강한 추세 지속 시 큰 손실", "임계값 설정이 성과에 민감"],
    "best_market": "횡보·박스권 시장",
}
