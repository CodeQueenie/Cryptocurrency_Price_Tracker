#!/usr/bin/env python3
"""
Bitcoin Dashboard Standalone
---------------------------
A standalone dashboard for viewing Bitcoin prices.
This script combines the functionality of view_database_contents.py and view_bitcoin_history.py
into a single application that can be packaged with PyInstaller.

Copyright (c) 2025 Nicole LeGuern
Licensed under MIT License with attribution requirements
https://github.com/CodeQueenie/Cryptocurrency_Price_Tracker
"""

import os
import sys
import pandas as pd
import re
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tabulate import tabulate
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Add parent directory to path for imports from core
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from core.db_utils import get_latest_prices, get_bitcoin_history
except ImportError:
    # Fallback for standalone mode or when packaged
    pass

# Load environment variables
load_dotenv()

# Helper function to clean environment variables
def clean_env_value(value):
    if value is None:
        return None
    # Remove quotes and trailing comments
    value = value.strip()
    # Remove any quotes from the value
    value = re.sub(r'^[\'"]|[\'"]$', '', value)
    # Remove anything after a # character (comment)
    value = re.sub(r'#.*$', '', value).strip()
    return value if value else None

# Database configuration
DB_TYPE = clean_env_value(os.getenv("DB_TYPE", "postgresql"))  # postgresql or mysql
DB_HOST = clean_env_value(os.getenv("DB_HOST", "localhost"))
DB_PORT_STR = clean_env_value(os.getenv("DB_PORT", "5432" if DB_TYPE == "postgresql" else "3306"))
# Extract just the numeric part for the port
DB_PORT = int(re.sub(r'[^0-9]', '', DB_PORT_STR))
DB_NAME = clean_env_value(os.getenv("DB_NAME", "crypto_tracker"))
DB_USER = clean_env_value(os.getenv("DB_USER", "postgres" if DB_TYPE == "postgresql" else "root"))
DB_PASSWORD = clean_env_value(os.getenv("DB_PASSWORD", ""))

# Remove any quotes from the password
if DB_PASSWORD.startswith('"') and DB_PASSWORD.endswith('"'):
    DB_PASSWORD = DB_PASSWORD[1:-1]
if DB_PASSWORD.startswith("'") and DB_PASSWORD.endswith("'"):
    DB_PASSWORD = DB_PASSWORD[1:-1]

def create_db_engine():
    """Create and return a SQLAlchemy engine for database operations."""
    try:
        if DB_TYPE == "postgresql":
            connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:  # mysql
            connection_string = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Print connection string with password masked for debugging
        masked_connection = connection_string.replace(DB_PASSWORD, "********") if DB_PASSWORD else connection_string
        print(f"DEBUG: Connection string: {masked_connection}")
        
        return create_engine(connection_string)
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
        return None

def export_to_excel(df, filename="crypto_data_excel.xlsx"):
    """Export DataFrame to Excel file."""
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=filename
        )
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Data exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {str(e)}")

def plot_bitcoin_history(df):
    """Plot Bitcoin price history."""
    if df is None or df.empty:
        messagebox.showinfo("No Data", "No Bitcoin price history available.")
        return
    
    # Convert timestamp to datetime if it's not already
    if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort by timestamp
    df = df.sort_values('timestamp')
    
    # Create a new window for the plot
    plot_window = tk.Toplevel()
    plot_window.title("Bitcoin Price History")
    plot_window.geometry("800x600")
    
    # Create figure and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['timestamp'], df['price_usd'], marker='o', linestyle='-', color='orange')
    ax.set_title('Bitcoin Price History')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.grid(True)
    
    # Format y-axis as currency
    ax.yaxis.set_major_formatter('${x:,.2f}')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout
    plt.tight_layout()
    
    # Embed the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Add a close button
    close_button = ttk.Button(plot_window, text="Close", command=plot_window.destroy)
    close_button.pack(pady=10)

# Define local implementations as fallbacks if imports fail
if 'get_latest_prices' not in globals():
    def get_latest_prices():
        """Get the latest cryptocurrency prices from the database."""
        try:
            engine = create_db_engine()
            if not engine:
                return None
                
            query = """
            WITH latest_prices AS (
                SELECT 
                    coin_id,
                    MAX(timestamp) as latest_timestamp
                FROM 
                    crypto_prices
                GROUP BY 
                    coin_id
            )
            SELECT 
                cp.coin_id,
                cp.coin_name,
                cp.price_usd,
                cp.market_cap,
                cp.price_change_percentage_24h,
                cp.timestamp
            FROM 
                crypto_prices cp
            JOIN 
                latest_prices lp ON cp.coin_id = lp.coin_id AND cp.timestamp = lp.latest_timestamp
            ORDER BY 
                cp.market_cap DESC;
            """
            
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get latest prices: {str(e)}")
            return None

