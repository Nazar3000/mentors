from django.db import models


class ExtraRegionData(models.Model):
    region = models.CharField(max_length=1024)
    child_count = models.PositiveIntegerField(default=0)


class SPMaterialCategory(models.Model):
    title = models.CharField(max_length=256)
    icon = models.ImageField(upload_to='icons', blank=True, null=True)

    class Meta:
        verbose_name = "Material category"
        verbose_name_plural = "Material categories"

    def __str__(self):
        return "{}".format(self.title)


class SPMaterial(models.Model):
    title = models.CharField(max_length=256)
    file = models.FileField(blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(SPMaterialCategory, blank=True, null=True, on_delete=models.SET_NULL)
