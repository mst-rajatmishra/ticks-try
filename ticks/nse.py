import nsepy
from datetime import datetime

# Get the list of all companies
all_symbols = nsepy.get_stock_codes()
companies_with_space = [symbol for symbol in all_symbols if ' ' in all_symbols[symbol]]

print(companies_with_space)
