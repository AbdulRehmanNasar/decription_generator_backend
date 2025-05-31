from flask import Flask
from flask_cors import CORS
from routes.seo_routes import seo_blueprint
import os

app = Flask(__name__)

# Allow specific origins (Vercel frontend and local dev)
CORS(app, resources={r"/*": {"origins": ["https://description-generator-frontend-mu.vercel.app", "http://localhost:5173"]}})

app.register_blueprint(seo_blueprint)

if __name__ == "__main__":
    # Use Render's PORT or default to 5001 for local development
    port = int(os.getenv("PORT", 5001))
    app.run(host="0.0.0.0", port=port)