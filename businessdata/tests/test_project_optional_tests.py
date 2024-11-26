import subprocess
from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application

def test_wsgi_application():
  try:
    application = get_wsgi_application()
  except Exception as e:
    pytest.fail(f"WSGI application failed to load: {str(e)}")

def test_asgi_application():
  try:
    application = get_asgi_application()
  except Exception as e:
    pytest.fail(f"ASGI application failed to load: {str(e)}")

def test_manage_script():
  try:
    result = subprocess.run(['python', 'manage.py', '--help'], check=True)
    assert result.returncode == 0
  except subprocess.CalledProcessError as e:
    pytest.fail(f"manage.py script failed: {str(e)}")
