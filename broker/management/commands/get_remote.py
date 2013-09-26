from django.core.management.base import BaseCommand, CommandError
from broker.models import *

from data.views import *

import json
import urllib2

class Command(BaseCommand):
    help = 'Gets data from the remotes'

    def handle(self, *args, **options):
	todo = []
	if len(args) > 0 :
		todo.append(args[0])
	else:
		todo.extend(Proxy.objects.all().values_list('id', flat=True))
	print todo
	for i in todo:
	        p = Proxy.objects.get(id=i)
		uu = p.request.url
		if uu[-1] != "/":
			uu = uu+"/"
        	url = "%sdata/%s" % (uu, p.request.token)
		print url	
		data = urllib2.urlopen(url)
	
	        dd = data.read()
        	#print dd
	        put_data(p,json.loads(dd))
