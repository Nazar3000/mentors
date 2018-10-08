from django.contrib import admin
from .models import SocialServiceMasterKey, SocialServiceVideo, Material, MaterialCategory

admin.site.register(SocialServiceMasterKey)
admin.site.register(SocialServiceVideo)
admin.site.register(Material)
admin.site.register(MaterialCategory)