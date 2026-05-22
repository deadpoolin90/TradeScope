import pandas as pd
from strategies.base import calc_metrics

# 단기/장기 이동평균 교차 전략
# 단기MA가 장기MA를 상향돌파 → 매수, 하향돌파 → 매도
def run(df: pd.DataFrame, short: int = 20, long: int = 60) -> dict:
    close = df["close"]
    ma_short = close.rolling(short).mean()
    ma_long  = close.rolling(long).mean()

    # 교차 시그널 생성
    prev_above = (ma_short.shift(1) > ma_long.shift(1))
    curr_above = (ma_short > ma_long)

    signals = pd.Series(0, index=close.index)
    signals[~prev_above & curr_above] = 1   # 골든크로스 → 매수
    signals[prev_above & ~curr_above] = -1  # 데드크로스 → 매도

    return calc_metrics(close, signals)


METADATA = {
    "slug":        "ma-crossover",
    "name":        "MA Crossover",
    "name_ko":     "이동평균 교차",
    "category":    "technical",
    "description": "단기 이동평균이 장기 이동평균을 상향 돌파할 때 매수(골든크로스), 하향 돌파할 때 매도(데드크로스)하는 가장 고전적인 추세 추종 전략입니다.",
    "params":      [{"name": "short", "default": 20, "desc": "단기 이동평균 기간(일)"},
                    {"name": "long",  "default": 60, "desc": "장기 이동평균 기간(일)"}],
    "pros":        ["이해하기 쉽고 구현이 단순", "강한 추세장에서 높은 성과"],
    "cons":        ["횡보장에서 잦은 손절(채찍질)", "후행성으로 진입·청산이 늦음"],
    "best_market": "추세가 뚜렷한 상승/하락장",
}
