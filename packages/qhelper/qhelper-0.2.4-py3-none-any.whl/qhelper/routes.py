from flask import render_template
from .dash.app import create_dash_app
from .auth import init_auth
from .error import init_error
from .setting import init_setting
from .scheduler import init_scheduler

def init_routes(app):
    init_auth(app)
    init_error(app)
    scheduler = init_scheduler(app)
    init_setting(app, scheduler)
    create_dash_app(app)
    @app.route('/')
    def index():
        return render_template('index.html')