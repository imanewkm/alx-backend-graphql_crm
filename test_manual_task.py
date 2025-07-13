#!/usr/bin/env python
"""
Manual test script for the CRM report generation task
Run this after setting up the full environment to test the task manually
"""
import os
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

def test_task_execution():
    """Test the CRM report generation task manually"""
    try:
        from crm.tasks import generate_crm_report
        
        print("🚀 Testing CRM report generation task...")
        print(f"Timestamp: {datetime.now()}")
        print("-" * 50)
        
        # Execute the task synchronously for testing
        result = generate_crm_report()
        
        print("Task execution result:")
        print(result)
        
        # Try to read the log file
        try:
            with open("/tmp/crm_report_log.txt", "r") as f:
                log_content = f.read()
                print("\nCurrent log content:")
                print(log_content)
        except FileNotFoundError:
            print("\n⚠️  Log file not found at /tmp/crm_report_log.txt")
        except Exception as e:
            print(f"\n❌ Error reading log file: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Task execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_async_task():
    """Test the task execution with Celery (requires worker to be running)"""
    try:
        from crm.tasks import generate_crm_report
        
        print("\n🔄 Testing async task execution...")
        print("Note: This requires a Celery worker to be running!")
        
        # Execute the task asynchronously
        result = generate_crm_report.delay()
        
        print(f"Task ID: {result.id}")
        print(f"Task State: {result.state}")
        
        # Wait for result (with timeout)
        try:
            task_result = result.get(timeout=30)
            print(f"Task Result: {task_result}")
            return True
        except Exception as e:
            print(f"❌ Failed to get task result: {e}")
            print("Make sure Celery worker is running: celery -A crm worker -l info")
            return False
            
    except Exception as e:
        print(f"❌ Async task test failed: {e}")
        return False

def main():
    print("🧪 Manual CRM Task Testing")
    print("=" * 60)
    
    # First test direct execution
    direct_success = test_task_execution()
    
    if direct_success:
        print("\n" + "=" * 60)
        # Then test async execution
        test_async_task()
    
    print("\n" + "=" * 60)
    print("Testing complete!")

if __name__ == "__main__":
    main()
