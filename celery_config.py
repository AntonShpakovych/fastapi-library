from celery import Celery


app = Celery(__name__)
app.config_from_object("config", namespace="CELERY")
app.conf.imports = ("src.library.tasks",)
app.conf.broker_connection_retry_on_startup = True
