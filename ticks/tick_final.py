import tkinter as tk
from kiteconnect import KiteConnect
import threading

# API credentials
api_key = ''
api_secret = ''
access_token = ''  # Replace with your access token

# Create a Kite Connect instance
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Create a list of instrument tokens you are subscribed to
subscribed_instruments = ['NSE:RELIANCE', 'NSE:TATASTEEL']  # Replace with your subscribed instruments

# Function to update live data for subscribed instruments
def update_live_data():
    while True:
        for instrument_token in subscribed_instruments:
            ltp_data = kite.ltp([instrument_token])
            ltp = ltp_data[instrument_token]['last_price']
            ltp_label.config(text=f"{instrument_token} - LTP: {ltp}")
        app.update_idletasks()

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create labels to display live data
ltp_label = tk.Label(app, text="", font=('Helvetica', 16))
ltp_label.pack(pady=20)

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()
