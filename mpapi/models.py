from django.db import models


class AuditModel(models.Model):
    created = models.DateField(auto_now_add=True, null=True)
    last_updated = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# Create your models here.
