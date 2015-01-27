from flask import Flask
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {"DB": "localhost:27017"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)


def register_blueprints(app):
    # Prevents circular imports
    from app.views import products
    from app.admin import admin
    from app.api import api
    app.register_blueprint(products)
    app.register_blueprint(admin)
    app.register_blueprint(api)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
