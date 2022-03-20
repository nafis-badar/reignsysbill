from django.contrib import admin
from home.models import UserInput

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserInput, AuthorAdmin)