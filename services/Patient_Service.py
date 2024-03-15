from entities.Patient import Patient


class Patient_Service:
    @staticmethod
    def add_patient(name, age, gender, session_object):
        new_patient = Patient(name=name, age=age, gender=gender)
        session_object.add(new_patient)
        session_object.commit()
        session_object.close()