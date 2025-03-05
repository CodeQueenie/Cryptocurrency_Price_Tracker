# Cryptocurrency Price Tracker

A beginner-friendly tool that automatically fetches live cryptocurrency prices, stores them in a database, and provides visualization capabilities.

![Bitcoin Price Tracker](docs/bitcoin.ico)

## Important Notice

This project was created by Nicole LeGuern as a learning tool and portfolio piece. While it's open source under the MIT license, **any use of this code requires clear attribution to the original author**. This includes both personal and commercial applications.

## Features

- Fetches real-time prices for Bitcoin, Ethereum, and other cryptocurrencies using the CoinGecko API
- Stores price data in PostgreSQL, MySQL, or SQLite database
- Provides export options for Excel dashboards
- Automated data collection with Windows Task Scheduler
- Interactive visualization of Bitcoin price trends
- Comprehensive error handling and detailed logging

## Quick Start Guide

### For End Users (Standalone Application)

1. Download the latest release from the [Releases](https://github.com/CodeQueenie/Cryptocurrency_Price_Tracker/releases) page
2. Extract the ZIP file to any location on your computer
3. Run the `install.bat` file
4. Follow the on-screen instructions

### For Developers

#### Prerequisites

- Python 3.8 or higher
- PostgreSQL, MySQL, or SQLite database
- Windows operating system

#### Installation

1. Clone the repository:
   ```
   git clone https://github.com/CodeQueenie/Cryptocurrency_Price_Tracker.git
   cd Cryptocurrency_Price_Tracker
   ```

2. Run the setup script to create a virtual environment and install dependencies:
   ```
   setup_venv.bat
   ```

3. Configure your database connection in the `.env` file:
   ```
   DB_TYPE=postgresql  # or mysql, sqlite
   DB_HOST=localhost
   DB_PORT=5432  # or 3306 for MySQL, 0 for SQLite
   DB_NAME=crypto_tracker  # or path to SQLite file
   DB_USER=your_username
   DB_PASSWORD=your_password
   ```

## Project Structure

The project is organized into the following directories:

- `core/` - Core functionality for cryptocurrency tracking
  - `crypto_tracker.py` - Main class for fetching cryptocurrency data
  - `db_utils.py` - Database utility functions
  - `create_database.py` - Script to create the initial database

- `bitcoin_tracker/` - Bitcoin-specific implementation
  - `bitcoin_dashboard_standalone.py` - Standalone Bitcoin dashboard application

- `ethereum_tracker/` - Placeholder for Ethereum-specific implementation (future)

- `scripts/` - Utility scripts
  - `package_app.bat` - Script to package the application
  - `create_installer.bat` - Script to create an installer
  - `update_db_password.py` - Script to update the database password
  - `fix_db_password.py` - Script to fix database password issues

- `docs/` - Documentation
  - `SQL_QUERIES.md` - Documentation of SQL queries used
  - `FAQ.md` - Frequently asked questions

## Usage

### Tracking Cryptocurrency Prices

Run the cryptocurrency tracker to fetch and store prices:
```
run_crypto_tracker.bat
```

### Viewing Bitcoin Dashboard

Launch the Bitcoin dashboard to view current and historical prices:
```
bitcoin_dashboard.bat
```

### Viewing Bitcoin Price History

View historical Bitcoin price data:
```
view_bitcoin_history.bat
```

## Creating a Standalone Application

To create a standalone application for distribution:

1. Run the packaging script:
   ```
   package_app.bat
   ```

2. Create an installer package:
   ```
   create_installer.bat
   ```

3. The installer package will be available as `Bitcoin_Price_Tracker_Installer.zip`

## Documentation

- [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md): Guide for getting started with the application
- [docs/SQL_QUERIES.md](docs/SQL_QUERIES.md): Documentation of SQL queries used in the application
- [docs/FAQ.md](docs/FAQ.md): Frequently asked questions
- [REORGANIZATION_COMPLETE.md](REORGANIZATION_COMPLETE.md): Summary of the project reorganization

## License

This project is licensed under the MIT License with an additional attribution requirement - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CoinGecko API](https://www.coingecko.com/en/api) for providing cryptocurrency data
- All contributors to the open-source libraries used in this project
