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
        ltp_data = kite.ltp(subscribed_instruments)
        for instrument_token, ltp in ltp_data.items():
            # Calculate profit/loss (dummy calculation, replace with your strategy)
            pnl = ltp['last_price'] - 1000  # Dummy example, assuming entry price was 1000

            # Update GUI labels
            ltp_label = ltp_labels[instrument_token]
            pnl_label = pnl_labels[instrument_token]

            ltp_label.config(text=f"{instrument_token} - LTP: {ltp['last_price']}")
            
            if pnl >= 0:
                pnl_label.config(text=f"Profit: {pnl}", fg='green')
            else:
                pnl_label.config(text=f"Loss: {abs(pnl)}", fg='red')
                
        app.update_idletasks()

# Function to search instruments
def search_instruments():
    query = search_var.get().upper()
    result_listbox.delete(0, tk.END)
    matching_instruments = [instrument for instrument in subscribed_instruments if query in instrument]
    for instrument in matching_instruments:
        result_listbox.insert(tk.END, instrument)

# Create the main application window
app = tk.Tk()
app.title("Zerodha Live Market Data")

# Create labels to display live data and profit/loss for each subscribed instrument
ltp_labels = {}
pnl_labels = {}
for instrument_token in subscribed_instruments:
    ltp_label = tk.Label(app, text="", font=('Helvetica', 16))
    ltp_label.pack(pady=10)
    ltp_labels[instrument_token] = ltp_label

    pnl_label = tk.Label(app, text="", font=('Helvetica', 12))
    pnl_label.pack(pady=5)
    pnl_labels[instrument_token] = pnl_label

# Create a search box
search_var = tk.StringVar()
search_entry = tk.Entry(app, textvariable=search_var, font=('Helvetica', 12))
search_entry.pack(pady=10)

# Create a search button
search_button = tk.Button(app, text="Search", command=search_instruments)
search_button.pack(pady=5)

# Create a listbox to display search results
result_listbox = tk.Listbox(app, selectmode=tk.SINGLE, font=('Helvetica', 12), height=5)
result_listbox.pack(pady=10)

# Create a thread for updating live data
data_thread = threading.Thread(target=update_live_data)
data_thread.daemon = True
data_thread.start()

# Start the GUI application
app.mainloop()
