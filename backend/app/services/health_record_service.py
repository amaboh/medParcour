from app.models import db, User, HealthRecord, HealthRecordVector
import spacy

class HealthRecordService:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
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
        
        self.create_health_record_vector(health_record)
        
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
        
        self.update_health_record_vector(health_record)
        return health_record.serialize()
    
    def create_health_record_vector(self, health_record):
        vector = self.generate_health_record_vector(health_record)
        health_record_vector = HealthRecordVector(health_record_id=health_record.id, vector=vector)
        db.session.add(health_record_vector)
        db.session.commit()

    def update_health_record_vector(self, health_record):
        health_record_vector = HealthRecordVector.query.filter_by(health_record_id=health_record.id).first()
        if health_record_vector:
            vector = self.generate_health_record_vector(health_record)
            health_record_vector.vector = vector
            db.session.commit()
            
    def generate_health_record_vector(self, health_record):
        # Extracting relevant entities from the health record
        entities = [
            health_record.illness,
            health_record.medication,
            health_record.medication_instructions,
            health_record.duration,
            health_record.observations
        ]

        # Preprocess the entities
        processed_entities = [self.preprocess_text(entity) for entity in entities]

        # Generate word embeddings for each entity
        entity_vectors = [self.generate_entity_vector(entity) for entity in processed_entities]

        # Combine the entity vectors into a single vector
        health_record_vector = self.combine_vectors(entity_vectors)

        return health_record_vector

    def preprocess_text(self, text):
        # Perform text preprocessing
        doc = self.nlp(text.lower())
        processed_text = " ".join([token.text for token in doc if not token.is_punct])
        return processed_text

    def generate_entity_vector(self, entity):
        # Generate word embeddings for the entity using spaCy
        doc = self.nlp(entity)
        entity_vector = doc.vector
        return entity_vector

    def combine_vectors(self, vectors):
        # Combine the entity vectors into a single vector
        combined_vector = sum(vectors) / len(vectors)
        return combined_vector