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
- Conda package manager (recommended)
- PostgreSQL or MySQL database
- Power BI, Tableau, or Excel (for visualization)

### Installation

1. **One-Click Setup with Conda (Recommended)**:
   - Windows: Double-click `setup.bat`
   - This will create a Conda environment and install all dependencies

2. **Manual Setup**:
   - Create a Conda environment: `conda create -n crypto_tracker python=3.9`
   - Activate the environment: `conda activate crypto_tracker`
   - Install dependencies: `conda install --file requirements.txt`
   - Configure your database connection in `.env` file

### Configuration

1. Copy `.env.example` to `.env`
2. Edit `.env` with your database credentials and preferences
3. Customize which cryptocurrencies to track and update frequency

### Running the Application

- **Manual**: Run `python crypto_tracker.py`
- **Automated**: Run `python setup_scheduler.py` to set up automated data collection with Windows Task Scheduler

### Visualizing Data

1. Export data for visualization: `python export_for_visualization.py`
2. Options for export formats:
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
- `setup_scheduler.py`: Sets up automated data collection
- `test_db_connection.py`: Tests database connectivity

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
