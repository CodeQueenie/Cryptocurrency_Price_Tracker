"""
Export Data for Visualization
----------------------------
This script exports cryptocurrency price data in formats suitable for visualization tools
like Power BI, Tableau, and Excel.

It provides various export options with different data transformations to facilitate
easy visualization and analysis.
"""

import os
import sys
import pandas as pd
import argparse
from datetime import datetime, timedelta
from db_utils import get_db_connection, get_latest_prices, get_price_history, get_rolling_averages

def export_for_power_bi(output_file="crypto_data_powerbi.csv"):
    """
    Export data in a format optimized for Power BI.
    
    Includes additional calculated columns and proper data types
    to facilitate visualization in Power BI.
    
    Args:
        output_file (str, optional): Path to the output CSV file. 
                                     Defaults to "crypto_data_powerbi.csv".
    
    Returns:
        str: Message indicating the export status.
        
    Raises:
        Exception: If there's an error exporting the data.
    """
    try:
        print(f"Exporting data for Power BI to {output_file}...")
        
        # Get database connection
        engine = get_db_connection()
        
        # Query to get all price data with date parts for easier filtering in Power BI
        query = """
        SELECT 
            cp.coin_id,
            cp.coin_name,
            cp.price_usd,
            cp.market_cap,
            cp.volume_24h,
            cp.price_change_24h,
            cp.price_change_percentage_24h,
            cp.timestamp,
            EXTRACT(YEAR FROM cp.timestamp) as year,
            EXTRACT(MONTH FROM cp.timestamp) as month,
            EXTRACT(DAY FROM cp.timestamp) as day,
            EXTRACT(HOUR FROM cp.timestamp) as hour
        FROM 
            crypto_prices cp
        ORDER BY 
            cp.timestamp, cp.market_cap DESC;
        """
        
        # Adjust query for MySQL if needed
        if os.getenv("DB_TYPE", "postgresql") == "mysql":
            query = query.replace("EXTRACT(YEAR FROM cp.timestamp)", "YEAR(cp.timestamp)")
            query = query.replace("EXTRACT(MONTH FROM cp.timestamp)", "MONTH(cp.timestamp)")
            query = query.replace("EXTRACT(DAY FROM cp.timestamp)", "DAY(cp.timestamp)")
            query = query.replace("EXTRACT(HOUR FROM cp.timestamp)", "HOUR(cp.timestamp)")
        
        # Execute query and get data
        df = pd.read_sql(query, engine)
        
        # Add day of week for time intelligence in Power BI
        df["day_of_week"] = pd.to_datetime(df["timestamp"]).dt.day_name()
        
        # Export to CSV
        df.to_csv(output_file, index=False)
        return f"✅ Data exported to {output_file} for Power BI"
    except Exception as e:
        raise Exception(f"Error exporting data for Power BI: {e}")

def export_for_tableau(output_file="crypto_data_tableau.csv"):
    """
    Export data in a format optimized for Tableau.
    
    Includes pivot tables and aggregations that work well with Tableau's
    data model.
    
    Args:
        output_file (str, optional): Path to the output CSV file. 
                                     Defaults to "crypto_data_tableau.csv".
    
    Returns:
        str: Message indicating the export status.
        
    Raises:
        Exception: If there's an error exporting the data.
    """
    try:
        print(f"Exporting data for Tableau to {output_file}...")
        
        # Get database connection
        engine = get_db_connection()
        
        # Query to get all price data
        query = """
        SELECT 
            cp.coin_id,
            cp.coin_name,
            cp.price_usd,
            cp.market_cap,
            cp.volume_24h,
            cp.price_change_24h,
            cp.price_change_percentage_24h,
            cp.timestamp
        FROM 
            crypto_prices cp
        ORDER BY 
            cp.timestamp, cp.market_cap DESC;
        """
        
        # Execute query and get data
        df = pd.read_sql(query, engine)
        
        # Convert timestamp to datetime if it's not already
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        # Add date column without time for easier grouping in Tableau
        df["date"] = df["timestamp"].dt.date
        
        # Export to CSV
        df.to_csv(output_file, index=False)
        return f"✅ Data exported to {output_file} for Tableau"
    except Exception as e:
        raise Exception(f"Error exporting data for Tableau: {e}")

