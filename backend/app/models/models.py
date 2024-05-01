
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
    user_records = db.relationship('UserRecords', backref='user', uselist=False)

class UserRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)
    person_of_contact = db.Column(db.String(100))
    doctors = db.relationship('Doctor', secondary='doctor_patient', back_populates='patients')

    
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    patients = db.relationship('UserRecords', secondary='doctor_patient', back_populates='doctors')
    health_records = db.relationship('HealthRecord', backref='doc', lazy=True)
    remarks = db.Column(db.Text)

class HealthRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=True)
    illness = db.Column(db.String(100), nullable=False)
    medication = db.Column(db.String(100), nullable=False)
    medication_instructions = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    observations = db.Column(db.Text)
    doctor_name = db.Column(db.String(100), nullable=False)
    hospital = db.Column(db.String(100), nullable=False)
    
    user = db.relationship('User', backref=db.backref('health_records', lazy=True))
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'patient_name': self.user.name,
            'illness': self.illness,
            'medication': self.medication,
            'medication_instructions': self.medication_instructions,
            'duration': self.duration,
            'observations': self.observations,
            'doctor_name': self.doctor_name,
            'hospital': self.hospital
        }
    

doctor_patient = db.Table('doctor_patient',
    db.Column('doctor_id', db.Integer, db.ForeignKey('doctor.id'), primary_key=True),
    db.Column('user_records_id', db.Integer, db.ForeignKey('user_records.id'), primary_key=True)
)
class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ConversationVector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    vector = db.Column(Vector(300))

class HealthRecordVector(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health_record_id = db.Column(db.Integer, db.ForeignKey('health_record.id'), nullable=False)
    vector = db.Column(Vector(300))
    

class DoctorRemark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    health_record_id = db.Column(db.Integer, db.ForeignKey('health_record.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    remark = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    health_record = db.relationship('HealthRecord', backref=db.backref('remarks', lazy=True))
    doctor_observations = db.relationship('Doctor', backref=db.backref('assigned_remarks', lazy=True))
    
    
    
   