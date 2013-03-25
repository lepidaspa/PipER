from django.core.management.base import BaseCommand, CommandError
from broker.models import *

from data.views import *

import json
import urllib2

class Command(BaseCommand):
    help = 'Gets data from the remotes'

    def handle(self, *args, **options):
	todo = []
	if len(args) > 0:
		todo.append(args[0])
	else:
		todo.extend(Proxy.objects.all().values_list('id', flat=True))
	for i in  todo:
	        p = Proxy.objects.get(id=i)
        	url = p.request.url
	        if url[-1] != "/":
        	    url += "/"
	        tot = "%srefreshremote/%s/" % (url, p.request.token)
        	print tot
	        data = urllib2.urlopen(tot)
        	dd = data.read()
	        print  dd
