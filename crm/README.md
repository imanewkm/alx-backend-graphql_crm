# CRM Celery Configuration

This document provides setup instructions for configuring Celery with Celery Beat to generate weekly CRM reports using GraphQL.

## Prerequisites

- Python 3.8+
- Redis server
- Django project setup

## Installation Steps

### 1. Install Redis

**On Windows:**
```bash
# Download and install Redis from https://github.com/microsoftarchive/redis/releases
# Or use Windows Subsystem for Linux (WSL) with Ubuntu and run:
sudo apt update
sudo apt install redis-server
```

**On macOS:**
```bash
brew install redis
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- celery==5.3.4
- django-celery-beat==2.5.0
- redis==5.0.1
- gql[requests]==3.4.1

### 3. Configure Database

Run Django migrations to set up the database:

```bash
python manage.py migrate
python manage.py migrate django_celery_beat
```

### 4. Start Redis Server

**On Windows/WSL:**
```bash
redis-server
```

**On macOS/Linux:**
```bash
sudo systemctl start redis-server
# or
redis-server
```

Verify Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

### 5. Start Django Development Server

```bash
python manage.py runserver
```

The GraphQL endpoint will be available at: `http://localhost:8000/graphql`

### 6. Start Celery Worker

Open a new terminal and run:

```bash
celery -A crm worker -l info
```

This starts the Celery worker that will execute the tasks.

### 7. Start Celery Beat

Open another terminal and run:

```bash
celery -A crm beat -l info
```

This starts the Celery Beat scheduler that will trigger tasks according to the schedule.

## Task Configuration

The CRM report generation task is configured to run every Monday at 6:00 AM UTC:

```python
CELERY_BEAT_SCHEDULE = {
    'generate-crm-report': {
        'task': 'crm.tasks.generate_crm_report',
        'schedule': crontab(day_of_week='mon', hour=6, minute=0),
    },
}
```

## Manual Task Execution

To manually trigger the report generation task:

```bash
# Using Django shell
python manage.py shell

# In the shell:
from crm.tasks import generate_crm_report
result = generate_crm_report.delay()
print(result.get())
```

Or using Celery command:

```bash
celery -A crm call crm.tasks.generate_crm_report
```

## Verify Setup

### 1. Check Celery Beat Schedule

```bash
celery -A crm beat -l info
```

You should see log entries indicating the scheduled task.

### 2. Check Report Logs

The weekly reports are logged to `/tmp/crm_report_log.txt`:

```bash
# On Windows/WSL
type /tmp/crm_report_log.txt

# On macOS/Linux
cat /tmp/crm_report_log.txt
```

Example log entry:
```
2025-07-13 10:30:00 - Report: 15 customers, 32 orders, 1523.50 revenue
```

### 3. Test GraphQL Endpoint

Visit `http://localhost:8000/graphql` and run this query:

```graphql
query {
  customers {
    id
    name
    email
  }
  orders {
    id
    totalAmount
    customer {
      name
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Redis Connection Error:**
   - Ensure Redis server is running
   - Check Redis connection: `redis-cli ping`

2. **Task Not Executing:**
   - Verify Celery worker is running
   - Check Celery Beat scheduler is running
   - Review logs for errors

3. **GraphQL Errors:**
   - Ensure Django server is running
   - Check database migrations are applied
   - Verify GraphQL schema is properly configured

### Log Files

- Celery Worker logs: Console output where worker is running
- Celery Beat logs: Console output where beat is running
- CRM Reports: `/tmp/crm_report_log.txt`
- Low Stock Updates: `/tmp/low_stock_updates_log.txt`

## Development Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Seed database with sample data
python seed_db.py

# Run tests
python manage.py test

# Check Celery worker status
celery -A crm inspect active

# Purge all tasks
celery -A crm purge
```

## Production Considerations

1. Use a process manager like Supervisor or systemd for Celery processes
2. Configure proper logging and monitoring
3. Use a robust Redis configuration
4. Set up proper error handling and alerting
5. Consider using Celery Flower for monitoring: `pip install flower && celery -A crm flower`

