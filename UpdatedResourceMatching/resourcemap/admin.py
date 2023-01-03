from django.contrib import admin

# Register your models here.
from .models import Resource,Project

admin.site.register(Resource)
admin.site.register(Project)