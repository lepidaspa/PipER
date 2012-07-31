from celery.task import task

from broker.models import *
from datetime import datetime
from datetime import timedelta

import crontab

@task()
def read_proxies():
    print "ciao"
    for mrt in MetadataRefreshTime.objects.all():
        if crontab.CronTab(mrt.crontab).next()<1800:
            do_refresh(mrt.metadata)