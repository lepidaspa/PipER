from django.db import models
    

class DataModel(models.Model):
    #type = models.CharField(max_length=50, choices=[('point', 'Point'),(''),()])
    name = models.CharField(max_length=255)
    container = models.ForeignKey('DataModel', related_name="models", blank=True, null=True)
    federated = models.BooleanField(default=False)
    within = models.ForeignKey('DataModel', related_name="contains", null=True, blank=True)
    geo_type = models.CharField(max_length=255, choices=(("Point","Punctual"),("LineString","Linear")))
    def __str__(self):
        return self.name  
    
    def to_large_json(self):
        j = {
             'name':self.name,
             'objtype': self.geo_type,
             'properties': {}
             }  
        if self.federated:
            j['federated'] = True
        if self.within is not None:
            j['within'] = self.within.id
        
        for attr in self.attributes.all():
            if attr.type in ['str', 'int', 'float','bool']:
                j['properties'][str(attr)] = attr.type
            else:
                s = attr.semantic.related_table_name.values
                if attr.semantic.filter != "":
                    s = s.filter(super__value = attr.semantic.filter)
                else: 
                    s = s.filter(super = "")
                vv = []
                for v in s:
                    vv.append(v.value)
                j['properties'][attr.name] = vv
        return j


class Infrastructure(models.Model):
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class DataModelAttribute(models.Model):
    data_model = models.ForeignKey('DataModel', related_name="attributes")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=(("int","Integer"),("str","String"),("float","Float"),("bool","Boolean"),("owner", "Owner"),("infrastructure", "Infrastructure")) )
    private = models.BooleanField(default=False)
    
    
    def __str__(self):
        return "%s%s" % ("_" if self.private else "", self.name,) 
    
    


