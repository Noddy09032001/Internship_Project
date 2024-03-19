import pydicom as pdcom

"""The main function of the class is to process the dicom image
the dcmread function reads the dicom file through the path provided """


class Dicom_Processor:
    @staticmethod
    def get_processed_data(file_path):
        dicom_data = pdcom.dcmread(file_path)

        # storing the metadata in the image as a form of dictionary to return to the calling functions
        processed_data = {
            'patient_name': str(dicom_data.PatientName),
            'study_date': str(dicom_data.StudyDate),
            'series_description': str(dicom_data.SeriesDescription),
            'organ_type': str(dicom_data.BodyPartExamined),
            'study_description': str(dicom_data.StudyDescription)
        }
        return processed_data  # returning as a form of a dictionary

