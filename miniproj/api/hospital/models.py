from django.db import models
from mpapi import models as amodels

from miniproj.constants import Validators


class Hospital(amodels.AuditModel):
    name = models.CharField(
        max_length=255, unique=True, validators=[Validators.alpha_only]
    )
    address = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Hospital List"
        ordering = ["name"]
