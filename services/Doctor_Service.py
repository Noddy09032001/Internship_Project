from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from entities.Doctor import Doctor

class Doctor_Service:

    """function to add the doctors to the database"""
    def add_doctor(self, name, doctor_id, speciality):
        session = self.Session()
        doctor = Doctor(name=name, doctor_id=doctor_id, speciality=speciality)
        session.add(doctor)
        session.commit()
        session.close()

    """get doctor details based on a particular id"""
    def get_doctor_details(self, doctor_id):
        session = self.Session()
        doctor = session.query(Doctor).filter_by(doctor_id = doctor_id).first()
        session.close()
        return doctor.to_dict() if doctor else None