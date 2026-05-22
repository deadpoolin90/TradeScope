from fastapi import APIRouter
from strategies import (ma_crossover, macd, rsi, bollinger,
                        momentum, mean_reversion)
from strategies.ml import xgboost_strategy

router = APIRouter()

ALL_METADATA = [
    ma_crossover.METADATA,
    macd.METADATA,
    rsi.METADATA,
    bollinger.METADATA,
    momentum.METADATA,
    mean_reversion.METADATA,
    xgboost_strategy.METADATA,
    # 정적 메타데이터 (백테스팅 미구현 모델)
    {
        "slug": "lstm", "name": "LSTM", "name_ko": "LSTM (장단기 기억망)",
        "category": "ml",
        "description": "시계열 패턴을 장기 기억하는 딥러닝 모델입니다. 가격·거래량·기술 지표를 시퀀스로 입력받아 미래 방향을 예측합니다. 학습 시간이 길지만 복잡한 비선형 패턴 포착에 강합니다.",
        "pros": ["장기 의존성 학습", "다변량 입력 가능"],
        "cons": ["학습 시간 길고 튜닝 어려움", "설명 불가 (블랙박스)"],
        "best_market": "변동성 패턴이 반복되는 암호화폐, 선물",
    },
    {
        "slug": "random-forest", "name": "Random Forest", "name_ko": "랜덤 포레스트",
        "category": "ml",
        "description": "수백 개의 결정 트리를 앙상블하여 예측 안정성을 높입니다. XGBoost와 유사하나 병렬 처리로 빠르고 과적합에 더 강합니다.",
        "pros": ["과적합 강함", "피처 중요도 제공"],
        "cons": ["XGBoost 대비 정확도 낮음", "메모리 사용量 많음"],
        "best_market": "데이터 노이즈가 많은 시장",
    },
    {
        "slug": "dual-momentum", "name": "Dual Momentum", "name_ko": "듀얼 모멘텀",
        "category": "quant",
        "description": "Gary Antonacci가 개발. 절대 모멘텀(벤치마크 대비)과 상대 모멘텀(자산 간)을 결합해 하락장 방어와 상승 포착을 동시에 추구합니다.",
        "pros": ["하락장 방어 우수", "장기 검증된 전략"],
        "cons": ["월 1회 리밸런싱 필요", "단기 수익 낮음"],
        "best_market": "장기(1년↑) 글로벌 자산배분",
    },
    {
        "slug": "ichimoku", "name": "Ichimoku Cloud", "name_ko": "일목균형표",
        "category": "technical",
        "description": "전환선·기준선·선행스팬A/B·후행스팬 다섯 개 선으로 추세·지지·저항을 한눈에 파악합니다. 구름(Cloud) 위에서 매수, 아래에서 매도하는 것이 기본 원칙입니다.",
        "pros": ["추세·지지·저항 통합 분석", "미래 구름으로 선행 예측"],
        "cons": ["파라미터 5개로 복잡", "초보자 이해 어려움"],
        "best_market": "일·주 단위 추세 추종",
    },
]

@router.get("/models")
def list_models():
    return {"models": ALL_METADATA}

@router.get("/models/{slug}")
def get_model(slug: str):
    for m in ALL_METADATA:
        if m["slug"] == slug:
            return m
    return {"error": "모델을 찾을 수 없습니다"}
