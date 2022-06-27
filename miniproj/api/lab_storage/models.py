from django.db import models

# from django.core.exceptions import ValidationError
from mpapi import models as amodels

from miniproj.constants import Validators
from miniproj.api.order.models import Order


class LabStorage(amodels.AuditModel):
    name = models.CharField(
        max_length=255, unique=True, validators=[Validators.alpha_num_wsc]
    )
    location = models.CharField(max_length=255)
    orders = models.ManyToManyField(
        Order, limit_choices_to={"is_deleted": False}, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Laboratory Storage List"
        ordering = ["name"]
