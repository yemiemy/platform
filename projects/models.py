from django.db import models
from accounts.models import Team

# Create your models here.
class Solution(models.Model):
    details = models.TextField()
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.details

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    attachment = models.FileField(upload_to='attachments/%Y/%m/%d/', null=True, blank=True)
    point = models.IntegerField(null=True)
    startdate = models.DateTimeField(null=True)
    deadline = models.DateTimeField(blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='project')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, null=True, related_name='project')
    is_assigned = models.BooleanField(default=False, null=True)
    is_submitted = models.BooleanField(default=False, null=True)
    is_accepted = models.BooleanField(default=False, null=True)
    def __str__(self):
        return self.title

class Issue(models.Model):
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    title = models.CharField(max_length=225, null=True)
    message = models.TextField()
    post_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    team = models.ForeignKey(Team, related_name='feedbacks', on_delete=models.CASCADE)
    title = models.CharField(max_length=225, null=True)
    message = models.TextField()
    post_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title