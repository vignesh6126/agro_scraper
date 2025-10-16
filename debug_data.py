"""
Debug script to check why data isn't being saved
"""

import os
import glob
import traceback

def debug_data_issue():
    print("🔧 DEBUGGING DATA SAVING ISSUE")
    print("=" * 50)
    
    # Check if directories exist
    print("📁 Checking directories:")
    directories = ['data/processed', 'data/raw', 'logs']
    for directory in directories:
        exists = os.path.exists(directory)
        print(f"   {directory}: {'✅ EXISTS' if exists else '❌ MISSING'}")
        if exists:
            files = os.listdir(directory)
            print(f"     Files: {files if files else '(empty)'}")
    
    # Check if we can write to directories
    print("\n📝 Checking write permissions:")
    for directory in ['data/processed', 'data/raw']:
        if os.path.exists(directory):
            test_file = os.path.join(directory, 'test_write.txt')
            try:
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                print(f"   {directory}: ✅ WRITABLE")
            except Exception as e:
                print(f"   {directory}: ❌ NOT WRITABLE - {e}")
    
    # Check log file for errors
    print("\n📋 Checking logs for errors:")
    log_files = glob.glob('logs/*.log')
    for log_file in log_files:
        print(f"   Log file: {log_file}")
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()[-10:]  # Last 10 lines
                for line in lines:
                    if 'ERROR' in line or 'CRITICAL' in line:
                        print(f"     ⚠️  {line.strip()}")
        except Exception as e:
            print(f"     ❌ Could not read log: {e}")

if __name__ == "__main__":
    debug_data_issue()