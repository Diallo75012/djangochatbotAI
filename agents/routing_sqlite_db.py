class LogsAnalyzerRouter:
  logs_analyzer_db = "logs_analyzer"
  default_db = "default"

  def db_for_read(self, model, **hints):
    if model._meta.app_label == 'agents':
      return self.logs_analyzer_db
    return None

  def db_for_write(self, model, **hints):
    if model._meta.app_label == 'agents':
      return self.logs_analyzer_db
    return None

  def allow_migrate(self, db, app_label, model_name=None, **hints):
    print(f"allow_migrate called with db={db}, app_label={app_label}, model_name={model_name}")
    if db == 'logs_analyzer':  # Only target the SQLite database
      # Allow migrations only for the agents app
      return app_label == 'agents'
    # For the default database, allow migrations for other apps
    return db == 'default'
