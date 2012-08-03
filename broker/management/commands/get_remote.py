from django.core.management.base import BaseCommand, CommandError
from broker.models import *

import json
import urllib2

class Command(BaseCommand):
    help = 'Gets data from the remotes'

    def handle(self, *args, **options):
        p = Proxy.objects.get(id=args[0])
        data = urllib2.urlopen("%sdata/%s" % (p.request.url, p.request.token))
