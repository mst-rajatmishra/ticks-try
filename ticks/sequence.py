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

# Create a list of instrument tokens you are subscribed to
subscribed_instruments = ['NSE:RELIANCE', 'NSE:TATASTEEL']  # Replace with your subscribed instruments

# Function to update live data for subscribed instruments
def update_live_data():
    while True:
        for i, instrument_token in enumerate(subscribed_instruments):
            ltp_data = kite.ltp([instrument_token])
            ltp = ltp_data[instrument_token]['last_price']
            ltp_labels[i].config(text=f"{instrument_token} - LTP: {ltp}")
        app.update_idletasks()
        time.sleep(1)  # Update every second

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create labels to display live data for each subscribed instrument
ltp_labels = []
for i in range(len(subscribed_instruments)):
    ltp_label = tk.Label(app, text="", font=('Helvetica', 16))
    ltp_label.grid(row=i, column=0, pady=10)
    ltp_labels.append(ltp_label)

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()
