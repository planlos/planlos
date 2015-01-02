# coding: utf-8
from flask import Blueprint


mod = Blueprint('angular', __name__,
                static_url_path="",
                static_folder='static/app')


@mod.route('/')
def index():
    return mod.send_static_file('index.html')
