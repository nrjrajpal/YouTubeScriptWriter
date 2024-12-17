from APIs.temp_api import temp_blueprint, sign_up_2_blueprint

def api_blueprints(app):
    # Register blueprints
    app.register_blueprint(temp_blueprint)
    app.register_blueprint(sign_up_2_blueprint)
    # app.register_blueprint(agent_blueprint, url_prefix="/agent")
