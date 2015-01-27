from flask import Blueprint, request, redirect, render_template, url_for, jsonify
from flask.views import MethodView

from flask.ext.mongoengine.wtf import model_form

from app.models import Product, Review, User

api = Blueprint('api', __name__, template_folder='templates')


def index():
    list = [
            {'param': 'foo', 'val': 2},
            {'param': 'bar', 'val': 10}
        ]
    return jsonify(results=list)

# Register the urls
api.add_url_rule('/api/', 'index', index)
