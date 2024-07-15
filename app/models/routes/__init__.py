from flask import Flask  
from flask_sqlalchemy import SQLAlchemy  

app = Flask(__name__)  
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///granduer_yacht_collection.db"  
db = SQLAlchemy(app)  