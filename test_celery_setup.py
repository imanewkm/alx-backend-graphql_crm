#!/usr/bin/env python
"""
Test script to verify Celery setup for CRM project
"""
import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql_crm.settings')
django.setup()

def test_celery_import():
    """Test if Celery can be imported and configured"""
    try:
        from crm.celery import app
        print("✅ Celery app imported successfully")
        print(f"   Broker URL: {app.conf.broker_url}")
        return True
    except Exception as e:
        print(f"❌ Failed to import Celery app: {e}")
        return False

def test_task_import():
    """Test if the CRM task can be imported"""
    try:
        from crm.tasks import generate_crm_report
        print("✅ CRM task imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import CRM task: {e}")
        return False

def test_models():
    """Test if models can be imported and accessed"""
    try:
        from crm.models import Customer, Product, Order
        customer_count = Customer.objects.count()
        product_count = Product.objects.count()
        order_count = Order.objects.count()
        
        print("✅ Models imported and accessible")
        print(f"   Customers: {customer_count}")
        print(f"   Products: {product_count}")
        print(f"   Orders: {order_count}")
        return True
    except Exception as e:
        print(f"❌ Failed to access models: {e}")
        return False

def test_schema():
    """Test if GraphQL schema can be imported"""
    try:
        from crm.schema import Query, Mutation
        print("✅ GraphQL schema imported successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to import GraphQL schema: {e}")
        return False

def main():
    print("🧪 Testing CRM Celery Setup")
    print("=" * 50)
    
    tests = [
        test_celery_import,
        test_task_import,
        test_models,
        test_schema
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Setup looks good.")
        print("\nNext steps:")
        print("1. Install and start Redis: redis-server")
        print("2. Run migrations: python manage.py migrate")
        print("3. Start Django: python manage.py runserver")
        print("4. Start Celery worker: celery -A crm worker -l info")
        print("5. Start Celery beat: celery -A crm beat -l info")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")

if __name__ == "__main__":
    main()
