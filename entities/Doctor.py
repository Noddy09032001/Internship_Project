import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()   # declare the thing for orm mappings and classes

"""creating the doctor table to store the information about the doctors available"""

class Doctor(Base):
    __tablename__ = "Doctor"

    """determining the columns of the database """
    id = Column(Integer, primary_key = True)
    name = Column(String)
    doctor_id = Column(String)
    speciality = Column(String)