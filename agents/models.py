from django.db import models


class LogAnalyzer(models.Model):
  # this is storing the log lines
  chunk = models.CharField(blank=True)
  # this will be the log level
  log_level = models.CharField(blank=True)
  # this is the advice for the report based on the schemas type of log that we want to make an LLM report for
  # but I have decided to not store adivice but get the report made rirectly with the advice on it.
  # agent would just fetch from database what is needed
  # advice = models.CharField(blank=True)
