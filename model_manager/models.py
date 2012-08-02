from django.db import models
    
class DataModelContainer(models.Model):
    
    def __str__(self):
        return str(self.id)

class DataModel(models.Model):
    #type = models.CharField(max_length=50, choices=[('point', 'Point'),(''),()])
    name = models.CharField(max_length=255)
    container = models.ForeignKey('DataModelContainer', related_name="models")
    federated = models.BooleanField(default=False)
    within = models.ForeignKey('DataModel', related_name="contains", null=True, blank=True)
    geo_type = models.CharField(max_length=255, choices=(("Point","Punctual"),("LineString","Linear")))
    def __str__(self):
        return self.name  
    
    def to_json(self):
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
                if attr.semantic.filter is not None:
                    s = s.filter(value = attr.semantic.filter)
                else: 
                    s = s.all()
                vv = []
                for v in s:
                    vv.append(v)
                j['properties'][attr.name] = vv
        return j


class DataModelAttributeTable(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name
    
class DataModelAttributeValues(models.Model):
    table = models.ForeignKey(DataModelAttributeTable, related_name="values")
    value = models.CharField(max_length = 255)
    super = models.ForeignKey('DataModelAttributeValues', related_name="children", null=True, blank=True)
    def __str__(self):
        return "%s - %s" % (self.table, self.value, )


class DataModelAttributeSemantic(models.Model):
    name = models.CharField(max_length = 255)
    filter = models.CharField(max_length = 255, null=True, blank=True)
    related_table_name = models.ForeignKey(DataModelAttributeTable, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class DataModelAttribute(models.Model):
    data_model = models.ForeignKey('DataModel', related_name="attributes")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=(("int","Integer"),("str","String"),("float","Float"),("bool","Boolean"),("list", "List")) )
    private = models.BooleanField(default=False)
    semantic = models.ForeignKey(DataModelAttributeSemantic, null=True, blank=True)
    
    
    def __str__(self):
        return "_" if self.private else "" + self.name 
    
    


