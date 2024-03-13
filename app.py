import flask
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers import Dicom_Processor
from entities.Patient import Patient, Base as PatientBase
from entities.CTScan import CTScan, Base as CTScanBase
from entities.Doctor import Doctor,Base as DoctorBase
from services.Doctor_Service import Doctor_Service

app = Flask(__name__)

connection_url = "mysql+pymysql://root:arthrex09032001@localhost/Internship"
engine = create_engine(connection_url)

PatientBase.metadata.create_all(engine)
CTScanBase.metadata.create_all(engine)
DoctorBase.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

Doctor_Service(connection_url)
Doctor_Service.create_tables()

@app.route("/")
def welcome_page():
    return "Welcome to the code of the final internship project"

@app.route("/add_doctor", methods = ['POST'])
def add_doctor():
    data = request.get_json()
    name = data.get('name')
    speciality = data.get('speciality')
    doctor_id = data.get('doctor_id')

    Doctor_Service.add_doctor(name=name, speciality=speciality, doctor_id=doctor_id)
    return jsonify({"message": "Doctor added successfully"}), 201

    # function to get the details of a particular doctor based on the doctor id
@app.route('/get_doctor_details', methods=['GET'])
def get_doctor_details():
    doctor_id = request.args.get('doctor_id')
    doctor_details = Doctor_Service.get_doctor_details(doctor_id)
    if doctor_details:
        return jsonify(doctor_details), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404

"""==============================================================================================================================="""

@app.route('/add_patient', methods=['POST'])
def add_patient():
    data = request.get_json()

    # Check if all required fields are present
    required_fields = ['name', 'age', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Extract patient data from request
    name = data['name']
    age = data['age']
    gender = data['gender']

    # Create a new patient object
    new_patient = Patient(name=name, age=age, gender=gender)

    # Add the patient to the database session
    session.add(new_patient)
    session.commit()

    return jsonify({'message': 'Patient added successfully'}), 201

"""=============================================================================================================================="""

@app.route("/upload_scan", methods=['POST'])
def process_dicom():
    if request.method == 'POST':
        dicom_image_path = request.files['dicom_image_path']
        if dicom_image_path.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Save the uploaded file to a location
        file_path = "/Users/niranjand/Desktop/Final_Project/Medical_Project/" + dicom_image_path.filename
        dicom_image_path.save(file_path)

        # Pass the file path to your controller function for processing
        result = Dicom_Processor.get_processed_data(file_path)

        # Check if the patient already exists in the database
        patient = session.query(Patient).filter_by(name=result['patient_name']).first()

        if patient:
            # Check if the patient has an existing scan
            existing_scan = session.query(CTScan).filter_by(patient_id=patient.id).first()
            if existing_scan:
                # Patient has an existing scan, create a new row with the scan object
                new_scan = CTScan(
                    patient_id=patient.id,
                    study_date=result['study_date'],
                    series_description=result['series_description'],
                    organ_type=result['organ_type'],
                    study_description=result['study_description']
                )
                session.add(new_scan)
            else:
                # Patient does not have an existing scan, update the existing scan object
                existing_scan.study_date = result['study_date']
                existing_scan.series_description = result['series_description']
                existing_scan.organ_type = result['organ_type']
                existing_scan.study_description = result['study_description']
        else:
            # Patient does not exist, create a new patient and associated CTScan object
            new_patient = Patient(
                name=result['patient_name'],
                # Add other patient attributes here like age, gender if needed
            )
            session.add(new_patient)
            session.flush()  # Ensure the new_patient object gets an ID before referencing it

            new_scan = CTScan(
                patient_id=new_patient.id,
                study_date=result['study_date'],
                series_description=result['series_description'],
                organ_type=result['organ_type'],
                study_description=result['study_description']
            )
            session.add(new_scan)

        # Commit the changes to the database
        session.commit()

        # Close the session
        session.close()

        return jsonify(result)  # returning the result in the JSON file format
