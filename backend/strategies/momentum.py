import pandas as pd
from strategies.base import calc_metrics

# 모멘텀 전략: 최근 N일 수익률이 양수이면 보유, 음수이면 청산
def run(df: pd.DataFrame, lookback: int = 60, hold: int = 20) -> dict:
    close = df["close"]
    # N일 전 대비 수익률
    momentum = close.pct_change(lookback)

    signals = pd.Series(0, index=close.index)
    # 모멘텀 양전환 → 매수
    signals[(momentum.shift(1) <= 0) & (momentum > 0)] = 1
    # 모멘텀 음전환 → 매도
    signals[(momentum.shift(1) > 0) & (momentum <= 0)] = -1

    return calc_metrics(close, signals)


METADATA = {
    "slug":        "momentum",
    "name":        "Momentum",
    "name_ko":     "모멘텀",
    "category":    "quant",
    "description": "최근 N일간 수익률이 양(+)이면 상승 모멘텀이 지속될 것으로 보고 매수합니다. '오르는 주식은 계속 오른다'는 시장 관성을 이용하는 전략으로 학술적으로도 검증된 팩터입니다.",
    "params":      [{"name": "lookback", "default": 60, "desc": "모멘텀 계산 기간(일)"},
                    {"name": "hold",     "default": 20, "desc": "최소 보유 기간(일)"}],
    "pros":        ["장기 수익률 검증된 팩터", "단순한 로직"],
    "cons":        ["급반전 시 큰 손실", "거래비용에 민감"],
    "best_market": "장기 상승 추세장",
}
