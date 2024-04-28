from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.models import db
from app.models import User, Doctor, HealthRecord, Conversation, ConversationVector, HealthRecordVector
from app.routes.auth import auth_bp
from app.routes.health_record import health_record_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')    
    
    # Initialize database
    db.init_app(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_record_bp)
    
    return app