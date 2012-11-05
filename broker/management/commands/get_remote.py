from django.core.management.base import BaseCommand, CommandError
from broker.models import *

from data.views import *

import json
import urllib2

class Command(BaseCommand):
    help = 'Gets data from the remotes'

    def handle(self, *args, **options):
        p = Proxy.objects.get(id=args[0])
        url = "%sdata/%s" % (p.request.url, p.request.token)
	print url	
	data = urllib2.urlopen(url)
	
        dd = data.read()
        #print dd
        put_data(p,json.loads(dd))
