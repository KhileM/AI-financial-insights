from flask import Flask
from config import Config
from models.database import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    JWTManager(app)

    with app.app_context():
        # Import models here so SQLAlchemy can register them
        from models import user
        from routes.auth import auth_bp
        app.register_blueprint(auth_bp)
        
        db.create_all()  # Will create tables once models are defined

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)