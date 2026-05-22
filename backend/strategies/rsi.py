import pandas as pd
from strategies.base import calc_metrics

# RSI 전략: RSI가 oversold(30 이하) → 매수, overbought(70 이상) → 매도
def run(df: pd.DataFrame, period: int = 14, oversold: int = 30, overbought: int = 70) -> dict:
    close = df["close"]
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(period).mean()
    loss  = (-delta.clip(upper=0)).rolling(period).mean()
    rs    = gain / loss.replace(0, 1e-9)
    rsi   = 100 - (100 / (1 + rs))

    signals = pd.Series(0, index=close.index)
    signals[(rsi.shift(1) <= oversold)  & (rsi > oversold)]  = 1   # 과매도 탈출 → 매수
    signals[(rsi.shift(1) >= overbought) & (rsi < overbought)] = -1 # 과매수 탈출 → 매도

    return calc_metrics(close, signals)


METADATA = {
    "slug":        "rsi",
    "name":        "RSI",
    "name_ko":     "RSI (상대강도지수)",
    "category":    "technical",
    "description": "0~100 사이의 값으로 과매수·과매도를 판단합니다. RSI 30 이하에서 매수, 70 이상에서 매도하는 역추세 전략으로 단기 반등 포착에 효과적입니다.",
    "params":      [{"name": "period",    "default": 14, "desc": "RSI 계산 기간"},
                    {"name": "oversold",  "default": 30, "desc": "과매도 기준선"},
                    {"name": "overbought","default": 70, "desc": "과매수 기준선"}],
    "pros":        ["횡보장·반등 포착에 강함", "직관적 해석"],
    "cons":        ["강한 추세장에서 조기 청산", "단독 사용 시 신뢰도 낮음"],
    "best_market": "횡보·박스권 시장",
}
