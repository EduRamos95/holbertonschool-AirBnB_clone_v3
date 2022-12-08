#!/usr/bin/python3
""" Method that starts a Flask web application """
from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)


@app.teardown_appcontext
def close(self):
    """ this method logs out the database session """
    storage.close()


if __name__ == "__main__":
    app.run(
            host=os.getenv("HBNB_API_HOST", '0.0.0.0'),
            port=os.getenv("HBNB_API_PORT", 5000),
            threaded=True
           )
