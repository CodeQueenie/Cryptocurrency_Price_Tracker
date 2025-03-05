# Bitcoin Price Tracker

A user-friendly application for tracking Bitcoin prices, viewing historical data, and visualizing price trends.

## Important Notice

This project was created by Nicole LeGuern as a learning tool and portfolio piece. While it's open source under the MIT license, **any use of this code requires clear attribution to the original author**. This includes both personal and commercial applications.

## Quick Start Guide

### Installation
1. Extract the ZIP file to any location on your computer
2. Run the `install.bat` file
3. A shortcut will be created on your desktop
4. The application will launch automatically

### Using the Application

#### View Current Bitcoin Price
- Click the "View Current Bitcoin Price" button
- See the latest price, market cap, and 24-hour change

#### View Historical Data
- Click the "View Bitcoin Price History" button
- Enter the number of days to view
- See Bitcoin prices over time

#### Visualize Price Trends
- Click the "Plot Bitcoin Price History" button
- Enter the number of days to include
- View an interactive chart of Bitcoin prices

#### Export Data
- Click the "Export Bitcoin Data to Excel" button
- Choose where to save the file
- Open in Excel for further analysis

## Features

- **Real-time Bitcoin Data**: Get the latest Bitcoin prices from CoinGecko API
- **Historical Analysis**: View and analyze historical Bitcoin price data
- **Interactive Visualization**: Plot Bitcoin price trends with interactive charts
- **Data Export**: Export Bitcoin data to Excel for custom analysis
- **Automatic Updates**: Set up automatic data collection (see Advanced Features)

## Troubleshooting

### Common Issues

1. **Application won't start**
   - Make sure you extracted all files from the ZIP
   - Try running the application as administrator

2. **No data appears in the dashboard**
   - Check your internet connection
   - Verify database connection settings in the `.env` file

3. **Error connecting to database**
   - By default, the application uses a local SQLite database
   - For advanced users: check database credentials in the `.env` file

## Advanced Features

### Setting Up Automatic Data Collection

1. Open Windows Task Scheduler
2. Create a new task to run the Bitcoin Price Tracker
3. Set it to run at your preferred interval (hourly, daily, etc.)

See the `docs/TASK_SCHEDULER_SETUP.md` file for detailed instructions.

## About This Application

The Bitcoin Price Tracker is part of the larger Cryptocurrency Price Tracker project, which supports tracking multiple cryptocurrencies. This standalone application focuses specifically on Bitcoin for simplicity and ease of use.

For more information about the full Cryptocurrency Price Tracker project, visit [GitHub Repository](https://github.com/CodeQueenie/Cryptocurrency_Price_Tracker).

## For Developers

### Project Structure
The Bitcoin Tracker is a modular component of the main Cryptocurrency Price Tracker project:

- `bitcoin_dashboard_standalone.py` - Main entry point for the standalone application
- `bitcoin_data_processor.py` - Handles Bitcoin-specific data processing
- `bitcoin_visualizer.py` - Creates visualizations for Bitcoin price data

### Extending the Bitcoin Tracker
To add new features to the Bitcoin Tracker:

1. Fork the repository
2. Make your changes in the `bitcoin_tracker` directory
3. Submit a pull request

## License and Attribution

This project is licensed under the MIT License with an attribution requirement - see the [LICENSE](../LICENSE) file in the main project directory for details.

Note: This version (v1.0) is released under MIT License for demonstration and portfolio purposes. Future versions may be released under different licensing terms.

### Attribution Requirements

When using this software or substantial portions of it, you must include the following attribution:

Created by Nicole LeGuern (CodeQueenie). Original repository: [https://github.com/CodeQueenie/Cryptocurrency_Price_Tracker](https://github.com/CodeQueenie/Cryptocurrency_Price_Tracker)

This attribution may be included in:
- Documentation
- "About" section of your application
- Code comments
- Credits file that ships with your software

### Author

Nicole LeGuern (GitHub: [CodeQueenie](https://github.com/CodeQueenie))
