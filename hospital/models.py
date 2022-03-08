from django.db import models
from mpapi import models as amodels


class Hospital(amodels.AuditModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hospital List"
        ordering = ["name"]


# Create your models here.
