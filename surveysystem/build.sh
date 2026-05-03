#!/bin/bash
# Render Build Script with Database Safety

echo "=== Starting Safe Build Process ==="

# Set environment variables
export PYTHONPATH="$PYTHONPATH:$PWD"

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check database safety
echo "Checking database configuration..."
python scripts/safe_deploy.py

if [ $? -ne 0 ]; then
    echo "❌ Safety checks failed!"
    exit 1
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations (Render handles this automatically)
echo "Checking migrations..."
python manage.py migrate --check

if [ $? -ne 0 ]; then
    echo "Running pending migrations..."
    python manage.py migrate
fi

# Verify database connection
echo "Verifying database connection..."
python manage.py dbshell --command "SELECT 1;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Database connection successful"
else
    echo "❌ Database connection failed"
    exit 1
fi

echo "=== Build completed successfully ==="
echo "✓ Dependencies installed"
echo "✓ Database safety verified"
echo "✓ Static files collected"
echo "✓ Migrations checked"
echo "✓ Database connection verified"

echo "🎉 Ready for deployment!"
