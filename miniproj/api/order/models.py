from django.db import models

from miniproj.constants import OrderStatus, Validators
from miniproj.api.sample.models import Sample
from miniproj.api.hospital.models import Hospital
from miniproj.api.physician.models import Physician

# from miniproj.api.lab_storage.models import LabStorage


from mpapi import models as amodels


class Order(amodels.AuditModel):
    internal_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Internal Id",
        validators=[Validators.alpha_num_wsc],
    )
    date_sample_taken = models.DateField(null=True, verbose_name="Date Sample Taken")
    sample = models.ForeignKey(
        Sample,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_deleted": False},
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=20, default=OrderStatus.RECEIVED)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_deleted": False},
        blank=True,
        null=True,
    )
    physician = models.ForeignKey(
        Physician,
        on_delete=models.SET_NULL,
        limit_choices_to={"is_deleted": False},
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.internal_id

    class Meta:
        verbose_name = "Order List"
        ordering = ["internal_id"]
