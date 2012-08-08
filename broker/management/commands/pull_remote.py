from django.core.management.base import BaseCommand, CommandError
from broker.models import *

from data.views import *

import json
import urllib2

class Command(BaseCommand):
    help = 'Gets data from the remotes'

    def handle(self, *args, **options):
        p = Proxy.objects.get(id=args[0])
        url = p.request.url
        if url[-1] != "/":
            url += "/"
        data = urllib2.urlopen("%srefreshremote/%s" % (url, p.request.token))
        dd = data.read()
        print dd
        put_data(json.loads(dd))
