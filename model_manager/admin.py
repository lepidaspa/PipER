from django.contrib import admin
from django.db import models

from model_manager.models import *

admin.site.register(DataModelAttribute)
admin.site.register(DataModelContainer)
admin.site.register(DataModel)
