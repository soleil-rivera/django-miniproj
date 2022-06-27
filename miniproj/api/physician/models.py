from django.db import models
from mpapi import models as amodels

from miniproj.constants import Validators


class Physician(amodels.AuditModel):
    first_name = models.CharField(max_length=255, validators=[Validators.alpha_only])
    middle_name = models.CharField(max_length=255, validators=[Validators.alpha_only])
    last_name = models.CharField(max_length=255, validators=[Validators.alpha_only])
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, validators=[Validators.num_only])

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Physician List"
        ordering = ["last_name"]
