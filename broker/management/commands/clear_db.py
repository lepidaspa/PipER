from django.core.management.base import BaseCommand, CommandError
from broker.models import *

from data.views import *

import json
import urllib2
from pymongo import Connection, GEO2D

class Command(BaseCommand):
    help = 'Gets data from the remotes'

    def handle(self, *args, **options):
        connection = Connection()
        db = connection.data
        db.elements.drop()
