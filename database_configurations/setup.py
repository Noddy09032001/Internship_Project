from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import current_app
from configFiles.config import Config
from entities.Patient import Patient, Base as PatientBase
from entities.Patient import CTScan, Base as CTScanBase
from entities.Doctor import Doctor,Base as DoctorBase

def setup_database(app, connection_url):
    # Retrieve connection URL from app config
    connection_url = connection_url
    engine = create_engine(connection_url)

    # Create tables
    PatientBase.metadata.create_all(engine)
    CTScanBase.metadata.create_all(engine)
    DoctorBase.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session