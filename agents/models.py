from django.db import models


class LogAnalyzer(models.Model):
  # this is storing the log lines
  chunk = models.CharField(blank=True)
  # this will be the log level
  log_level = models.CharField(blank=True)
  # this is the advice for the report based on the schemas type of log that we want to make an LLM report for
  advice = models.CharField(blank=True)
