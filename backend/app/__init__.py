from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.models import db
from app.models import User, Doctor, HealthRecord, Conversation, ConversationVector, HealthRecordVector
from app.routes.auth import auth_bp
from app.routes.health_record import health_record_bp
from app.routes.doctor import doctor_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')    
    
    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)
    
    #create database tables
    with app.app_context():
        try:
            session = db.session()
            session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error creating vector extension: {str(e)}")
        db.create_all()
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(health_record_bp)
    app.register_blueprint(doctor_bp)
    
    return app