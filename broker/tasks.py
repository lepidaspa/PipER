from celery.task import task

from broker.models import *
from datetime import datetime
from datetime import timedelta


@task()
def read_proxies():
    for mrt in MetadataRefreshTime.objects.filter(due>datetime.now(), due < datetime.now()+timedelta(minutes=30)):
        print "ciao"