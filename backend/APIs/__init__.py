from .temp_api import temp_blueprint
# from backend.APIs.agent_api import agent_blueprint

def api_blueprints(app):
    # Register blueprints
    app.register_blueprint(temp_blueprint)
    # app.register_blueprint(agent_blueprint, url_prefix="/agent")
