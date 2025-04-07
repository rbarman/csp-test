import duckdb
import pandas as pd
import matplotlib.pyplot as plt
from finance_utils import get_puts_option_chain, get_dte
import argparse
from datetime import datetime


def execute_query(query_path: str, params: dict = {}) -> pd.DataFrame:
    with open(query_path, "r") as f:
        query = f.read()
    query = query.format(**params)
    print(query)
    return duckdb.query(query).to_df()


def plot_csp_analysis(df: pd.DataFrame, details: dict, target_return: float = 10):
    plt.plot(df['strike'], df['annualized_return'], label='Annualized Return', marker='o')
    plt.xlabel('Strike Price')
    plt.ylabel('Annualized Return')
    plt.title(f'Annualized Return vs. Strike Price [PUT {details["ticker_symbol"]} at {details["expiration_date"]}]')

    plt.axhline(y=target_return, color='red', linestyle='--', label=f'Target Return ({target_return}%)')

    # Find intersection point(s)
    strikes = df['strike'].values
    returns = df['annualized_return'].values

    intersection_x = None

    for i in range(len(returns) - 1):
        if (returns[i] - target_return) * (returns[i+1] - target_return) < 0:
            # Linear interpolation
            x0, x1 = strikes[i], strikes[i+1]
            y0, y1 = returns[i], returns[i+1]
            intersection_x = x0 + (target_return - y0) * (x1 - x0) / (y1 - y0)

            # Plot the intersection
            plt.scatter(intersection_x, target_return, color='green', zorder=5)
            plt.text(intersection_x, target_return + 0.005,
                    f'.       {intersection_x:.2f}', color='green')
            break  # If you want only the first intersection, otherwise remove this line

    plt.legend()
    plt.grid(True)
    plt.show()


def get_args():
    
    parser = argparse.ArgumentParser(description='Analyze Cash Secured Put options for a given stock')
    parser.add_argument(
        'ticker', 
        type=str, 
        help='Stock ticker symbol (e.g., AAPL)'
    )
    parser.add_argument(
        '--expiration_date', 
        '-e',
        default=datetime.now().strftime('%Y-%m-%d'),
        type=str, 
        help='Option expiration date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--target-return', 
        '-t',
        type=float, 
        default=10,
        help='Target annualized return percentage (default: 10)'
    )
    args = parser.parse_args()
    try:
        datetime.strptime(args.expiration_date, '%Y-%m-%d')
    except ValueError:
        parser.error("Expiration date must be in YYYY-MM-DD format")
    return args

if __name__ == "__main__":
    
    args = get_args()
    ticker_symbol = args.ticker.upper()
    expiration_date = args.expiration_date

    puts_df = get_puts_option_chain(ticker_symbol, expiration_date)

    df = execute_query(
        query_path="./csp_analysis_query.sql",
        params={
            "DTE": get_dte(expiration_date), 
            "tbl": "puts_df"
        }
    )
    print(df.head())

    plot_csp_analysis(
        df, 
        details = {
            "ticker_symbol": ticker_symbol,
            "expiration_date": expiration_date
        },
        target_return=args.target_return
    )