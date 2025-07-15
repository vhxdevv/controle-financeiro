from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from routes import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///financas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()