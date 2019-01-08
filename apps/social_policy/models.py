from django.db import models


class ExtraRegionData(models.Model):
    region = models.CharField(max_length=1024)
    child_count = models.PositiveIntegerField(default=0)
