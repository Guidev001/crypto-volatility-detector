from pydantic import BaseModel, Field
from typing import Optional

class CollectKlinesRequest(BaseModel):
    """
    Modelo de requisição para o endpoint de coleta de klines.
    """
    symbol: str = Field(..., example="BTCUSDT", description="O símbolo do par de negociação (ex: BTCUSDT)")
    interval: str = Field(..., example="1d", description="O intervalo da vela (ex: 1m, 1h, 1d)")
    limit: Optional[int] = Field(1000, ge=1, le=1000, description="Número de klines a buscar (entre 1 e 1000)")

class CollectionResponse(BaseModel):
    """
    Modelo de resposta para o endpoint de coleta.
    """
    status: str = Field(..., example="sucesso", description="Status da operação de coleta")
    message: str = Field(..., example="Dados coletados e salvos com sucesso.", description="Mensagem detalhando o resultado")
    symbol_collected: Optional[str] = Field(None, example="BTCUSDT", description="Símbolo para o qual os dados foram coletados")
    interval_collected: Optional[str] = Field(None, example="1d", description="Intervalo para o qual os dados foram coletados")
    records_processed: Optional[int] = Field(None, example=1000, description="Número de registros de klines processados")
    records_saved_to_db: Optional[int] = Field(None, example=1000, description="Número de registros salvos/afetados no banco de dados")

class ErrorResponse(BaseModel):
    """
    Modelo de resposta para erros.
    """
    detail: str = Field(..., example="Ocorreu um erro durante a operação.")