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
    app.run(debug=True,host='0.0.0.0', port=5877)