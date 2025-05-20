
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from src.api.schemas import CollectionResponse, ErrorResponse
from src.database.db_config import SessionLocal
from src.database.utils import save_klines_dataframe
from src.scripts.binance_collector import get_klines, klines_to_dataframe


router = APIRouter(
    prefix="/collect",
    tags=["Data Collection"], 
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/klines", 
    response_model=CollectionResponse,
    summary="Coleta e armazena klines da Binance",
    responses={
        200: {"description": "Dados coletados e salvos com sucesso."},
        400: {"model": ErrorResponse, "description": "Erro nos parâmetros da requisição."},
        500: {"model": ErrorResponse, "description": "Erro interno do servidor durante a coleta ou salvamento."}
    }
)
async def collect_and_store_klines(
    symbol: str = Query(..., example="BTCUSDT", description="Símbolo do par (ex: BTCUSDT)"),
    interval: str = Query(..., example="1d", description="Intervalo da vela (ex: 1m, 1h, 1d)"),
    limit: Optional[int] = Query(1000, ge=1, le=1000, description="Número de klines a buscar (1-1000)"),
    db: Session = Depends(get_db)
):
    """
    Endpoint para buscar dados de klines da API da Binance e armazená-los no banco de dados.
    """
    print(f"Recebida requisição para coletar klines: symbol={symbol}, interval={interval}, limit={limit}")

    #Coletar dados da Binance
    raw_klines_data = get_klines(symbol=symbol, interval=interval, limit=limit)
    if not raw_klines_data:
        print(f"Nenhum dado retornado pela API da Binance para {symbol} ({interval}).")
        raise HTTPException(
            status_code=500, 
            detail=f"Nenhum dado retornado pela API da Binance para {symbol} ({interval})."
        )

    #Converter para DataFrame
    df_klines = klines_to_dataframe(raw_klines_data)
    if df_klines.empty:
        print("DataFrame vazio após a conversão. Nada a salvar.")
        raise HTTPException(
            status_code=500, 
            detail="Dados da Binance foram recebidos, mas resultaram em um DataFrame vazio após a conversão."
        )
    
    print(f"Dados convertidos para DataFrame: {len(df_klines)} velas.")

    #Salvar no Banco de Dados
    try:
        print(f"Tentando salvar {len(df_klines)} klines no banco de dados...")

        rows_saved = save_klines_dataframe(
            db=db, 
            df=df_klines, 
            symbol=symbol, 
            interval=interval
        )
        
        if rows_saved == -1:
            print("Erro reportado pela função save_klines_dataframe_to_db.")
            raise HTTPException(status_code=500, detail="Erro ao salvar dados no banco de dados.")
        
        print(f"Linhas afetadas no banco de dados: {rows_saved}")
        return CollectionResponse(
            status="sucesso",
            message=f"Dados para {symbol} ({interval}) coletados e processo de salvamento iniciado.",
            symbol_collected=symbol,
            interval_collected=interval,
            records_processed=len(df_klines),
            records_saved_to_db=rows_saved
        )
    except Exception as e:
        print(f"Exceção crítica ao salvar no banco de dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno do servidor ao salvar dados: {str(e)}")

