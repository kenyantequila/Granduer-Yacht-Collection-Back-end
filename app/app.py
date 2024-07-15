from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
from routes.yacht import yacht_blueprint


app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///granduer_yacht_collection.db'

# create database called jobs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(yacht_blueprint)


db.init_app(app)
migrate = Migrate(app=app, db=db)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)