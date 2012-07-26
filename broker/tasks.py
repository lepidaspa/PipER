from celery import task


from broker.models import *

@task()
def read_proxies():
    pass