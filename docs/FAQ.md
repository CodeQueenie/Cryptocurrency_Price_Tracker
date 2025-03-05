# Frequently Asked Questions (FAQ)

## General Questions

### What is the Cryptocurrency Price Tracker?
The Cryptocurrency Price Tracker is a beginner-friendly tool that automatically fetches live cryptocurrency prices using the CoinGecko API, stores them in a database, and provides tools for data analysis and visualization.

### Do I need coding experience to use this tool?
No! The tool is designed to be accessible to users with zero coding experience. The setup scripts and documentation guide you through the entire process.

## Installation & Setup

### What do I need to install before using this tool?
You'll need:
1. Python 3.8 or higher
2. Conda package manager (recommended)
3. A PostgreSQL or MySQL database
4. Power BI, Tableau, or Excel (for visualization)

### How do I install the Cryptocurrency Price Tracker?
1. Double-click `setup.bat` if you're on Windows
2. This will create a Conda environment and install all dependencies
3. Edit the `.env` file with your database credentials

### I don't have Conda installed. What should I do?
You can download and install Conda from [Anaconda's website](https://www.anaconda.com/products/distribution). We recommend using Miniconda for a lighter installation.

### I don't have a database installed. What should I do?
You have several options:
1. Install PostgreSQL from [postgresql.org](https://www.postgresql.org/download/)
2. Install MySQL from [mysql.com](https://dev.mysql.com/downloads/)
3. Use a cloud-based database service like Amazon RDS or Azure Database

### How do I set up automatic data collection?
Run the `setup_scheduler.py` script, which will configure Windows Task Scheduler to run the tracker automatically at regular intervals using your Conda environment.

## Database Questions

### Which database should I use: PostgreSQL or MySQL?
Both are excellent choices:
- PostgreSQL offers more advanced analytical functions and better handles complex queries
- MySQL is often easier to set up and may be more familiar to beginners

### How do I connect to my database?
Edit the `.env` file with your database credentials:
```
DB_TYPE="postgresql"  # or "mysql"
DB_HOST="localhost"
DB_PORT="5432"  # 5432 for PostgreSQL, 3306 for MySQL
DB_NAME="crypto_tracker"
DB_USER="your_username"
DB_PASSWORD="your_password"
```

### How much disk space will the database use?
The database size depends on how many cryptocurrencies you track and how frequently you collect data. As a rough estimate:
- Tracking 10 cryptocurrencies with hourly updates: ~5MB per month
- Tracking 50 cryptocurrencies with hourly updates: ~25MB per month

## Data Collection

### Which cryptocurrencies does the tracker monitor?
By default, it tracks Bitcoin, Ethereum, Cardano, Solana, Ripple, Polkadot, and Dogecoin. You can customize this list in the `.env` file.

### How often does it update the prices?
By default, it updates every hour. You can change this in the `.env` file by modifying the `UPDATE_INTERVAL` value (in seconds).

### Does it use a lot of internet bandwidth?
No, the API calls are very lightweight. Each update typically uses less than 100KB of data.

### Is there a limit to how often I can fetch data?
The CoinGecko API has rate limits for free users. The default settings are well within these limits, but if you set very frequent updates (e.g., every minute), you might hit these limits.

## Visualization

### How do I create dashboards with this data?
1. Run the `export_for_visualization.py` script to export the data
2. You can specify different export formats:
   - `--format powerbi`: Optimized for Power BI
   - `--format tableau`: Optimized for Tableau
   - `--format excel`: Creates multi-sheet Excel workbook
3. Open your visualization tool and import the exported data

### What kind of visualizations can I create?
You can create:
- Price charts and trends
- Market cap comparisons
- Volume analysis
- Portfolio performance tracking
- Correlation between different cryptocurrencies

### Can I customize the dashboards?
Absolutely! The exported data is designed to be flexible. You can create custom visualizations based on your preferences and analysis needs.

## Troubleshooting

### I'm getting a "Database connection error"
Check that:
1. Your database server is running
2. The credentials in your `.env` file are correct
3. The database exists (it should be created automatically, but you might need to create it manually)
4. Your firewall isn't blocking the connection

### The script runs but no data is being collected
Check that:
1. You have an internet connection
2. The CoinGecko API is accessible (sometimes it might be down temporarily)
3. The coins you're trying to track exist in the CoinGecko API

### I'm having issues with the Conda environment
Try these steps:
1. Make sure Conda is properly installed and in your PATH
2. Try creating the environment manually: `conda create -n crypto_tracker python=3.9`
3. Activate the environment: `conda activate crypto_tracker`
4. Install packages manually: `conda install --file requirements.txt`

### How do I check if the scheduler is working?
1. Open Windows Task Scheduler
2. Look for the "CryptocurrencyPriceTracker" task
3. Check its status and history

### I need more help!
If you're experiencing issues not covered here:
1. Check the logs in the `crypto_tracker.log` file
2. Look for error messages in the console output
3. Search for similar issues online, as they might be related to Python, your database, or the CoinGecko API
