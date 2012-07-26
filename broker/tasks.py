from celery.task import task

from broker.models import *



@task()
def read_proxies():
    print "ciao"