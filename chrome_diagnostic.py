import subprocess
import sys
import os

def check_chrome_installation():
    """Check if Chrome is properly installed and accessible"""
    print("🔍 Checking Chrome installation...")
    
    # Common Chrome paths on Windows
    chrome_paths = [
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe")
    ]
    
    chrome_path = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_path = path
            break
    
    if chrome_path:
        print(f"✅ Chrome found at: {chrome_path}")
        # Test if Chrome can be launched
        try:
            result = subprocess.run([chrome_path, "--version"], capture_output=True, text=True, timeout=10)
            print(f"✅ Chrome version: {result.stdout.strip()}")
            return True
        except Exception as e:
            print(f"❌ Error checking Chrome version: {e}")
            return False
    else:
        print("❌ Chrome not found in common installation paths")
        return False

def check_system_info():
    """Check system information"""
    print("\n🖥️  System Information:")
    print(f"Platform: {sys.platform}")
    print(f"Python version: {sys.version}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not running in virtual environment")

def main():
    print("🔧 Chrome and Selenium Diagnostic Tool")
    print("=" * 50)
    
    check_system_info()
    chrome_ok = check_chrome_installation()
    
    if not chrome_ok:
        print("\n💡 Recommendations:")
        print("1. Make sure Google Chrome is installed on your system")
        print("2. If Chrome is installed in a non-standard location, add it to your PATH")
        print("3. Try reinstalling Google Chrome")
        print("4. Check if your antivirus is blocking Chrome execution")
    
    print("\n✅ Diagnostic completed")

if __name__ == "__main__":
    main()