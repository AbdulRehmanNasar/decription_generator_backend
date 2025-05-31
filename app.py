from flask import Flask
from flask_cors import CORS
from routes.seo_routes import seo_blueprint

app = Flask(__name__)

# Allow specific origin (React dev server at port 5173)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

app.register_blueprint(seo_blueprint)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
