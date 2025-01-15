from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
import subprocess
import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from dotenv import load_dotenv
# load env vars
load_dotenv(dotenv_path='.env', override=False)
load_dotenv(dotenv_path=".vars.env", override=True)



# function for decorator check if user is in the `admin` group of users
# `is_superuser` is a flag and `is_staff` as well and don't need import to check
# if needed a group. this need to be created by admin in webUI or programmatically
def is_admin_user(user):
  return user.is_superuser

# send user to business user login as admin is also a business user
'''
  Maybe here could create a `users:loginadminuser` new path and view function just for admin tasks.
  Need also to create proper html page rendered for admin to see what is going on or just the result
  Need also to create a database table using models.py but after using just `psycopg3` connection to write
  to bd the outcome of the AI agent launch, who started it, when.
  And when Devops/Security team login they would see the latest rows (a certain number of row only) of past reports.
  So can just login, launch it and come back later, or just check the Discord to see report files from Agent.
'''
# get root project folder path
base_dir = setting.BASE_DIR
log_agent_graph_file_name = os.getenv("LOG_AGENT_GRAPH_FILE_NAME")
log_analysis_center = os.getnev("LOG_ANALYSIS_CENTER")
python_binary_env_path = os.getnev("PYTHON_BINARY_ENV_PATH")
log_analyzer_folder = os.getenv("LOG_AGENT_ANALYZER_FOLDER")
log_job_output_file = os.getenv("LOG_JOB_OUTPUT_FILE")
job_output_write_file = os.path.join(base_dir, log_analyzer_folder, log_job_output_file)

@login_required(login_url='users:loginbusinessuser')
@user_passes_test(is_admin_user, login_url='users:loginbusinessuser')
def runLogAnalyzer(request):
    try:
        # Set the path to your Python script
        script_path = os.path.join(
            os.path.dirname(
                base_dir, 
                log_analyzer_folder,
                log_agent_graph_file_name
            )

        # path of python binary in python virt env
        python_binary = os.path.join(base_dir, python_binary_env_path)

        # Run the Python script using subprocess
        process = subprocess.run(
            [python_binary, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Capture output and errors
        stdout = process.stdout
        stderr = process.stderr

        if process.returncode == 0:
            # write to the job output file the stdout
            with open(job_output_write_file, "a", encoding="utf-8") as job_output_file:
                job_output_file.write(f"Success stdout: {stdout}")
            return JsonResponse({"status": "success", "stdout": stdout})
        else:
            with open(job_output_write_file, "a", encoding="utf-8") as job_output_file:
                job_output_file.write(f"Error stderr: {stderr}")
            return JsonResponse({"status": "error", "stderr": stderr})

    except Exception as e:
        with open(job_output_write_file, "a", encoding="utf-8") as job_output_file:
            job_output_file.write(f"Exception stderr: {stderr}")
        return JsonResponse({"status": "error", "message": str(e)})

