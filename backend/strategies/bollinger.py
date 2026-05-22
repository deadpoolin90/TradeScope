import pandas as pd
from strategies.base import calc_metrics

# 볼린저 밴드 전략: 가격이 하단 밴드 터치 → 매수, 상단 밴드 터치 → 매도
def run(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> dict:
    close  = df["close"]
    ma     = close.rolling(period).mean()
    std    = close.rolling(period).std()
    upper  = ma + std_dev * std
    lower  = ma - std_dev * std

    signals = pd.Series(0, index=close.index)
    signals[(close.shift(1) > lower.shift(1)) & (close <= lower)] = 1   # 하단 밴드 터치 → 매수
    signals[(close.shift(1) < upper.shift(1)) & (close >= upper)] = -1  # 상단 밴드 터치 → 매도

    return calc_metrics(close, signals)


METADATA = {
    "slug":        "bollinger-bands",
    "name":        "Bollinger Bands",
    "name_ko":     "볼린저 밴드",
    "category":    "technical",
    "description": "20일 이동평균을 중심으로 ±2 표준편차 밴드를 그립니다. 가격이 하단 밴드에 닿으면 매수, 상단 밴드에 닿으면 매도하는 평균 회귀 전략입니다. 변동성이 클수록 밴드 폭이 넓어집니다.",
    "params":      [{"name": "period",  "default": 20,  "desc": "이동평균 기간"},
                    {"name": "std_dev", "default": 2.0, "desc": "표준편차 배수"}],
    "pros":        ["변동성 자동 반영", "시각적으로 직관적"],
    "cons":        ["강한 추세 돌파 시 손실 위험", "변동성 낮은 시장에서 신호 부족"],
    "best_market": "횡보·변동성 높은 시장",
}
