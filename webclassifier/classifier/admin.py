from django.contrib import admin
from . import models

class WebsiteAdmin(admin.ModelAdmin):
    list_display=("url", "status", "score")

admin.site.register(models.Website, WebsiteAdmin)
admin.site.register(models.Binary)
