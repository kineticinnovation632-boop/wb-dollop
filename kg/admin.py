from django.contrib import admin
from .models import Developers, Site

# Register your models here.
@admin.register(Developers)
class DevelopersAdmin(admin.ModelAdmin):
    list_display = ('name', 'remark', )

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('developer', 'name', 'address',)