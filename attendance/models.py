from django.db import models
from django.db.models.fields import CharField, DateField

# Create your models here.
class Holiday(models.Model):
    name = CharField(max_length=100)
    monthanddate = DateField()
    dayoftheweek = CharField(max_length=100)