if 'get_bitcoin_history' not in globals():
    def get_bitcoin_history(days=7):
        """Get Bitcoin price history for the specified number of days."""
        try:
            engine = create_db_engine()
            if not engine:
                return None
                
            # Calculate the date from days ago
            days_ago = datetime.now() - timedelta(days=days)
            
            query = f"""
            SELECT 
                coin_id,
                coin_name,
                price_usd,
                timestamp,
                price_change_percentage_24h
            FROM 
                crypto_prices
            WHERE
                coin_id = 'bitcoin'
                AND timestamp >= '{days_ago.strftime('%Y-%m-%d')}'
            ORDER BY 
                timestamp DESC;
            """
            
            df = pd.read_sql(query, engine)
            return df
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get Bitcoin history: {str(e)}")
            return None

class BitcoinDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bitcoin Price Tracker Dashboard")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set theme
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        
        # Configure colors
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TButton', background='#4a7abc', foreground='black')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_label = ttk.Label(
            self.main_frame, 
            text="Bitcoin Price Tracker Dashboard", 
            style='Header.TLabel'
        )
        header_label.pack(pady=(0, 20))
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Buttons
        self.view_price_button = ttk.Button(
            self.button_frame, 
            text="View Current Bitcoin Price",
            command=self.view_current_price
        )
        self.view_price_button.pack(side=tk.LEFT, padx=5)
        
        self.view_history_button = ttk.Button(
            self.button_frame, 
            text="View Bitcoin Price History",
            command=self.view_bitcoin_history
        )
        self.view_history_button.pack(side=tk.LEFT, padx=5)
        
        self.export_button = ttk.Button(
            self.button_frame, 
            text="Export Bitcoin Data to Excel",
            command=self.export_data
        )
        self.export_button.pack(side=tk.LEFT, padx=5)
        
        self.plot_button = ttk.Button(
            self.button_frame, 
            text="Plot Bitcoin Price History",
            command=self.plot_history
        )
        self.plot_button.pack(side=tk.LEFT, padx=5)
        
        # Data display frame
        self.data_frame = ttk.Frame(self.main_frame, padding=10)
        self.data_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview for data display
        self.tree = ttk.Treeview(self.data_frame)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.data_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize with current prices
        self.view_current_price()
    
    def view_current_price(self):
        """Display current cryptocurrency prices."""
        self.status_var.set("Loading current prices...")
        self.root.update()
        
        df = get_latest_prices()
        if df is None or df.empty:
            self.status_var.set("No data available")
            return
        
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Configure columns
        self.tree['columns'] = ['coin_name', 'price_usd', 'market_cap', 'price_change_percentage_24h', 'timestamp']
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('coin_name', anchor=tk.W, width=100)
        self.tree.column('price_usd', anchor=tk.E, width=100)
        self.tree.column('market_cap', anchor=tk.E, width=150)
        self.tree.column('price_change_percentage_24h', anchor=tk.E, width=150)
        self.tree.column('timestamp', anchor=tk.W, width=150)
        
        # Configure headings
        self.tree.heading('#0', text='', anchor=tk.W)
        self.tree.heading('coin_name', text='Coin Name', anchor=tk.W)
        self.tree.heading('price_usd', text='Price (USD)', anchor=tk.E)
        self.tree.heading('market_cap', text='Market Cap', anchor=tk.E)
        self.tree.heading('price_change_percentage_24h', text='24h Change', anchor=tk.E)
        self.tree.heading('timestamp', text='Timestamp', anchor=tk.W)
        
        # Insert data
        for idx, row in df.iterrows():
            price_usd = f"${float(row['price_usd']):,.2f}"
            market_cap = f"${float(row['market_cap']):,.0f}"
            price_change = f"{float(row['price_change_percentage_24h']):+.2f}%"
            timestamp = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row['timestamp'], datetime) else row['timestamp']
            
            self.tree.insert(
                parent='', 
                index='end', 
                iid=idx, 
                values=(row['coin_name'], price_usd, market_cap, price_change, timestamp)
            )
        
        self.status_var.set(f"Displaying current prices for {len(df)} cryptocurrencies")
    
    def view_bitcoin_history(self):
        """Display Bitcoin price history."""
        # Ask for number of days
        days_window = tk.Toplevel(self.root)
        days_window.title("Select Time Period")
        days_window.geometry("300x150")
        days_window.resizable(False, False)
        
        ttk.Label(days_window, text="Enter number of days of history to view:").pack(pady=(20, 5))
        
        days_var = tk.StringVar(value="7")
        days_entry = ttk.Entry(days_window, textvariable=days_var, width=10)
        days_entry.pack(pady=5)
        
        def fetch_history():
            try:
                days = int(days_var.get())
                days_window.destroy()
                
                self.status_var.set(f"Loading Bitcoin price history for the last {days} days...")
                self.root.update()
                
                df = get_bitcoin_history(days)
                if df is None or df.empty:
                    self.status_var.set("No Bitcoin price history available")
                    return
                
                # Clear existing data
                for item in self.tree.get_children():
                    self.tree.delete(item)
                
                # Configure columns
                self.tree['columns'] = ['coin_name', 'price_usd', 'price_change_percentage_24h', 'timestamp']
                self.tree.column('#0', width=0, stretch=tk.NO)
                self.tree.column('coin_name', anchor=tk.W, width=100)
                self.tree.column('price_usd', anchor=tk.E, width=100)
                self.tree.column('price_change_percentage_24h', anchor=tk.E, width=150)
                self.tree.column('timestamp', anchor=tk.W, width=150)
                
                # Configure headings
                self.tree.heading('#0', text='', anchor=tk.W)
                self.tree.heading('coin_name', text='Coin Name', anchor=tk.W)
                self.tree.heading('price_usd', text='Price (USD)', anchor=tk.E)
                self.tree.heading('price_change_percentage_24h', text='24h Change', anchor=tk.E)
                self.tree.heading('timestamp', text='Timestamp', anchor=tk.W)
                
                # Insert data
                for idx, row in df.iterrows():
                    price_usd = f"${float(row['price_usd']):,.2f}"
                    price_change = f"{float(row['price_change_percentage_24h']):+.2f}%"
                    timestamp = row['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row['timestamp'], datetime) else row['timestamp']
                    
                    self.tree.insert(
                        parent='', 
                        index='end', 
                        iid=idx, 
                        values=(row['coin_name'], price_usd, price_change, timestamp)
                    )
                
                self.status_var.set(f"Displaying Bitcoin price history for the last {days} days ({len(df)} records)")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number of days")
        
        ttk.Button(days_window, text="View History", command=fetch_history).pack(pady=10)
        
        # Center the window
        days_window.update_idletasks()
        width = days_window.winfo_width()
        height = days_window.winfo_height()
        x = (days_window.winfo_screenwidth() // 2) - (width // 2)
        y = (days_window.winfo_screenheight() // 2) - (height // 2)
        days_window.geometry(f'{width}x{height}+{x}+{y}')
        
        days_entry.focus_set()
    
    def export_data(self):
        """Export current data to Excel."""
        if not self.tree.get_children():
            messagebox.showinfo("No Data", "No data to export.")
            return
        
        # Get column names
        columns = self.tree['columns']
        
        # Get data from treeview
        data = []
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            data.append(values)
        
        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)
        
        # Export to Excel
        export_to_excel(df)
    
    def plot_history(self):
        """Plot Bitcoin price history."""
        # Ask for number of days
        days_window = tk.Toplevel(self.root)
        days_window.title("Select Time Period")
        days_window.geometry("300x150")
        days_window.resizable(False, False)
        
        ttk.Label(days_window, text="Enter number of days to plot:").pack(pady=(20, 5))
        
        days_var = tk.StringVar(value="30")
        days_entry = ttk.Entry(days_window, textvariable=days_var, width=10)
        days_entry.pack(pady=5)
        
        def fetch_and_plot():
            try:
                days = int(days_var.get())
                days_window.destroy()
                
                self.status_var.set(f"Loading Bitcoin price history for plotting...")
                self.root.update()
                
                df = get_bitcoin_history(days)
                plot_bitcoin_history(df)
                
                self.status_var.set("Ready")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number of days")
        
        ttk.Button(days_window, text="Plot History", command=fetch_and_plot).pack(pady=10)
        
        # Center the window
        days_window.update_idletasks()
        width = days_window.winfo_width()
        height = days_window.winfo_height()
        x = (days_window.winfo_screenwidth() // 2) - (width // 2)
        y = (days_window.winfo_screenheight() // 2) - (height // 2)
        days_window.geometry(f'{width}x{height}+{x}+{y}')
        
        days_entry.focus_set()

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    app = BitcoinDashboardApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