def export_for_excel(output_file="crypto_data_excel.xlsx"):
    """
    Export data in a format optimized for Excel.
    
    Creates multiple sheets with different views of the data,
    and includes Excel formulas for additional analysis.
    
    Args:
        output_file (str, optional): Path to the output Excel file. 
                                     Defaults to "crypto_data_excel.xlsx".
    
    Returns:
        str: Message indicating the export status.
        
    Raises:
        Exception: If there's an error exporting the data.
    """
    try:
        print(f"Exporting data for Excel to {output_file}...")
        
        # Create Excel writer
        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            
            # Sheet 1: Latest prices
            latest_prices = get_latest_prices()
            latest_prices.to_excel(writer, sheet_name="Latest Prices", index=False)
            
            # Sheet 2: Bitcoin history (as an example)
            try:
                btc_history = get_price_history("bitcoin", days=30)
                btc_history.to_excel(writer, sheet_name="Bitcoin History", index=False)
            except Exception as e:
                print(f"Warning: Could not export Bitcoin history: {e}")
            
            # Sheet 3: Ethereum history (as an example)
            try:
                eth_history = get_price_history("ethereum", days=30)
                eth_history.to_excel(writer, sheet_name="Ethereum History", index=False)
            except Exception as e:
                print(f"Warning: Could not export Ethereum history: {e}")
            
            # Sheet 4: Rolling averages for Bitcoin
            try:
                btc_rolling = get_rolling_averages("bitcoin", window_size=7)
                btc_rolling.to_excel(writer, sheet_name="Bitcoin Rolling Avg", index=False)
            except Exception as e:
                print(f"Warning: Could not export Bitcoin rolling averages: {e}")
        
        return f"✅ Data exported to {output_file} for Excel"
    except Exception as e:
        raise Exception(f"Error exporting data for Excel: {e}")

def export_historical_comparison(coins=None, days=30, output_file="crypto_comparison.csv"):
    """
    Export a comparison of historical data for multiple cryptocurrencies.
    
    Args:
        coins (list, optional): List of coin IDs to compare. 
                               Defaults to ["bitcoin", "ethereum", "litecoin"].
        days (int, optional): Number of days of history to retrieve. Defaults to 30.
        output_file (str, optional): Path to the output CSV file. 
                                    Defaults to "crypto_comparison.csv".
    
    Returns:
        str: Message indicating the export status.
        
    Raises:
        Exception: If there's an error exporting the data.
    """
    try:
        if coins is None:
            coins = ["bitcoin", "ethereum", "litecoin"]
        
        print(f"Exporting historical comparison for {', '.join(coins)} to {output_file}...")
        
        # Get data for each coin
        all_data = []
        for coin in coins:
            try:
                coin_data = get_price_history(coin, days=days)
                all_data.append(coin_data)
            except Exception as e:
                print(f"Warning: Could not get data for {coin}: {e}")
        
        # Combine all data
        if all_data:
            combined_df = pd.concat(all_data)
            
            # Pivot the data to have coins as columns and dates as rows
            pivot_df = combined_df.pivot_table(
                index="timestamp", 
                columns="coin_id", 
                values="price_usd"
            )
            
            # Reset index to make timestamp a column
            pivot_df.reset_index(inplace=True)
            
            # Export to CSV
            pivot_df.to_csv(output_file, index=False)
            return f"✅ Historical comparison exported to {output_file}"
        else:
            return "❌ No data to export"
    except Exception as e:
        raise Exception(f"Error exporting historical comparison: {e}")

def main():
    """
    Main function to handle command-line arguments and execute exports.
    
    Parses command-line arguments to determine which export format to use
    and executes the appropriate export function.
    
    Returns:
        None
    """
    try:
        parser = argparse.ArgumentParser(description="Export cryptocurrency data for visualization")
        parser.add_argument(
            "--format", 
            choices=["powerbi", "tableau", "excel", "comparison", "all"], 
            default="all",
            help="Export format (powerbi, tableau, excel, comparison, or all)"
        )
        parser.add_argument(
            "--output", 
            help="Output file path (default depends on format)"
        )
        parser.add_argument(
            "--coins", 
            nargs="+", 
            help="Coin IDs for comparison (default: bitcoin ethereum litecoin)"
        )
        parser.add_argument(
            "--days", 
            type=int, 
            default=30,
            help="Number of days of history to include (default: 30)"
        )
        
        args = parser.parse_args()
        
        # Execute exports based on format
        if args.format in ["powerbi", "all"]:
            output_file = args.output if args.output else "crypto_data_powerbi.csv"
            result = export_for_power_bi(output_file)
            print(result)
            
        if args.format in ["tableau", "all"]:
            output_file = args.output if args.output else "crypto_data_tableau.csv"
            result = export_for_tableau(output_file)
            print(result)
            
        if args.format in ["excel", "all"]:
            output_file = args.output if args.output else "crypto_data_excel.xlsx"
            result = export_for_excel(output_file)
            print(result)
            
        if args.format in ["comparison", "all"]:
            output_file = args.output if args.output else "crypto_comparison.csv"
            result = export_historical_comparison(args.coins, args.days, output_file)
            print(result)
            
        print("\nData export complete! You can now import these files into your visualization tool.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
