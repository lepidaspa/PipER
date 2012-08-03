from celery.task import task

from broker.models import *
from datetime import datetime
from datetime import timedelta

import crontab
from django.core import management

@task()
def read_proxies():
    print "ciao"
    for mrt in MetadataRefreshTime.objects.all():
        if crontab.CronTab(mrt.crontab).next()<1800:
            management.call_command('get_remote', mrt.metadata.id)