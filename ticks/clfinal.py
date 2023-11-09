import tkinter as tk
from kiteconnect import KiteConnect
import threading
import time

# API credentials
api_key = ''
api_secret = ''
access_token = ''  # Replace with your access token

# Create a Kite Connect instance
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Function to update live data for subscribed instruments
def update_live_data():
    while True:
        ltp_data = kite.ltp(subscribed_instruments)
        for instrument_token, ltp in ltp_data.items():
            update_gui(instrument_token, ltp['last_price'])
        time.sleep(1)  # Update every second

def update_gui(instrument_token, last_price):
    pnl = calculate_pnl(instrument_token, last_price)
    stock_label = stock_labels[instrument_token]
    pnl_label = pnl_labels[instrument_token]

    stock_label.config(text=f"{instrument_token} - LTP: {last_price}")
    pnl_label.config(text=f"Profit/Loss: {pnl}", fg="green" if pnl >= 0 else "red")

def calculate_pnl(instrument_token, last_price):
    # Replace with your logic to calculate profit/loss
    # Example: Subtracting the last price from a hypothetical buy price
    return last_price - hypothetical_buy_price[instrument_token]

# Function to search for instruments
def search_instruments():
    query = search_var.get().upper()
    matching_instruments = [instrument for instrument in all_instruments if query in instrument]
    
    # Update the listbox
    listbox.delete(0, tk.END)
    for instrument in matching_instruments:
        listbox.insert(tk.END, instrument)

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create labels and variables
stock_labels = {}
pnl_labels = {}
hypothetical_buy_price = {}  # Replace with your actual buy prices
search_var = tk.StringVar()
search_var.trace("w", lambda name, index, mode: search_instruments())

# Create a list of all instruments
all_instruments = ['NSE:RELIANCE', 'NSE:TATASTEEL', 'NSE:INFY']  # Add more instruments as needed
subscribed_instruments = all_instruments

# Create a listbox for instrument search
listbox = tk.Listbox(app)
listbox.pack()

# Create labels to display live data for each subscribed instrument
for instrument_token in subscribed_instruments:
    stock_label = tk.Label(app, text="", font=('Helvetica', 12))
    pnl_label = tk.Label(app, text="", font=('Helvetica', 12))
    stock_labels[instrument_token] = stock_label
    pnl_labels[instrument_token] = pnl_label

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()
