# naguan

1. pip install -q requirements.txt
2. celery worker -A run_celery.celery --loglevel=info -Q vsphere
3. python manage.py runserver