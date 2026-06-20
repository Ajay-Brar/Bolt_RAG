# RAG Question Answer System

A FastAPI-based question-answer system that uses RAG (Retrieval-Augmented Generation) to provide intelligent responses based on pre-loaded documents.

## Tech Stack

- **Backend**: FastAPI, Python 3.8+, pyPDF
- **Database**: PostgreSQL
- **Vector Store**: Pinecone
- **AI Model**: Groq (Llama)
- **Embeddings**: Sentence Transformers
- **Frontend**: HTML, CSS, JavaScript

## Prerequisites

Before setting up the project, make sure you have:

- Python 3.8 or higher
- PostgreSQL database
- Pinecone account and API key
- Groq API key

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-question-answer
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Setup

Create a `.env` file in the root directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/your_database_name

# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key

# Optional: Upload directory (if needed for future features)
UPLOAD_DIR=app/uploads
```

### 5. Database Setup

#### Create PostgreSQL Database

```sql
CREATE DATABASE your_database_name;
```

#### Run Database Migrations

```bash
# If using Alembic (recommended)
alembic upgrade head

# Or create tables manually using Python
python -c "from app.db import engine; from app.models.models import Base; Base.metadata.create_all(bind=engine)"
```

### 6. Pinecone Setup

1. Create a Pinecone account at [pinecone.io](https://pinecone.io)
2. Create a new index with:
   - **Dimensions**: 384
   - **Metric**: cosine
   - **Pod Type**: p1.x1 (or starter for free tier)

### 7. Static Files

Ensure you have the required static files:

```
static/
├── bolt-logo.png
└── bolt_fav.png
```

## Running the Application

### Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Production Deployment

#### Prerequisites
- Docker and Docker Compose installed
- SSL certificates (for HTTPS)

#### Quick Start

1. **Configure Environment**
   ```bash
   cp .env.production.template .env.production
   nano .env.production  # Fill in your API keys and passwords
   ```

2. **Setup SSL Certificates**
   ```bash
   mkdir ssl
   # Add your SSL certificates:
   # ssl/cert.pem (SSL certificate)
   # ssl/key.pem (SSL private key)
   
   # Or generate self-signed for testing:
   openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
   ```

3. **Deploy**
   ```bash
   ./deploy.sh
   ```

#### Manual Docker Commands

```bash
# Build and start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop services
docker-compose -f docker-compose.prod.yml down

# Restart services
docker-compose -f docker-compose.prod.yml restart
```

#### Production URLs
- **HTTPS**: https://localhost (with SSL)
- **HTTP**: http://localhost (redirects to HTTPS)
- **Direct API**: http://localhost:8000

The application will be available at:
- **Local**: http://localhost:8000
- **Network**: http://your-ip:8000

## API Endpoints

### Health Check
```
GET /health
```

### Test Pinecone Connection
```
GET /test-pinecone/
```

### Ask Question
```
POST /ask-question/
Content-Type: application/json

{
  "question": "Your question here"
}
```

## Project Structure

```
├── app/
│   ├── models/
│   │   └── models.py          # Database models
│   └── db.py                  # Database configuration
├── templates/
│   └── index.html             # Web interface
├── static/                    # Static files (images, CSS, JS)
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md                  # This file
```
