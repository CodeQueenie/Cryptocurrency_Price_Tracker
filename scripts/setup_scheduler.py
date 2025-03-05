"""
Setup Scheduler for Cryptocurrency Price Tracker
-----------------------------------------------
This script helps users set up automated data collection using Windows Task Scheduler.
It configures the scheduler to run the crypto tracker at regular intervals.
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_windows_task_scheduler():
    """
    Set up Windows Task Scheduler to run the crypto tracker automatically.
    
    Creates a scheduled task that runs the crypto_tracker.py script every hour
    using the conda environment.
    
    Returns:
        bool: True if the task was created successfully, False otherwise.
        
    Raises:
        subprocess.CalledProcessError: If there's an error creating the task.
    """
    try:
        print("Setting up Windows Task Scheduler for automated data collection...")
        
        # Get the current directory and script paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        conda_path = os.path.join(os.environ.get("CONDA_PREFIX", ""), "..\\..\\Scripts\\conda.exe")
        script_path = os.path.join(current_dir, "crypto_tracker.py")
        
        # Create the task name
        task_name = "CryptocurrencyPriceTracker"
        
        # Build the command to create a scheduled task
        # This will run the script every hour using the conda environment
        cmd_to_run = f'cmd.exe /c "call conda activate crypto_tracker && python "{script_path}""'
        
        cmd = [
            "schtasks", "/create", "/tn", task_name, "/tr", 
            cmd_to_run, 
            "/sc", "hourly", 
            "/mo", "1",  # Run every 1 hour
            "/st", "00:00",  # Start time
            "/ru", "SYSTEM",  # Run with system privileges
            "/f"  # Force creation (overwrite if exists)
        ]
        
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"✅ Successfully created scheduled task '{task_name}'")
        print(f"   The script will run every hour to collect cryptocurrency data")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create scheduled task: {e}")
        print("   You may need to run this script as administrator")
        return False
    except Exception as e:
        print(f"❌ Unexpected error setting up scheduler: {e}")
        return False

def main():
    """
    Main function to set up the scheduler.
    
    Guides the user through setting up automated data collection
    using the appropriate scheduler for their operating system.
    
    Returns:
        None
    """
    try:
        print("=" * 50)
        print("Cryptocurrency Price Tracker - Scheduler Setup")
        print("=" * 50)
        print("\nThis script will set up automated data collection for the Cryptocurrency Price Tracker.")
        
        # Check if running on Windows
        if sys.platform != "win32":
            print("❌ This script is designed for Windows only.")
            print("   For Linux/Mac, please set up a cron job manually:")
            print("   Example: crontab -e")
            print("   Then add: 0 * * * * conda activate crypto_tracker && python /path/to/crypto_tracker.py")
            return
        
        # Check if conda environment exists
        try:
            result = subprocess.run(
                ["conda", "env", "list"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            if "crypto_tracker" not in result.stdout:
                print("❌ Conda environment 'crypto_tracker' not found.")
                print("   Please run setup.bat first to create the environment.")
                return
        except subprocess.CalledProcessError:
            print("❌ Could not verify conda environment.")
            print("   Please make sure conda is installed and in your PATH.")
            return
        
        # Confirm with the user
        choice = input("\nDo you want to set up automatic hourly data collection? (y/n): ").lower()
        if choice != "y":
            print("Setup cancelled.")
            return
        
        # Set up the scheduler
        success = setup_windows_task_scheduler()
        
        if success:
            print("\nSetup complete! The Cryptocurrency Price Tracker will now run automatically.")
            print("You can view or modify this task in Windows Task Scheduler.")
        else:
            print("\nSetup failed. Please try running this script as administrator.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
