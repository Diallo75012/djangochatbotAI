from django.db import models
from django.contrib.auth.models import User


class LogAnalysisTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)  # Automatically set at creation
    end_time = models.DateTimeField(auto_now=True)  # Automatically update on save
    output = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("Running", "Running"), ("Success", "Success"), ("Error", "Error")]
    )
