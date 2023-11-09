import tkinter as tk
from kiteconnect import KiteConnect
from datetime import datetime
import threading

# API credentials
api_key = ''
api_secret = ''
access_token = ''

# Replace with your access token

# Create a Kite Connect instance
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Create a list of instrument tokens you are subscribed to
subscribed_instruments = ['NSE:RELIANCE', 'NSE:TATASTEEL']  # Replace with your subscribed instruments

# Dictionary to store live data for each instrument
live_data = {instrument_token: {'ltp': 0, 'pnl_percentage': 0} for instrument_token in subscribed_instruments}

# Dictionary to store daily and overall PnL values
daily_pnl = {instrument_token: 0 for instrument_token in subscribed_instruments}
overall_pnl = {instrument_token: 0 for instrument_token in subscribed_instruments}

# Current date to track per day PnL
current_date = datetime.now().date()

# Function to update live data for subscribed instruments
def update_live_data():
    while True:
        for instrument_token in subscribed_instruments:
            ltp_data = kite.ltp([instrument_token])
            ltp = ltp_data[instrument_token]['last_price']
            live_data[instrument_token]['ltp'] = ltp

            # Calculate a simplified profit/loss percentage for demonstration purposes
            base_price = 1000  # Assuming a base price of 1000
            pnl_percentage = ((ltp - base_price) / base_price) * 100
            live_data[instrument_token]['pnl_percentage'] = pnl_percentage

            # Update daily and overall PnL
            update_pnl(instrument_token)
            
            # Update the GUI labels
            update_gui()
        app.update_idletasks()

# Function to update daily and overall PnL
def update_pnl(instrument_token):
    global current_date
    today = datetime.now().date()

    if today != current_date:
        # Reset daily PnL for the new day
        daily_pnl[instrument_token] = 0
        current_date = today

    # Update daily and overall PnL
    daily_pnl[instrument_token] += live_data[instrument_token]['pnl_percentage']
    overall_pnl[instrument_token] += live_data[instrument_token]['pnl_percentage']

# Function to update the GUI labels
def update_gui():
    for instrument_token, data in live_data.items():
        ltp_label = ltp_labels[instrument_token]
        pnl_label = pnl_labels[instrument_token]
        daily_pnl_label = daily_pnl_labels[instrument_token]
        overall_pnl_label = overall_pnl_labels[instrument_token]

        ltp_label.config(text=f"{instrument_token} - LTP: {data['ltp']}")
        pnl_label.config(text=f"PnL: {data['pnl_percentage']:.2f}%", fg='green' if data['pnl_percentage'] >= 0 else 'red')
        daily_pnl_label.config(text=f"Daily PnL: {daily_pnl[instrument_token]:.2f}%", fg='green' if daily_pnl[instrument_token] >= 0 else 'red')
        overall_pnl_label.config(text=f"Overall PnL: {overall_pnl[instrument_token]:.2f}%", fg='green' if overall_pnl[instrument_token] >= 0 else 'red')

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create labels to display live data for each subscribed instrument
ltp_labels = {}
pnl_labels = {}
daily_pnl_labels = {}
overall_pnl_labels = {}
for instrument_token in subscribed_instruments:
    ltp_label = tk.Label(app, text="", font=('Helvetica', 16))
    ltp_label.pack(pady=20)
    ltp_labels[instrument_token] = ltp_label

    pnl_label = tk.Label(app, text="", font=('Helvetica', 16))
    pnl_label.pack(pady=10)
    pnl_labels[instrument_token] = pnl_label

    daily_pnl_label = tk.Label(app, text="", font=('Helvetica', 16))
    daily_pnl_label.pack(pady=10)
    daily_pnl_labels[instrument_token] = daily_pnl_label

    overall_pnl_label = tk.Label(app, text="", font=('Helvetica', 16))
    overall_pnl_label.pack(pady=10)
    overall_pnl_labels[instrument_token] = overall_pnl_label

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()
