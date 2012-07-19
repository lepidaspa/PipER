from django.contrib import admin
from django.db import models
DataModelContainer = models.get_model("model_manager", "DataModelContainer")
DataModel = models.get_model("model_manager", "DataModel")
DataModelAttribute = models.get_model("model_manager", "DataModelAttribute")

admin.site.register(DataModelAttribute)
admin.site.register(DataModelContainer)
admin.site.register(DataModel)
