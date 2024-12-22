from APIs.temp_api import temp_blueprint
from APIs.project_api import project_blueprint
from APIs.sign_up_2_api import sign_up_2_blueprint
from APIs.user_api import user_blueprint
from APIs.video_title_api import video_title_blueprint
from APIs.select_questions_api import select_questions_blueprint
from APIs.sources_api import sources_blueprint
from APIs.research_paper_api import researchpaper_blueprint
from APIs.youtube_api import youtube_blueprint
from APIs.webpage_api import webpage_blueprint

def api_blueprints(app):
    # Register blueprints
    app.register_blueprint(temp_blueprint)
    app.register_blueprint(video_title_blueprint)
    app.register_blueprint(sign_up_2_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(project_blueprint)
    app.register_blueprint(select_questions_blueprint)
    app.register_blueprint(sources_blueprint)
    app.register_blueprint(researchpaper_blueprint)
    app.register_blueprint(youtube_blueprint)
    app.register_blueprint(webpage_blueprint)
    # app.register_blueprint(agent_blueprint, url_prefix="/agent")
