import jwt
import time
import os
from flask import Flask, render_template, jsonify
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
METABASE_SITE_URL = os.getenv('METABASE_SITE_URL', "http://localhost:3000")
METABASE_SECRET_KEY = os.getenv('METABASE_SECRET_KEY')
METABASE_DASHBOARD_ID = int(os.getenv('METABASE_DASHBOARD_ID', '2'))

# Validate required environment variables
if not METABASE_SECRET_KEY:
    raise ValueError("METABASE_SECRET_KEY environment variable is required")

# Initialize the Flask app
app = Flask(__name__)


# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html',
                         superset_url=os.getenv('SUPERSET_URL', 'http://localhost:8088/superset/dashboard/12/?native_filters_key=tOFPeLxWVpg&standalone=1'),
                         querytree_url=os.getenv('QUERYTREE_URL', 'http://localhost:8082'))


@app.route('/get-metabase-url')
def get_metabase_url():
    """Generates the signed URL for the Metabase dashboard embed."""
    payload = {
        "resource": {"dashboard": METABASE_DASHBOARD_ID},
        "params": {},
        "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
    }

    token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

    # in Python 3, jwt.encode returns bytes. decode it to a string.
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    iframeUrl = f"{METABASE_SITE_URL}/embed/dashboard/{token}#bordered=true&titled=true"

    return jsonify({"url": iframeUrl})


# --- Run the App ---

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '9999')), debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')
