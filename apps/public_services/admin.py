from django.contrib import admin
from .models import PublicServiceMasterKey, PublicServiceVideo, CommonQuestion

admin.site.register(PublicServiceMasterKey)
admin.site.register(PublicServiceVideo)
admin.site.register(CommonQuestion)
