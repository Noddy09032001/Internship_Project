from entities.Patient import Patient


class Patient_Service:
    @staticmethod
    def add_patient(name, age, gender, session_object):
        new_patient = Patient(name=name, age=age, gender=gender)
        session_object.add(new_patient)
        session_object.commit()
        session_object.close()

    """this function will check for the duplicates inside the database and return the object if duplicates are there
    if not then the following will return null"""
    @staticmethod
    def check_for_duplicates(name, age, gender, session_object):
        existing_patient = session_object.query(Patient).filter_by(name=name, age=age, gender=gender).first()
        return existing_patient