from django.contrib import admin
from accounts.models import Team, UserProfile

# Register your models here.
admin.site.register(Team),
admin.site.register(UserProfile)