import json
import threading

from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configFiles.config import Config
from controllers.File_Controller import File_Controller
from database_configurations.setup import setup_database
from services.File_Service import File_Service
from services.Patient_Service import Patient_Service
from services.Scan_Service import Scan_Service

"""importing the pymysql module for establishing connection with the database"""

from services.Dicom_Processor import Dicom_Processor
from services.Doctor_Service import Doctor_Service

app = Flask(__name__)

# Load config
with open('configFiles/config.json', 'r') as cfg_files:
    config = json.load(cfg_files)
    directory = config['directory']
    connection_url = config['connection_url']

session = setup_database(app, connection_url) # importing this from the database_configurations package which has the code to setup the db


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

    existing_doctor = Doctor_Service.check_duplicates(name, doctor_id, speciality, session)
    if existing_doctor:
        return jsonify({'error': 'Patient with these credentials already exist in the database'}), 409

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

    """checking if the patient already exists"""

    existing_patient = Patient_Service.check_for_duplicates(name, age, gender, session)
    if existing_patient:
        return jsonify({'error': 'Patient with these credentials already exist in the database'}), 409

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
        search_directory = directory   #"/Users/niranjand/Desktop/Final_Project/Final_Internship_Project/"
        extension = ".dcm"
        names = f"{name_file}{extension}"
        print(names)

        result = File_Service.get_files(directory=search_directory, search_name=names)

        # now since we have the file pass this to the ImageProcessor to get the extracted data from the image
        """the dicom_data has the metadata extracted in the dictionary format"""
        dicom_data = Dicom_Processor.get_processed_data(result[0])

        Scan_Service.add_scan(dicom_data, session)

        print(result)
        return jsonify(dicom_data)  # Return the processed data as JSON

@app.route("/dicom1", methods=['POST'])
def process_dicom_images():
    if 'dicom_images' not in request.files:
        return jsonify({'error': 'No DICOM images provided'})

    dicom_images = request.files.getlist('dicom_images')
    name_files = request.form.getlist('name_files')
    responses = []

    if len(dicom_images) != len(name_files):
        return jsonify({'error': 'Number of images and filenames do not match'})

    def process_image(dicom_image, name_file):
        extensions = ".dcm"
        file_path = directory + name_file + extensions
        dicom_image.save(file_path)
        processed_data = Dicom_Processor.get_processed_data(file_path)
        responses.append({'file_name': name_file, 'file_path': file_path, 'processed_data': processed_data})

    threads = []
    for dicom_image, name_file in zip(dicom_images, name_files):
        thread = threading.Thread(target=process_image, args=(dicom_image, name_file))
        threads.append(thread)

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return jsonify({'status': 'Processing complete', 'responses': responses})

if __name__ == "__main__":
    app.run(debug=True)
