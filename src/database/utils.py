import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
from .db_config import engine, Base, SessionLocal
from .models import KlineOHLCV

def save_klines_dataframe(db: Session, df: pd.DataFrame, symbol: str, interval: str):
    """
    Salva um DataFrame de klines no banco de dados.
    Usa 'ON CONFLICT DO NOTHING' para evitar duplicatas baseadas na constraint única.
    
    Args:
        db (Session): A sessão do SQLAlchemy.
        df (pd.DataFrame): DataFrame contendo os dados de klines.
                           Espera-se que as colunas do DataFrame correspondam aos nomes
                           dos campos no modelo KlineOHLCV, especialmente após a conversão
                           de 'open_time' e 'close_time' para datetime.
        symbol (str): O símbolo da criptomoeda (ex: 'BTCUSDT').
        interval (str): O intervalo da vela (ex: '1h').
    """

    if df.empty:
        print("DataFrame vazio, nada para salvar.")
        return 0
    
    records_to_insert = []
    for _, row in df.iterrows():
        record = {
            'symbol': symbol.upper(),
            'interval_time': interval,
            'open_time': row['open_time'],
            'open_price': row['open'],
            'high_price': row['high'],
            'low_price': row['low'],
            'close_price': row['close'],
            'volume': row['volume'],
            'close_time': row['close_time'],
            'quote_asset_volume': row['quote_asset_volume'],
            'number_of_trades': row['number_of_trades'],
            'taker_buy_base_asset_volume': row['taker_buy_base_asset_volume'],
            'taker_buy_quote_asset_volume': row['taker_buy_quote_asset_volume'],
        }
        records_to_insert.append(record)

    if not records_to_insert:
        print("Nenhum registro preparado para inserção.")
        return 0
    
    try:
        stmt = pg_insert(KlineOHLCV).values(records_to_insert)
        stmt = stmt.on_conflict_do_nothing(
            index_elements=['symbol', 'interval_time', 'open_time']
        )
        result = db.execute(stmt)
        db.commit()
        print(f"{len(records_to_insert)} registros tentados.")
        return result.rowcount if result else 0
    except Exception as e:
        db.rollback()
        print(f"Erro ao salvar dados no banco de dados: {e}")
        return -1
