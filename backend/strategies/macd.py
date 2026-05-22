import pandas as pd
from strategies.base import calc_metrics

# MACD 전략: MACD선이 시그널선을 상향돌파 → 매수, 하향돌파 → 매도
def run(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    close = df["close"]
    ema_fast   = close.ewm(span=fast,   adjust=False).mean()
    ema_slow   = close.ewm(span=slow,   adjust=False).mean()
    macd_line  = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()

    prev_above = (macd_line.shift(1) > signal_line.shift(1))
    curr_above = (macd_line > signal_line)

    signals = pd.Series(0, index=close.index)
    signals[~prev_above & curr_above] = 1
    signals[prev_above & ~curr_above] = -1

    return calc_metrics(close, signals)


METADATA = {
    "slug":        "macd",
    "name":        "MACD",
    "name_ko":     "MACD",
    "category":    "technical",
    "description": "단기(12일)·장기(26일) EMA 차이인 MACD선과 9일 시그널선의 교차를 활용한 모멘텀 전략입니다. 히스토그램으로 모멘텀 강도도 파악할 수 있습니다.",
    "params":      [{"name": "fast",   "default": 12, "desc": "단기 EMA 기간"},
                    {"name": "slow",   "default": 26, "desc": "장기 EMA 기간"},
                    {"name": "signal", "default": 9,  "desc": "시그널선 기간"}],
    "pros":        ["추세 + 모멘텀 동시 포착", "MA보다 반응이 빠름"],
    "cons":        ["파라미터 민감도 높음", "횡보장 노이즈"],
    "best_market": "중·장기 추세장",
}
