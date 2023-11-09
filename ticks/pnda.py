import tkinter as tk
from kiteconnect import KiteConnect
from datetime import datetime
import threading
import pandas as pd

# API credentials
api_key = ''
api_secret = ''
access_token = ''  # Replace with your access token

# Create a Kite Connect instance
kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

# Create a list of instrument tokens you are subscribed to
subscribed_instruments = ['NSE:RELIANCE', 'NSE:TATASTEEL']  # Replace with your subscribed instruments

# Create a DataFrame to store tick-by-tick data
columns = ['Timestamp'] + subscribed_instruments
tick_data_df = pd.DataFrame(columns=columns)

# Function to update live data for subscribed instruments and save to DataFrame
def update_live_data():
    while True:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ltp_data = kite.ltp(subscribed_instruments)
        
        row_data = [timestamp] + [ltp_data[instrument]['last_price'] for instrument in subscribed_instruments]
        tick_data_df.loc[len(tick_data_df)] = row_data
        app.update_idletasks()

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create labels to display live data for each subscribed instrument
for instrument_token in subscribed_instruments:
    tk.Label(app, text=f"{instrument_token} - LTP:", font=('Helvetica', 16)).pack(pady=5)

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()

# Save the DataFrame to Excel file when the application is closed
tick_data_df.to_excel('tick_data.xlsx', index=False)
