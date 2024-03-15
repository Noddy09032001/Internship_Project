from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from controllers.File_Controller import File_Controller
from services.File_Service import File_Service
from services.Patient_Service import Patient_Service
from services.Scan_Service import Scan_Service

"""importing the pymysql module for establishing connection with the database"""

from services.Dicom_Processor import Dicom_Processor
from entities.Patient import Patient, Base as PatientBase
from entities.Patient import CTScan, Base as CTScanBase
from entities.Doctor import Doctor,Base as DoctorBase
from services.Doctor_Service import Doctor_Service

app = Flask(__name__)

connection_url = "mysql+pymysql://root:arthrex09032001@localhost/FinalProject"
engine = create_engine(connection_url)

"""manages the connection to the database
also helps in connection pooling and handling of the transactions towards the database we have created"""

"""
the create_all() is used to create all the tables in the database 
"""
PatientBase.metadata.create_all(engine)
CTScanBase.metadata.create_all(engine)
DoctorBase.metadata.create_all(engine)

"""ye session just hibernate ke session ke tarah hota hai which allows communication
with the database. Same procedure as we do in hibernate"""
# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# the entry point or the main function of the code, we will get redirected here on the first call
@app.route("/")
def welcome_page():
    return "Welcome to the code of the final internship project"

@app.route("/doctor", methods = ['POST'])
def add_doctor():
    data = request.json

    # Check if all required fields are present
    required_fields = ['name', 'doctor_id', 'speciality']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Extract doctor data from request
    name = data['name']
    doctor_id = data['doctor_id']
    speciality = data['speciality']

    Doctor_Service.add_doctor(name,doctor_id,speciality,session)
    return jsonify({'message': 'Doctor added successfully'}), 201
    # function to get the details of a particular doctor based on the doctor id
@app.route('/doctor_details', methods=['GET'])
def get_doctor_details():
    doctor_id = request.args.get('doctor_id')
    doctor_details = Doctor_Service.get_doctor_details(doctor_id)
    if doctor_details:
        return jsonify(doctor_details), 200
    else:
        return jsonify({"message": "Doctor not found"}), 404

"""==============================================================================================================================="""

@app.route('/patient', methods=['POST'])
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

    Patient_Service.add_patient(name,age,gender,session)
    return jsonify({'message': 'Patient added successfully'}), 201

"""=============================================================================================================================="""

@app.route("/dicom", methods = ['POST'])
def get_image():
    if request.method == 'POST':
        dicom_image = request.files['dicom_image']
        name_file = request.form['name_file']
        file_path = File_Controller.get_saved_file_path(dicom_image, name_file)
        dicom_image.save(file_path)


        return f"File name stored is: {file_path}"

@app.route("/scan", methods = ['POST'])
def get_file_list():
    if request.method == 'POST':
        name_file = request.form['name_file']
        directory = "/Users/niranjand/Desktop/Final_Project/Final_Internship_Project/"
        extension = ".dcm"
        names = f"_{name_file}{extension}"
        print(names)

        result = File_Service.get_files(directory=directory, search_name=names)

        # now since we have the file pass this to the ImageProcessor to get the extracted data from the image
        """the dicom_data has the metadata extracted in the dictionary format"""
        dicom_data = Dicom_Processor.get_processed_data(result[0])

        Scan_Service.add_scan(dicom_data, session)

        print(result)
        return jsonify(dicom_data)  # Return the processed data as JSON



if __name__ == "__main__":
    app.run(debug=True)
