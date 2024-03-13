import pydicom as pdcom
class Dicom_Processor:
    def get_processed_data(self,file_path):
        dicom_data = pdcom.dcmread(file_path)
        processed_data = {
            'patient_name': str(dicom_data.PatientName),
            'study_date': str(dicom_data.StudyDate),
            'series_description': str(dicom_data.SeriesDescription),
            'organ_type': str(dicom_data.BodyPartExamined),
            'study_description': str(dicom_data.StudyDescription)
        }
        return processed_data

