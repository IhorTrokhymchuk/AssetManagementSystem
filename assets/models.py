# assets/models.py
from django.db import models


class Asset(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    acquisition_date = models.DateField()
    location = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    maintenance_history = models.ManyToManyField('MaintenanceRecord', blank=True, related_name='assets')

    def __str__(self):
        return self.name


class MaintenanceRecord(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    responsible_person = models.CharField(max_length=255)

    def __str__(self):
        return f"Maintenance record for {self.asset.name}"
