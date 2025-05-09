import os
import requests
import pandas as pd
from datetime import datetime, timezone
import time

BINANCE_API_BASE_URL = "https://api.binance.com/api/v3"

def get_klines(symbol: str, interval: str, start_time_ms: int = None, end_time_ms: int = None, limit: int = 1000):
    """
    Busca dados de klines (OHLCV) da API da Binance.
    Retorna uma lista de listas ou None em caso de erro.
    """
    endpoint = f"{BINANCE_API_BASE_URL}/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": min(limit, 1000)
    }

    if start_time_ms:
        params["startTime"] = start_time_ms
    if end_time_ms:
        params["endTime"] = end_time_ms

    print(f"Buscando as últimas {params['limit']} velas para {symbol} ({interval})...")
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar klines para {symbol} ({interval}): {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado ao processar klines para {symbol} ({interval}): {e}")
        return None
    
def klines_to_dataframe(klines_data):
    """Converte os dados brutos de klines para um DataFrame Pandas."""
    if not klines_data:
        return pd.DataFrame()

    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ]
    df = pd.DataFrame(klines_data, columns=columns)

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

    numeric_cols = ["open", "high", "low", "close", "volume",
                    "quote_asset_volume", "taker_buy_base_asset_volume",
                    "taker_buy_quote_asset_volume"]
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    df["number_of_trades"] = pd.to_numeric(df["number_of_trades"])

    df.drop(columns=['ignore'], inplace=True, errors='ignore')

    return df
    
if __name__ == "__main__":
    symbol_test = "BTCUSDT"
    # '1m', '5m', '15m', '30m', '1h', '2h', '4h', '1d'
    interval_test = "1d"
    number_of_klines_to_test = 1000

    print(f"Iniciando coleta dos últimos {number_of_klines_to_test} klines para {symbol_test} ({interval_test}).")

    raw_data = get_klines(symbol_test, interval_test, limit=number_of_klines_to_test)

    if raw_data:
        df_klines = klines_to_dataframe(raw_data)

        if not df_klines.empty:
            output_dir = "data/raw"
            os.makedirs(output_dir, exist_ok=True)
            
            timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"{output_dir}/{symbol_test}_{interval_test}_latest_{len(df_klines)}_{timestamp_str}.csv"
            
            try:
                df_klines.to_csv(filename, index=False)
                print(f"\nDados salvos em: {filename}")
            except Exception as e:
                print(f"Erro ao salvar o arquivo CSV: {e}")
        else:
            print("O DataFrame resultante está vazio após a conversão.")
    else:
        print(f"Nenhum dado foi retornado pela API para {symbol_test}.")
