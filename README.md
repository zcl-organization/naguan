# naguan

注意：数据库字符
1. pip install -q requirements.txt
2. celery work -A run_celery.celery --loglevel=info 
3. celery beat -A run_celery.celery --loglevel=info 
2. celery worker -A run_celery.celery --loglevel=info -Q vsphere
3. python manage.py runserver