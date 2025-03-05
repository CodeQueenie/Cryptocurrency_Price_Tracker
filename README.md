# Cryptocurrency Price Tracker

A beginner-friendly tool that automatically fetches live cryptocurrency prices, stores them in a database, and provides visualization capabilities.

## Features

- Fetches real-time prices for Bitcoin, Ethereum, and other cryptocurrencies using the CoinGecko API
- Stores price data in a PostgreSQL or MySQL database
- Provides export options for Power BI, Tableau, and Excel dashboards
- Automated data collection with Windows Task Scheduler
- Optimized SQL queries for trend analysis and market insights
- Comprehensive error handling and detailed logging

## Quick Start Guide

### Prerequisites

- Python 3.8 or higher
- PostgreSQL or MySQL database
- Power BI, Tableau, or Excel (for visualization)

### Installation

1. **One-Click Setup**:
   - Windows: Double-click `setup.bat`
   - This will create a virtual environment, install all dependencies, and set up the database

2. **Manual Setup**:
   - Create a virtual environment: `python -m venv venv`
   - Activate the virtual environment: 
     - Windows: `venv\Scripts\activate`
     - Linux/Mac: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`
   - Create the database: `python create_database.py`
   - Configure your database connection in `.env` file

### Configuration

1. Copy `.env.example` to `.env`
2. Edit `.env` with your database credentials and preferences
3. Customize which cryptocurrencies to track and update frequency

### Running the Application

- **Manual**: 
   1. Activate the virtual environment: `venv\Scripts\activate`
   2. Run the tracker: `python crypto_tracker.py`
- **Automated**: Add `run_crypto_tracker.bat` to Windows Task Scheduler

### Visualizing Data

1. Activate the virtual environment: `venv\Scripts\activate`
2. Export data for visualization: `python export_for_visualization.py`
3. Options for export formats:
   - `--format powerbi`: Optimized for Power BI
   - `--format tableau`: Optimized for Tableau
   - `--format excel`: Creates multi-sheet Excel workbook
   - `--format comparison`: Creates comparison of multiple cryptocurrencies
   - `--format all`: Exports all formats

## Dashboard Features

- **Crypto Price Heatmap**: Track price fluctuations
- **Portfolio Performance**: Calculate investment returns
- **Market Trends**: Detect bullish/bearish trends using SQL rolling averages
- **Time-Series Analysis**: Visualize price movements over time

## Project Structure

- `crypto_tracker.py`: Main script for fetching and storing cryptocurrency data
- `db_utils.py`: Database utility functions and optimized SQL queries
- `export_for_visualization.py`: Data export tools for visualization
- `create_database.py`: Creates the database for storing cryptocurrency data
- `run_crypto_tracker.bat`: Batch file for running the tracker (for Task Scheduler)
- `test_db_connection.py`: Tests database connectivity
- `view_database_contents.py`: View the latest cryptocurrency prices stored in the database

## Virtual Environment

This project uses a Python virtual environment to isolate dependencies and avoid conflicts:

- The virtual environment is stored in the `venv` directory
- Always activate the virtual environment before running any scripts
- The setup.bat script will create and configure the virtual environment for you
- All required packages are listed in requirements.txt

## Coding Style Guidelines

This project follows these coding style guidelines:

1. String literals use double quotes
2. Variable names use snake_case
3. Comprehensive error handling with try-except blocks
4. Detailed docstrings for all functions and modules

## Troubleshooting

For common issues and solutions, please see the FAQ document in the docs folder.

## License

MIT
