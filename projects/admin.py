from django.contrib import admin
from projects.models import Project, Solution, Feedback, Issue

# Register your models here.
admin.site.register(Project)
admin.site.register(Solution)
admin.site.register(Feedback)
admin.site.register(Issue)