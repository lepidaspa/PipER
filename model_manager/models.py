from django.db import models
    
class DataModelContainer(models.Model):
    pass

class DataModel(models.Model):
    #type = models.CharField(max_length=50, choices=[('point', 'Point'),(''),()])
    name = models.CharField(max_length=255)
    container = models.ForeignKey(DataModelContainer, related_name="models")
    
    def __str__(self):
        return self.name    
    
class DataModelAttribute(models.model):
    data_model = models.ForeignKey(DataModel, related_name="attributes")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    
    def __str__(self):
        return "_" if self.private else "" + self.name + ": " + self.type  

