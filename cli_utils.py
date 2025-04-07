import argparse
from datetime import datetime
from finance_utils import get_possible_expiration_dates
def get_args():
    parser = argparse.ArgumentParser(description='Analyze Cash Secured Put options for a given stock')
    parser.add_argument(
        'ticker', 
        type=str, 
        help='Stock ticker symbol (e.g., AAPL)'
    )
    parser.add_argument(
        '--expiration-date', 
        '-e',
        type=str, 
        help='Option expiration date in YYYY-MM-DD format. If not provided, will show available dates.'
    )
    parser.add_argument(
        '--target-return', 
        '-t',
        type=float, 
        default=10,
        help='Target annualized return percentage (default: 10)'
    )
    args = parser.parse_args()
    
    if args.expiration_date:
        try:
            datetime.strptime(args.expiration_date, '%Y-%m-%d')
        except ValueError:
            parser.error("Expiration date must be in YYYY-MM-DD format")
    
    return args

def select_expiration_date(ticker_symbol: str) -> str:
    available_dates = get_possible_expiration_dates(ticker_symbol)
    
    print("\nAvailable expiration dates:")
    for idx, date in enumerate(available_dates, 1):
        print(f"{idx}. {date}")
    
    while True:
        try:
            choice = input("\nSelect a date (enter the number): ")
            idx = int(choice) - 1
            if 0 <= idx < len(available_dates):
                selected_date = available_dates[idx]
                return selected_date
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def process_cli_args() -> dict:

    args = get_args()
    ticker_symbol = args.ticker.upper()
    target_return = args.target_return
    expiration_date = args.expiration_date

    if not expiration_date:
        expiration_date = select_expiration_date(args.ticker)
        print(f"\nSelected expiration date: {expiration_date}")
        print("\n--------------------------------\n")
    
    ticker_symbol = args.ticker.upper()
    return {
        "ticker_symbol": ticker_symbol,
        "expiration_date": expiration_date,
        "target_return": target_return
    }