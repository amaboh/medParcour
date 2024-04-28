from app.models import db, User, HealthRecord

class HealthRecordService:
    def create_health_record(self, user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None
        
        health_record = HealthRecord(
            user_id=user_id,
            illness=data['illness'],
            medication=data['medication'],
            medication_instructions=data['medication_instructions'],
            duration=data['duration'],
            observations=data.get('observations', ''),
            doctor_name=data['doctor_name'],
            hospital=data['hospital']
        )
        db.session.add(health_record)
        db.session.commit()
        
        return health_record.serialize()
    
    def get_user_health_records(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return []
        
        health_records = HealthRecord.query.filter_by(user_id=user_id).all()
        return [health_record.serialize() for health_record in health_records]
    
    def update_health_record(self, user_id, health_record_id, data):
        health_record = HealthRecord.query.filter_by(id=health_record_id, user_id=user_id).first()
        if not health_record:
            return None
        
        health_record.illness = data.get('illness', health_record.illness)
        health_record.medication = data.get('medication', health_record.medication)
        health_record.medication_instructions = data.get('medication_instructions', health_record.medication_instructions)
        health_record.duration = data.get('duration', health_record.duration)
        health_record.observations = data.get('observations', health_record.observations)
        health_record.doctor_name = data.get('doctor_name', health_record.doctor_name)
        health_record.hospital = data.get('hospital', health_record.hospital)
        
        db.session.commit()
        
        return health_record.serialize()