
from sqlalchemy import Column, Integer, String, DateTime, Numeric, BigInteger, UniqueConstraint
from sqlalchemy.sql import func

from .db_config import Base 

class KlineOHLCV(Base):
    """
    Modelo SQLAlchemy para armazenar dados de Klines (OHLCV) da Binance.
    """
    __tablename__ = "klines_ohlcv"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    symbol = Column(String(20), nullable=False, index=True)
    interval_time = Column(String(5), nullable=False, index=True) # Ex: '1m', '1h', '1d'
    
    open_time = Column(DateTime(timezone=True), nullable=False, index=True)
    open_price = Column(Numeric(20, 8), nullable=False)
    high_price = Column(Numeric(20, 8), nullable=False)
    low_price = Column(Numeric(20, 8), nullable=False)
    close_price = Column(Numeric(20, 8), nullable=False)
    volume = Column(Numeric(30, 8), nullable=False)
    
    close_time = Column(DateTime(timezone=True), nullable=False)
    quote_asset_volume = Column(Numeric(30, 8))
    number_of_trades = Column(BigInteger)
    taker_buy_base_asset_volume = Column(Numeric(30, 8))
    taker_buy_quote_asset_volume = Column(Numeric(30, 8))
    
    __table_args__ = (UniqueConstraint('symbol', 'interval_time', 'open_time', name='uq_symbol_interval_opentime'),)

    def __repr__(self):
        return (f"<KlineOHLCV(symbol='{self.symbol}', interval='{self.interval_time}', "
                f"open_time='{self.open_time}', close_price='{self.close_price}')>")
