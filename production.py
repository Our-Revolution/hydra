bind = '0.0.0.0:80'
pid = 'gunicorn.pid'
django_settings = 'hydra.settings'
debug = True
errorlog = 'gunicorn_error.log'
workers = 2