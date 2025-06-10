# Dashboard Embedding POC

A Flask-based proof-of-concept application that demonstrates how to embed dashboards from multiple BI tools (Metabase, Apache Superset, and QueryTree) in a single web interface.

## Features

- **Multi-platform Dashboard Embedding**: Supports Metabase, Apache Superset, and QueryTree
- **Secure Metabase Integration**: Uses JWT tokens for secure dashboard embedding
- **Tabbed Interface**: Clean UI with tabs to switch between different dashboard platforms
- **Environment-based Configuration**: All settings configurable via environment variables
- **Docker Support**: Fully containerized with Docker and Docker Compose support

## Architecture

The application consists of:
- **Flask Backend**: Serves the web interface and generates secure Metabase URLs
- **HTML Frontend**: Tabbed interface with embedded iframes for each dashboard platform
- **JWT Authentication**: Secure token generation for Metabase dashboard access

## Important: Service Dependencies
**This application requires external BI services to be running and accessible**:

- **Metabase** (default: http://localhost:3000)
- **Apache Superset** (default: http://localhost:8088)
- **QueryTree** (default: http://localhost:8082)

## Deployment Scenarios

### Scenario 1: All Services on Same Machine (Development)

Best for local development and testing.

```bash
# 1. Start your BI services first
# - Metabase on port 3000
# - Superset on port 8088
# - QueryTree on port 8082

# 2. Run the embedding app
python app.py
# OR with Docker
docker run --network host --env-file .env poc-embed

Scenario 2: Using Docker Compose (Recommended)

This will start Metabase along with your embedding app. You'll need to set up Superset and QueryTree separately or add them to the compose file.

```yaml
# docker-compose.yml
version: '3.8'

services:
  poc-embed:
    build: .
    ports:
      - "9999:9999"
    environment:
      - METABASE_SITE_URL=http://metabase:3000
      - METABASE_SECRET_KEY=${METABASE_SECRET_KEY}
      - METABASE_DASHBOARD_ID=${METABASE_DASHBOARD_ID}
      - SUPERSET_URL=${SUPERSET_URL}
      - QUERYTREE_URL=${QUERYTREE_URL}
    depends_on:
      - metabase
    networks:
      - dashboard-network

  metabase:
    image: metabase/metabase:latest
    ports:
      - "3000:3000"
    environment:
      - MB_DB_TYPE=h2
    volumes:
      - metabase-data:/metabase-data
    networks:
      - dashboard-network

  # Optional: Add Superset
  superset:
    image: apache/superset:latest
    ports:
      - "8088:8088"
    environment:
      - SUPERSET_SECRET_KEY=your-secret-key
    networks:
      - dashboard-network

volumes:
  metabase-data:

networks:
  dashboard-network:
    driver: bridge
```

### Scenario 3: Remote BI Services

If your BI tools are running on different servers/cloud instances:

```bash
# Set environment variables to point to remote services
export METABASE_SITE_URL=https://your-metabase.example.com
export SUPERSET_URL=https://your-superset.example.com/superset/dashboard/12/
export QUERYTREE_URL=https://your-querytree.example.com

# Run the container
docker run -p 9999:9999 \
  -e METABASE_SITE_URL=$METABASE_SITE_URL \
  -e METABASE_SECRET_KEY=$METABASE_SECRET_KEY \
  -e SUPERSET_URL=$SUPERSET_URL \
  -e QUERYTREE_URL=$QUERYTREE_URL \
  poc-embed
```

### Scenario 4: Cloud Deployment

For deploying to cloud platforms (AWS, GCP, Azure, etc.):

1. **Deploy BI services first** or use managed services
2. **Update environment variables** to point to your BI service URLs
3. **Deploy the embedding app** with proper network configuration

## Prerequisites

- Python 3.9+ (for local development)
- Docker (for containerized deployment)
- **Running instances of**:
  - Metabase (with embedding enabled and secret key configured)
  - Apache Superset (optional)
  - QueryTree (optional)

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd poc-embed
cp .env.example .env
```

### 2. Configure Environment Variables

Edit `.env` file with your actual values:

```bash
# Metabase Configuration (Required)
METABASE_SITE_URL=http://localhost:3000
METABASE_SECRET_KEY=your_actual_metabase_secret_key
METABASE_DASHBOARD_ID=2

# Superset Configuration (Optional)
SUPERSET_URL=http://localhost:8088/superset/dashboard/12/?native_filters_key=tOFPeLxWVpg&standalone=1

# QueryTree Configuration (Optional)
QUERYTREE_URL=http://localhost:8082

# Flask Configuration
PORT=9999
FLASK_DEBUG=true
```

### 3. Choose Your Deployment Method

#### Option A: Local Development
```bash
pip install -r requirements.txt
python app.py
```

#### Option B: Docker (Services on Host)
```bash
docker build -t poc-embed .
docker run --network host --env-file .env poc-embed
```

#### Option C: Docker Compose (Includes Metabase)
```bash
docker-compose up --build
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `METABASE_SITE_URL` | No | `http://localhost:3000` | Metabase instance URL |
| `METABASE_SECRET_KEY` | **Yes** | - | Metabase embedding secret key |
| `METABASE_DASHBOARD_ID` | No | `2` | Dashboard ID to embed |
| `SUPERSET_URL` | No | `http://localhost:8088/...` | Superset dashboard URL |
| `QUERYTREE_URL` | No | `http://localhost:8082` | QueryTree instance URL |
| `PORT` | No | `9999` | Flask app port |
| `FLASK_DEBUG` | No | `false` | Enable Flask debug mode |

## Setting Up BI Services

### Metabase Setup
1. Install and run Metabase
2. Enable embedding in Admin → Settings → Embedding
3. Copy the embedding secret key to your `.env` file
4. Note the dashboard ID you want to embed

### Superset Setup (Optional)
1. Install and run Apache Superset
2. Create a dashboard and note its URL
3. Enable public access or configure authentication

### QueryTree Setup (Optional)
1. Install and run QueryTree
2. Configure it to be accessible via iframe

## Accessing the Application

Once running, visit:
- **Local**: http://localhost:9999
- **Docker**: http://localhost:9999 (or your configured port)

## Troubleshooting

### Common Issues

1. **"METABASE_SECRET_KEY environment variable is required"**
   - Make sure your `.env` file contains the Metabase secret key
   - Verify the `.env` file is in the same directory as `app.py`

2. **Metabase dashboard not loading**
   - Check if Metabase is running and accessible
   - Verify the `METABASE_SITE_URL` is correct
   - Ensure the dashboard ID exists and embedding is enabled

3. **Other dashboards showing errors**
   - Verify Superset/QueryTree services are running
   - Check if the URLs in environment variables are accessible
   - Ensure CORS is properly configured on the target services

4. **Docker networking issues**
   - Use `host.docker.internal` instead of `localhost` when running in Docker
   - Consider using Docker Compose for better service communication
