# Dashboard Embedding POC

A Flask-based proof-of-concept to embed dashboards from Metabase, Superset, and QueryTree in one UI.

## Features

* Embed dashboards from Metabase (via JWT), Superset, and QueryTree
* Configurable via environment variables
* Docker + Docker Compose support

## Prerequisites

* Python 3.9+ or Docker
* Running instances of:

  * Metabase (`http://localhost:3000`)
  * Superset (`http://localhost:8088`)
  * QueryTree (`http://localhost:8082`)

## Quick Start

```bash
git clone <your-repo>
cd dashboard-embed-poc
cp .env.example .env
```

Edit `.env` with your values:

```env
METABASE_SITE_URL=http://localhost:3000
METABASE_SECRET_KEY=your_secret
METABASE_DASHBOARD_ID=2
SUPERSET_URL=http://localhost:8089/superset/dashboard/12/
QUERYTREE_URL=http://localhost:8082
PORT=9999
```

## Setup
1. Install nginx: `brew install nginx`
2. Start nginx proxy: `nginx -c $(pwd)/nginx.conf`
3. Run Flask app: `python app.py`
4. Stop nginx: `nginx -s quit`


### Run Locally

```bash
pip install -r requirements.txt
python app.py
```

### Or with Docker

```bash
docker build -t poc-embed .
docker run --network host --env-file .env poc-embed
```

### Docker Compose (with Metabase)

```bash
docker-compose up --build
```

## Access

Visit: `http://localhost:9999`
