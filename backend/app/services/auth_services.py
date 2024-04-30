from app.models import db, User, Doctor, UserRecords
from werkzeug.security import generate_password_hash, check_password_hash

class AuthService:
    def register_user(self, name, email, password, phone):
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password, phone=phone)
        db.session.add(user)
        db.session.commit()
        return user


    def register_doctor(self, name, email, password):
        hashed_password = generate_password_hash(password)
        doctor = Doctor(name=name, email=email, password=hashed_password)
        db.session.add(doctor)
        db.session.commit()
        return doctor
    
    def register_user_records(self, user_id, age, address, date_of_birth, person_of_contact):
        user_records = UserRecords.query.filter_by(user_id=user_id).first()
        if user_records:
            user_records.age = age
            user_records.address = address
            user_records.date_of_birth = date_of_birth
            user_records.person_of_contact = person_of_contact
        else:
            user_records = UserRecords(
                user_id=user_id,
                age=age,
                address=address,
                date_of_birth=date_of_birth,
                person_of_contact=person_of_contact
            )
            db.session.add(user_records)
        db.session.commit()
        return user_records


    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        return None

    def authenticate_doctor(self, email, password):
        doctor = Doctor.query.filter_by(email=email).first()
        if doctor and check_password_hash(doctor.password, password):
            return doctor
        return None

    def get_user_details(self, user):
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'age': user.age,
            'address': user.address,
            'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
            'person_of_contact': user.person_of_contact
        }

    def get_doctor_details(self, doctor):
        return {
            'id': doctor.id,
            'name': doctor.name,
            'email': doctor.email
        }