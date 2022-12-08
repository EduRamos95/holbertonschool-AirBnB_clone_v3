#!/usr/bin/python3
""" Method that starts a Flask web application """
import os
from models import storage
#from api.v1.views import app_views
from flask import Flask
app = Flask(__name__)

@app.teardown_appcontext
def close(self):
    """ this method logs out the database session """
    #storage.close()

if __name__ == "__main__":
    app.run(host, port)
    host = os.getenv("HBNB_API_HOST")
    port = os.getenv("HBNB_API_PORT")
    threaded=True
