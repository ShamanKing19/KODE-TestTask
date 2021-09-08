from django.db import models

class DataModel(models.Model):
    station = models.CharField(max_length=30)
    line = models.CharField(max_length=30)
    adm_area = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    status = models.CharField(max_length=30)
    id = models.CharField(max_length=30)