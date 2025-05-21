from flask import Flask
from config import Config
from models.database import db
from routes.reports import reports_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(reports_bp)

    db.init_app(app)

    with app.app_context():
        # Import models here so SQLAlchemy can register them
        from models import user, transaction, card, user_profile, mcc_code
        from routes.insights import insights_bp
        app.register_blueprint(insights_bp)
        from routes.transactions import tx_bp
        app.register_blueprint(tx_bp)
        from routes.llm_routes import llm_bp
        app.register_blueprint(llm_bp)
        
        db.create_all()  # Will create tables once models are defined

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)