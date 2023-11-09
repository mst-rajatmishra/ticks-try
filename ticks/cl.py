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

# Get a list of all instruments
instruments = kite.ltp(['NSE:RELIANCE', 'NSE:TATASTEEL', 'NSE:INFY'])  # Replace with your subscribed instruments
instrument_tokens = list(instruments.keys())

# Dictionary to store P&L for each instrument
pnl_data = {instrument_token: 0.0 for instrument_token in instrument_tokens}

# Function to update live data and P&L
def update_live_data():
    while True:
        ltp_data = kite.ltp(instrument_tokens)

        for instrument_token, ltp in ltp_data.items():
            pnl = calculate_profit_loss(instrument_token, ltp['last_price'])
            pnl_label = pnl_labels[instrument_token]
            pnl_label.config(text=f"P&L: {pnl}", fg='green' if pnl >= 0 else 'red')

        app.update_idletasks()

# Function to calculate profit and loss
def calculate_profit_loss(instrument_token, current_price):
    # Replace this with your logic to calculate profit and loss
    # This is a simplified example
    previous_price = 100.0  # Replace with the initial price or a stored value
    pnl = (current_price - previous_price) * 10  # Assuming 10 quantities for simplicity
    pnl_data[instrument_token] = pnl
    return pnl

# Function to filter instruments based on search
def filter_instruments():
    search_text = search_entry.get().upper()
    filtered_tokens = [token for token in instrument_tokens if search_text in token]
    
    for token in instrument_tokens:
        frame = pnl_frames[token]
        if token in filtered_tokens:
            frame.pack()
        else:
            frame.pack_forget()

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create a search entry
search_entry = tk.Entry(app)
search_entry.pack(pady=10)
search_button = tk.Button(app, text="Search", command=filter_instruments)
search_button.pack()

# Create frames and labels for each instrument
pnl_frames = {}
pnl_labels = {}  # Corrected line
for instrument_token in instrument_tokens:
    frame = tk.Frame(app)
    frame.pack(pady=10)

    label = tk.Label(frame, text=f"{instrument_token} - LTP: ", font=('Helvetica', 12))
    label.pack(side=tk.LEFT)

    pnl_label = tk.Label(frame, text="P&L: ", font=('Helvetica', 12))
    pnl_label.pack(side=tk.RIGHT)
    pnl_labels[instrument_token] = pnl_label
    pnl_frames[instrument_token] = frame

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()
