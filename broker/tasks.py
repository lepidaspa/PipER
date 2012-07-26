from broker.models import *
from celery import task


@task
def read_proxies():
    print "ciao"