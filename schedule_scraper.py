"""
Script to demonstrate scheduling the LinkedIn job scraper
"""

import subprocess
import sys
import os
from datetime import datetime

def run_scraper():
    """Run the LinkedIn job scraper"""
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Run the scraper script
        result = subprocess.run([
            sys.executable, 
            os.path.join(script_dir, "scraper_bot_refined.py")
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        
        # Print results
        print(f"Scraper execution completed at {datetime.now()}")
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
            
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("Scraper timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"Error running scraper: {e}")
        return False

def create_windows_task():
    """Create a Windows Task Scheduler entry (Windows only)"""
    try:
        import platform
        if platform.system() != "Windows":
            print("This function only works on Windows")
            return False
            
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "scraper_bot_refined.py")
        
        # Create a batch file to run the scraper
        batch_content = f'''@echo off
cd /d "{script_dir}"
python "{script_path}"
pause
'''
        
        batch_file = os.path.join(script_dir, "run_scraper.bat")
        with open(batch_file, "w") as f:
            f.write(batch_content)
            
        print(f"Created batch file: {batch_file}")
        print("To schedule this task:")
        print("1. Open Task Scheduler")
        print("2. Create a new task")
        print(f"3. Set the action to run: {batch_file}")
        print("4. Set your desired schedule")
        
        return True
        
    except Exception as e:
        print(f"Error creating Windows task: {e}")
        return False

if __name__ == "__main__":
    print("LinkedIn Job Scraper Scheduler")
    print("=" * 40)
    
    # Run the scraper once
    print("Running scraper...")
    success = run_scraper()
    
    if success:
        print("✅ Scraper ran successfully")
    else:
        print("❌ Scraper failed")
        
    # Show scheduling instructions
    print("\nScheduling Options:")
    print("-" * 20)
    print("Windows: Run create_windows_task() to generate a batch file")
    print("Mac/Linux: Add this line to your crontab (crontab -e):")
    print("0 9 * * * cd /path/to/web_scraper && python scraper_bot_refined.py")