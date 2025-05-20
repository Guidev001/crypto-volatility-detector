
import uvicorn
from fastapi import FastAPI
from src.api.routers import klines

app = FastAPI(
    title="Crypto Volatility Detector API",
    description="API para coletar dados de criptomoedas e, futuramente, fornecer previsões de volatilidade.",
    version="0.1.0"
)

app.include_router(klines.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API Crypto Volatility Detector!"}

if __name__ == "__main__":
    print("Iniciando servidor Uvicorn")
    uvicorn.run(app, host="0.0.0.0", port=8000)
