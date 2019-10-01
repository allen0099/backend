from flask import Flask, redirect, make_response, jsonify
from flask_cors import CORS

from blueprints.api import api as bp_api
from blueprints.login import login as bp_login, login_manager
from database import db


def create_app(config_file=None) -> Flask:
    app = Flask(__name__)

    # disable sorting the jsonify data
    app.config['JSON_SORT_KEYS'] = False

    if config_file is None:
        # testing mode, should not use in production environment
        app.secret_key = b'(ML\x90\x13\xcd\xaev\xa0 \x1d\x1fC\xab\xb7\x05'

        # database connect pre define, must as first as possible
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:meowmeow@127.0.0.1:32769/testdb'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        db.init_app(app)
        login_manager.init_app(app)

    elif config_file == "testing":
        app.testing = True
        app.secret_key = b'testingString'

        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:meowmeow@127.0.0.1:32769/testing'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # import blueprints to flask
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_login)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def root():
        return redirect("/api")

    @app.errorhandler(401)
    def unauthorized(error):
        return make_response(jsonify({
            "error": "Unauthorized",
            "reason": error.get_description()[3:-4]
        }), 401)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({
            "error": "Not found",
            "reason": error.get_description()[3:-4]
        }), 404)

    @app.errorhandler(500)
    def internal_server_error(error):
        return make_response(jsonify({
            "error": "Internal Server Error",
            "reason": error.get_description()[3:-4]
        }), 500)

    return app
