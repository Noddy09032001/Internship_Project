import os

from flask import jsonify


class File_Controller:
    @staticmethod
    def get_saved_file_path(dicom_image, name_patient):
        if dicom_image.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Extracting the file extension
        filename, file_extension = os.path.splitext(dicom_image.filename)

        # Generating new filename with name_file appended
        new_filename = f"{filename}_{name_patient}{file_extension}"
        file_path = f"/Users/niranjand/Desktop/Final_Project/Final_Internship_Project/{new_filename}"
        return file_path
