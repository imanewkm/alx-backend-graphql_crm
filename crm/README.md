# CRM Celery Setup

## Steps to Set Up Celery and Celery Beat

1. **Install Redis**:
   - Install Redis on your system. For example, on Ubuntu:
     ```bash
     sudo apt update
     sudo apt install redis
     ```
   - Start the Redis server:
     ```bash
     sudo service redis start
     ```

2. **Install Dependencies**:
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run Migrations**:
   - Apply migrations for `django-celery-beat`:
     ```bash
     python manage.py migrate
     ```

4. **Start Celery Worker**:
   - Start the Celery worker:
     ```bash
     celery -A crm worker -l info
     ```

5. **Start Celery Beat**:
   - Start the Celery Beat scheduler:
     ```bash
     celery -A crm beat -l info
     ```

6. **Verify Logs**:
   - Check the generated report logs in `/tmp/crm_report_log.txt`.
