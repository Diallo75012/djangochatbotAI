from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.utils.timezone import now
from django.contrib import messages
import subprocess
import os
from common.record_to_db import db_recorder
from common.models import LogAnalysisTask
from dotenv import load_dotenv


# Load environment variables
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path='.vars.env', override=True)

# Environment configurations
base_dir = settings.BASE_DIR
log_analyzer_folder = os.getenv("LOG_AGENT_ANALYZER_FOLDER")
log_analyzer_file = os.getenv("LOG_AGENT_GRAPH_FILE_NAME")
python_binary_env_path = os.getenv("PYTHON_BINARY_ENV_PATH")
job_output_file = os.getenv("LOG_JOB_OUTPUT_FILE")

script_path = os.path.join(base_dir, log_analyzer_folder, log_analyzer_file)
python_path = os.path.join(base_dir, python_binary_env_path)
job_output_path = os.path.join(base_dir, log_analyzer_folder, job_output_file)


# Function to check if the user is an admin
def is_admin_user(user):
    return user.is_superuser


@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_admin_user, login_url='users:loginbusinessuser')
def runLogAnalyzer(request):
    """
    Handles GET and POST requests for the log analysis dashboard.
    """
    if request.method == "POST":
        # Create an initial log entry in the database
        task = LogAnalysisTask.objects.create(user=request.user, status="Running")

        # Run the Python log analyzer script
        try:
            process = subprocess.run(
                [python_path, script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Capture stdout and stderr
            stdout = process.stdout
            stderr = process.stderr

            # Determine task status and output
            if process.returncode == 0:
                task.status = "Success"
                task.output = stdout
            else:
                task.status = "Error"
                task.output = stderr

            # Save task completion time and update the database
            task.end_time = now()
            task.save()

            # Record task details to the database
            record_query = """
                INSERT INTO common_loganalysistask (user_id, start_time, end_time, output, status)
                VALUES (%s, %s, %s, %s, %s)
            """
            db_recorder(
                record_query,
                task.user.id,
                task.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                task.end_time.strftime("%Y-%m-%d %H:%M:%S"),
                task.output or "",
                task.status
            )

        except Exception as e:
            # Handle any unexpected exceptions
            task.status = "Error"
            task.output = str(e)
            task.end_time = now()
            task.save()

            with open(job_output_path, "a", encoding="utf-8") as log_file:
                log_file.write(f"Error occurred: {e}\n")

    # Retrieve the latest 10 tasks for the dashboard
    tasks = LogAnalysisTask.objects.order_by("-start_time")[:10]

    context = {
        "tasks": tasks
    }
    return render(request, "common/log_analysis_dashboard.html", context)

