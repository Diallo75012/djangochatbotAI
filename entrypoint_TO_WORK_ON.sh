#!/bin/bash
set -e  # Exit if a command fails

echo "📌 Applying Django migrations..."
/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python manage.py migrate --noinput

echo "📌 Collecting static files..."
/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python manage.py collectstatic --noinput

echo "📌 Checking if superuser exists..."
/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    print("📌 Creating superuser 'admin'")
    User.objects.create_superuser("admin", "admin@example.com", "adminpassword")
else:
    print("✅ Superuser already exists. Skipping creation.")
EOF

echo "🚀 Starting Gunicorn..."
exec /home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python -m gunicorn \
    --workers=3 --log-level=debug -b 0.0.0.0:8000 \
    --timeout 300 --preload \
    --forwarded-allow-ips="*" \
    --proxy-allow-from="*" \
    chatbotAI.wsgi:application
