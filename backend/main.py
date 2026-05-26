from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import backtest, rankings, models, search

app = FastAPI(title="TradeScope API", version="1.0.0")

# Next.js 개발 서버 및 배포 도메인 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(backtest.router, prefix="/api")
app.include_router(rankings.router, prefix="/api")
app.include_router(models.router,   prefix="/api")
app.include_router(search.router,   prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "service": "TradeScope API"}
