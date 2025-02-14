#!/bin/bash
set -e  # Exit if a command fails

chown -R creditizens:creditizens /home/creditizens/djangochatAI/chatbotAI/static
chown -R creditizens:creditizens /home/creditizens/djangochatAI/chatbotAI/media
chmod -R 755 /home/creditizens/djangochatAI/chatbotAI/static
chmod -R 755 /home/creditizens/djangochatAI/chatbotAI/media

# PostgreSQL readiness check
#echo "⏳ Waiting for PostgreSQL to be ready..."
#MAX_TRIES=5
#DB_HOST="${DATABASE_HOST:-db}"  # Default to "db" (service name in Docker Compose)
#DB_USER="${POSTGRES_USER:-creditizens}"
#DB_NAME="${POSTGRES_DB:-chatbotaidb}"
#DB_PORT="${POSTGRES_PORT:-5432}"

#for i in $(seq 1 $MAX_TRIES); do
#    if PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "SELECT 1;" >/dev/null 2>&1; then
#        echo "✅ PostgreSQL is ready!"
#        break
#    fi
#    echo "⏳ Waiting for PostgreSQL... ($i/$MAX_TRIES)"
#    sleep 2
#done

# If PostgreSQL is still not ready, exit with an error
#if ! PGPASSWORD="$POSTGRES_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -p "$DB_PORT" -c "SELECT 1;" >/dev/null 2>&1; then
#    echo "❌ PostgreSQL is still not ready after $MAX_TRIES attempts. Exiting."
#    exit 1
#fi

echo "📌 Applying Django migrations..."
/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python manage.py migrate --noinput

echo "📌 Collecting static files..."
/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python manage.py collectstatic --noinput

echo "📌 Checking if superuser exists..."
/home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username="creditizens").exists():
        print("📌 Creating superuser 'creditizens'")
        User.objects.create_superuser("creditizens", "creditizens@metaverse.com", "bonjour")
    else:
        print("✅ Superuser already exists. Skipping creation.")
except Exception as e:
    print(f"⚠️ Error creating superuser: {e}")
EOF

echo "🚀 Starting Gunicorn..."
exec /home/creditizens/djangochatAI/djangochatbotAI_venv/bin/python -m gunicorn \
    --workers=3 --log-level=debug -b 0.0.0.0:8000 \
    --timeout 300 --preload \
    --forwarded-allow-ips="*" \
    --proxy-allow-from="*" \
    chatbotAI.wsgi:application
