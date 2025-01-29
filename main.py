from flask_cors import CORS
from utils.app import *
from dotenv import load_dotenv
from routes import *

# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()

@app.route('/api/')
def homepage():
    return "Welcome to Icicle Edge to Cloud"

if __name__ == '__main__':
    env = os.getenv("ENV", "dev")
    port = int(os.getenv("PORT", 5877 if env == "dev" else 5000))
    app.run(debug=(env == "dev"), host='0.0.0.0', port=port)