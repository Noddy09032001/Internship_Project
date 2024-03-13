from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()   # declare the thing for orm mappings and classes
class CTScan(Base):
    _tablename__ = 'ct_scans'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="ct_scans")

    # Add other columns as needed
    study_date = Column(String)
    series_description = Column(String)
    organ_type = Column(String)
    study_description = Column(String)