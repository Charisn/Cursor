#!/bin/bash

# Staydesk NLP Service Startup Script

set -e

echo "🏨 Starting Staydesk NLP Service..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.13 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check environment variables
echo "🔧 Checking configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Please copy env.example to .env and configure it."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "✅ Created .env from env.example template"
        echo "🔧 Please edit .env file with your configuration before running the service"
        exit 1
    fi
fi

# Run health check
echo "🩺 Running health check..."
python cli_test.py health || {
    echo "❌ Health check failed. Please check your configuration."
    exit 1
}

echo "✅ Health check passed!"

# Start the service
echo "🚀 Starting NLP service on port 8001..."
echo "📖 API documentation will be available at: http://localhost:8001/docs"
echo "🔍 Service status at: http://localhost:8001/"

uvicorn main:app --host 0.0.0.0 --port 8001 --reload 