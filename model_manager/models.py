from django.db import models
    
class DataModelContainer(models.Model):
    
    def __str__(self):
        return str(self.id)

class DataModel(models.Model):
    #type = models.CharField(max_length=50, choices=[('point', 'Point'),(''),()])
    name = models.CharField(max_length=255)
    container = models.ForeignKey('DataModelContainer', related_name="models")
    geo_type = models.CharField(max_length=255, choices=(("Point","Punctual"),("LineString","Linear")))
    
    def __str__(self):
        return self.name    
    
class DataModelAttribute(models.Model):
    data_model = models.ForeignKey('DataModel', related_name="attributes")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    
    def __str__(self):
        return "_" if self.private else "" + self.name + ": " + self.type  

