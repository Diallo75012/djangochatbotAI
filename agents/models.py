from django.db import models


class LogAnalyzer(models.Model):
  chunk = models.CharField(blank=True)
  schema = models.CharField(blank=True)
  advice = models.CharField(blank=True)
