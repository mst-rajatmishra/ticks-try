import tkinter as tk
from kiteconnect import KiteConnect

# API credentials
api_key = ''
api_secret = ''


# Create a Kite Connect instance
kite = KiteConnect(api_key=api_key)

# Generate an access token (You'll need to get the request token manually)
access_token = ''
kite.set_access_token(access_token)

# Function to update the live data
def update_live_data():
    instrument_token = 'NSE:ADANIPORTS'  # Replace with the instrument you want to subscribe to

    # Get live market data
    ltp_data = kite.ltp([instrument_token])
    ltp = ltp_data[instrument_token]['last_price']

    # Update the label with live data
    ltp_label.config(text=f"LTP: {ltp}")

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create a label for live data
ltp_label = tk.Label(app, text="LTP: ", font=('Helvetica', 16))
ltp_label.pack(pady=20)

# Create a button to fetch live data
update_button = tk.Button(app, text="Update", command=update_live_data)
update_button.pack()

# Start the GUI application
app.mainloop()
