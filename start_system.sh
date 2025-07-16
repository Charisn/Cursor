#!/bin/bash

# Staydesk Complete System Startup Script

set -e

echo "🏨 Starting Staydesk Complete System"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose is not installed. Please install docker-compose.${NC}"
    exit 1
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p backend/api/database
mkdir -p backend/api/logs
mkdir -p backend/nlp/logs
mkdir -p backend/nlp/credentials
mkdir -p email-tests

# Create default environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚙️  Creating default .env file...${NC}"
    cat > .env << EOF
# Google Cloud Configuration (required for NLP)
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
VERTEX_AI_LOCATION=us-central1

# Email Configuration
IMAP_USERNAME=
IMAP_PASSWORD=

# NLP Configuration
CONFIDENCE_THRESHOLD=0.85
MAX_PROCESSING_TIME=300
GEMINI_MODEL=gemini-2.0-flash-exp

# API Configuration
API_TIMEOUT=30
LOG_LEVEL=INFO
LOG_FORMAT=json
EOF
    
    echo -e "${YELLOW}⚠️  Please edit .env file with your Google Cloud credentials before running NLP service.${NC}"
fi

# Build and start services
echo -e "${BLUE}🔨 Building Docker images...${NC}"
docker-compose build

echo -e "${BLUE}🚀 Starting services...${NC}"
docker-compose up -d

# Wait for services to start
echo -e "${BLUE}⏳ Waiting for services to initialize...${NC}"
sleep 10

# Check service health
echo -e "${BLUE}🩺 Checking service health...${NC}"

# Check MailHog
if curl -f http://localhost:8025 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ MailHog is running${NC}"
else
    echo -e "${RED}❌ MailHog is not responding${NC}"
fi

# Check API
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend API is running${NC}"
else
    echo -e "${RED}❌ Backend API is not responding${NC}"
fi

# Check NLP (might fail if no credentials)
if curl -f http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ NLP Service is running${NC}"
else
    echo -e "${YELLOW}⚠️  NLP Service may need Google Cloud credentials${NC}"
fi

echo
echo -e "${GREEN}🎉 Staydesk System Started Successfully!${NC}"
echo
echo -e "${BLUE}📋 Service URLs:${NC}"
echo "🔗 Backend API: http://localhost:8000"
echo "🔗 API Documentation: http://localhost:8000/docs"
echo "🔗 NLP Service: http://localhost:8001"
echo "🔗 NLP Documentation: http://localhost:8001/docs"
echo "🔗 MailHog Web UI: http://localhost:8025"
echo
echo -e "${BLUE}🧪 Testing:${NC}"
echo "📧 Send test emails: python email-tests/send_test_emails.py"
echo "🔍 Test API: curl http://localhost:8000/api/rooms/context"
echo "🧠 Test NLP: curl -X POST http://localhost:8001/process-email -H 'Content-Type: application/json' -d '{\"subject\":\"Room availability\",\"body\":\"I need 1 room for tomorrow\",\"sender\":\"test@example.com\"}'"
echo
echo -e "${BLUE}📊 Monitoring:${NC}"
echo "📈 View logs: docker-compose logs -f [service-name]"
echo "🔄 Restart service: docker-compose restart [service-name]"
echo "⏹️  Stop system: docker-compose down"
echo
echo -e "${YELLOW}💡 Next Steps:${NC}"
echo "1. Configure Google Cloud credentials in backend/nlp/credentials/"
echo "2. Send test emails using: python email-tests/send_test_emails.py"
echo "3. Monitor email processing in MailHog UI"
echo "4. Check API responses and NLP processing results"
echo
echo -e "${GREEN}🏨 Happy testing with Staydesk! 🎊${NC}" 