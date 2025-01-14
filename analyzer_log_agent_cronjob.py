from crontab import CronTab
import os

# Path to the Python executable in the virtual environment
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PYTHON_PATH = os.path.join(PROJECT_ROOT, "venv", "bin", "python")
SCRIPT_PATH = os.path.join(PROJECT_ROOT, "log_analysis_center", "log_analyzer_graph.py")
LOG_FILE = os.path.join(PROJECT_ROOT, "log_agent_reports", "cronjob.log")

# Create a new cron job
cron = CronTab(user=True)  # Use `user=True` for the current user

# Remove existing job for the same script (if any)
for job in cron:
    if SCRIPT_PATH in job.command:
        cron.remove(job)

# Add a new cron job
job = cron.new(
    command=f"{PYTHON_PATH} {SCRIPT_PATH} >> {LOG_FILE} 2>&1",
    comment="Log analyzer cronjob"
)
job.setall("08 20 * * *")  # Schedule to run at 19:25 daily

# Save the cron job
cron.write()

print(f"Cronjob added: {job}")
