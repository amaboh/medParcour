
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import pgvector
from pgvector.sqlalchemy import Vector


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    person_of_contact = db.Column(db.String(100), nullable=False)
    health_records = db.relationship('HealthRecord', backref='user', lazy=True)
    doctors = db.relationship('Doctor', secondary='doctor_patient', back_populates='patients')

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    patients = db.relationship('User', secondary='doctor_patient', back_populates='doctors')
    remarks = db.Column(db.Text)

doctor_patient = db.Table('doctor_patient',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    illness = db.Column(db.String(100), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    medication_instructions = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    observations = db.Column(db.Text)
    doctor_name = db.Column(db.String(100), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ConversationVector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    vector = db.Column(Vector(768))

class HealthRecordVector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health_record_id = db.Column(db.Integer, db.ForeignKey('health_record.id'), nullable=False)
    vector = db.Column(Vector(768))
    
    
    
   