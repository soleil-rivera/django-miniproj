from django.db import models
from mpapi import models as amodels

from miniproj.constants import Validators
from miniproj.api.patient.models import Patient


class Sample(amodels.AuditModel):
    sample_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Sample Id",
        validators=[Validators.alpha_num_wsc],
    )
    first_name = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.sample_id

    class Meta:
        verbose_name = "Sample List"
        ordering = ["sample_id"]
