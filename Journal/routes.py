"""
Routes and views for the flask application.
"""
from flask import render_template, g, make_response, request, Flask, redirect, url_for, abort
from flask.json import jsonify
from flask_cors import CORS
from Journal import app

import json

CORS(app)

@app.before_request
def begin_request():
    print('Request Start')

@app.after_request
def after_request(response):
    print('Request End')
    return response

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return "This is a home page that you asked for !"
