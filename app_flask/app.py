from flask import Flask
from flask_cors import CORS
from routes.firestore_data import firestore_data_bp

flask_app = Flask(__name__)
CORS(flask_app)

flask_app.register_blueprint(firestore_data_bp)

if __name__ == '__main__':
    flask_app.run()
