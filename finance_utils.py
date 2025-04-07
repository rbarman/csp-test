import datetime
import yfinance as yf
import pandas as pd


def get_possible_expiration_dates(ticker_symbol: str) -> list:
    ticker = yf.Ticker(ticker_symbol)
    _ = ticker.option_chain()
    return list(ticker._expirations.keys())

def get_puts_option_chain(ticker_symbol: str, expiration_date: str) -> pd.DataFrame:
    print(f"Getting puts option chain for {ticker_symbol} at {expiration_date}")
    ticker = yf.Ticker(ticker_symbol)
    options_chain = ticker.option_chain(date=expiration_date)
    puts_df = options_chain.puts
    if puts_df.empty:
        raise ValueError(f"No puts option chain found for {ticker_symbol} at {expiration_date}")
    return puts_df


def get_dte(expiration_date: str) -> int:
    # expiration_date like "2025-04-11"
    today = datetime.date.today().isoformat()
    dte = (datetime.datetime.strptime(expiration_date, '%Y-%m-%d') - datetime.datetime.strptime(today, '%Y-%m-%d')).days
    return dte


if __name__ == "__main__":
    print(get_possible_expiration_dates("AAPL"))