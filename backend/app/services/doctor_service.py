from app.models import Doctor, HealthRecord, User, UserRecords, DoctorRemark
from app import db

class DoctorService:
    def get_patient_health_records(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return None

        health_records = HealthRecord.query.join(User).filter(User.id == HealthRecord.user_id).filter(User.user_records.has(UserRecords.doctors.any(Doctor.id == doctor_id))).all()
        return health_records

    def add_doctor_remark(self, health_record_id, doctor_id, remark):
        health_record = HealthRecord.query.get(health_record_id)
        if not health_record:
            return 'health_record_not_found'

        if not doctor_id or not remark:
            return 'missing_fields'

        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return 'doctor_not_found'

        doctor_remark = DoctorRemark(health_record_id=health_record_id, doctor_id=doctor_id, remark=remark)
        db.session.add(doctor_remark)
        db.session.commit()

        return 'success'