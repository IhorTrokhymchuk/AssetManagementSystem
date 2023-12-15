from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_set', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='custom_user_set', related_query_name='custom_user')

    class Meta:
        pass


class Asset(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, default='asset')
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
