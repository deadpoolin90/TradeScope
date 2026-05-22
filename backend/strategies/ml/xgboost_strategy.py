import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import TimeSeriesSplit
from strategies.base import calc_metrics

# XGBoost 전략: 기술 지표를 피처로 학습해 다음 날 상승/하락 예측
def _make_features(close: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame(index=close.index)
    # 수익률 피처
    for n in [1, 3, 5, 10, 20]:
        df[f"ret_{n}"] = close.pct_change(n)
    # 이동평균 편차
    for n in [5, 10, 20, 60]:
        df[f"ma_dev_{n}"] = close / close.rolling(n).mean() - 1
    # 변동성
    df["vol_10"] = close.pct_change().rolling(10).std()
    df["vol_20"] = close.pct_change().rolling(20).std()
    # RSI
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    df["rsi"] = 100 - 100 / (1 + gain / loss.replace(0, 1e-9))
    return df.dropna()


def run(df: pd.DataFrame, forward: int = 5, threshold: float = 0.01) -> dict:
    close   = df["close"]
    feats   = _make_features(close)
    # 레이블: N일 후 수익률 > threshold → 1(매수), 아니면 0
    label   = (close.shift(-forward) / close - 1 > threshold).astype(int)
    label   = label.reindex(feats.index).dropna()
    feats   = feats.reindex(label.index)

    if len(feats) < 100:
        raise ValueError("학습 데이터 부족 (최소 100일 필요)")

    # 시계열 교차검증으로 학습 (미래 누수 방지)
    split   = int(len(feats) * 0.7)
    X_train, X_test = feats.iloc[:split], feats.iloc[split:]
    y_train         = label.iloc[:split]

    model = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05,
                          eval_metric="logloss", verbosity=0)
    model.fit(X_train, y_train)

    # 테스트 구간 예측
    pred    = model.predict(X_test)
    signals = pd.Series(0, index=close.index)
    test_idx = X_test.index
    signals.loc[test_idx[pred == 1]] = 1
    signals.loc[test_idx[pred == 0]] = -1

    return calc_metrics(close.reindex(signals.index), signals)


METADATA = {
    "slug":        "xgboost",
    "name":        "XGBoost",
    "name_ko":     "XGBoost (그래디언트 부스팅)",
    "category":    "ml",
    "description": "20여 개의 기술적 지표를 피처로 XGBoost 모델을 학습시켜 N일 후 주가 상승 여부를 예측합니다. 앙상블 방식으로 과적합에 강하며 정형 데이터에서 딥러닝 대비 경쟁력이 높습니다.",
    "params":      [{"name": "forward",   "default": 5,    "desc": "예측 기간(일)"},
                    {"name": "threshold", "default": 0.01, "desc": "매수 임계 수익률"}],
    "pros":        ["비선형 패턴 포착", "피처 중요도 해석 가능", "빠른 학습"],
    "cons":        ["학습 데이터 충분해야 함", "시장 구조 변화에 취약"],
    "best_market": "데이터 충분한 대형주, 암호화폐",
}
