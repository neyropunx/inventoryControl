from flask import Flask
from flask_sqlalchemy import SQLAlchemy

connection_string = "mysql+pymysql://admin:adminpass@localhost/warehouse"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)