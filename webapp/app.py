from flask import Flask
from routes.main import main_bp
from routes.ontology import ontology_bp
from routes.competency import competency_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")

    app.register_blueprint(main_bp)
    app.register_blueprint(ontology_bp, url_prefix="/ontology")
    app.register_blueprint(competency_bp, url_prefix="/competency")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)