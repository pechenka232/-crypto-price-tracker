import ccxt
import pandas as pd
import time
import matplotlib.pyplot as plt

# Выбираем биржи
binance = ccxt.binance()
okx = ccxt.okx()
bybit = ccxt.bybit()

# Функция получения данных
def fetch_ticker(exchange, symbol="BTC/USDT"):
    ticker = exchange.fetch_ticker(symbol)
    return {
        "exchange": exchange.id,
        "symbol": symbol,
        "price": ticker["last"],
        "volume": ticker["quoteVolume"],
        "timestamp": pd.to_datetime(ticker["timestamp"], unit="ms"),
    }

# Собираем данные с бирж
def collect_data():
    data = []
    for exchange in [binance, okx, bybit]:
        try:
            data.append(fetch_ticker(exchange))
        except Exception as e:
            print(f"Ошибка с {exchange.id}: {e}")
    return pd.DataFrame(data)

# Анализ волатильности
def analyze_volatility(df):
    df["change"] = df["price"].pct_change() * 100  # % изменение цены
    return df

# Построение графика волатильности
def plot_volatility(df):
    plt.figure(figsize=(10, 5))
    for exchange in df["exchange"].unique():
        subset = df[df["exchange"] == exchange]
        plt.plot(subset["timestamp"], subset["change"], label=exchange)
    
    plt.xlabel("Время")
    plt.ylabel("Изменение цены (%)")
    plt.title("Волатильность криптовалюты")
    plt.legend()
    plt.show()

# Основной цикл
if __name__ == "__main__":
    all_data = []
    
    for _ in range(5):  # Собираем данные 5 раз
        df = collect_data()
        all_data.append(df)
        time.sleep(10)  # Ждем 10 секунд
    
    full_df = pd.concat(all_data, ignore_index=True)
    full_df = analyze_volatility(full_df)

    print(full_df)
    plot_volatility(full_df)
