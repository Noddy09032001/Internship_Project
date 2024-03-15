from entities.Patient import Patient, CTScan


class Scan_Service:
    @staticmethod
    def add_scan(result, session_object):
        # Check if the patient already exists in the database
        patient = session_object.query(Patient).filter_by(name=result['patient_name']).first()

        if patient:
            # Check if the patient has an existing scan
            existing_scan = session_object.query(CTScan).filter_by(patient_id=patient.id).first()
            if existing_scan:
                # Patient has an existing scan, update the existing scan object
                existing_scan.study_date = result.get('study_date')
                existing_scan.series_description = result.get('series_description')
                existing_scan.organ_type = result.get('organ_type')
                existing_scan.study_description = result.get('study_description')
            else:
                # Patient does not have an existing scan, create a new row with the scan object
                new_scan = CTScan(
                    patient_id=patient.id,
                    study_date=result.get('study_date'),
                    series_description=result.get('series_description'),
                    organ_type=result.get('organ_type'),
                    study_description=result.get('study_description')
                )
                session_object.add(new_scan)
        else:
            # Patient does not exist, create a new patient and associated CTScan object
            new_patient = Patient(
                name=result['patient_name'],
                # Add other patient attributes here like age, gender if needed
            )
            session_object.add(new_patient)
            session_object.flush()  # Ensure the new_patient object gets an ID before referencing it

            new_scan = CTScan(
                patient_id=new_patient.id,
                study_date=result.get('study_date'),
                series_description=result.get('series_description'),
                organ_type=result.get('organ_type'),
                study_description=result.get('study_description')
            )
            session_object.add(new_scan)

        # Commit the changes to the database
        session_object.commit()

        # Close the session
        session_object.close()
