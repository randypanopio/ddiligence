'''
    Author: Randy Panopio
    a goofy lil flask app
'''

from flask import Flask
from flask_cors import CORS
from routes.firestore_data import firestore_data_bp
from routes.health import health_bp

flask_app = Flask(__name__)
CORS(flask_app)

flask_app.register_blueprint(firestore_data_bp)
flask_app.register_blueprint(health_bp)

if __name__ == '__main__':
    flask_app.run()
