# Setting Up Windows Task Scheduler

This guide will help you set up Windows Task Scheduler to automatically run the Cryptocurrency Price Tracker at regular intervals.

## Steps to Set Up Task Scheduler

1. **Open Windows Task Scheduler**
   - Press the Windows key and search for "Task Scheduler"
   - Click on "Task Scheduler" to open it

2. **Create a New Task**
   - In the right panel, click on "Create Basic Task..."
   - Enter a name (e.g., "Cryptocurrency Price Tracker") and a description
   - Click "Next"

3. **Set the Trigger**
   - Select when you want the task to start (e.g., "Daily" or "Weekly")
   - Click "Next"
   - Set the start time and recurrence pattern (e.g., every 1 hour)
   - Click "Next"

4. **Set the Action**
   - Select "Start a program" and click "Next"
   - In the "Program/script" field, browse to the location of `run_crypto_tracker.bat`
     - For example: `C:\Users\YourUsername\OneDrive\Documents\CascadeProjects\Cryptocurrency_Price_Tracker\run_crypto_tracker.bat`
   - Click "Next"
   - Note: The batch file will automatically activate the virtual environment before running the script

5. **Review and Finish**
   - Review your settings and click "Finish"

6. **Additional Settings (Optional)**
   - Right-click on your newly created task and select "Properties"
   - Go to the "Conditions" tab
     - Uncheck "Start the task only if the computer is on AC power" if you want it to run on battery
   - Go to the "Settings" tab
     - Check "Run task as soon as possible after a scheduled start is missed" to ensure it runs if the computer was off
   - Click "OK" to save these settings

## Verifying the Task

1. **Test the Task**
   - Right-click on your task in the Task Scheduler
   - Select "Run" to test if it works correctly
   - Check the `crypto_tracker.log` file to verify that data was collected

2. **View Task History**
   - Right-click on your task
   - Select "History" to see when the task has run and if there were any issues

## Troubleshooting

If your task doesn't run as expected:

1. **Check Permissions**
   - Make sure the user account running the task has permission to execute the batch file
   - Consider running the task with administrative privileges

2. **Check the Log File**
   - Open `crypto_tracker.log` to see if there are any error messages

3. **Verify Python Environment**
   - Make sure the virtual environment (`venv` folder) exists and contains all required packages
   - If needed, run `setup.bat` again to recreate the virtual environment

4. **Manual Test**
   - Double-click on `run_crypto_tracker.bat` to verify it works when run manually
   - This will activate the virtual environment and run the tracker
