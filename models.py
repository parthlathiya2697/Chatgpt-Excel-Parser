from sqlalchemy import Column, Integer, String, Float
from database import Base

class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)
    original_id = Column(Integer)
    name = Column(String)
    description = Column(String)
    price = Column(Float)
    extracted_info = Column(String)
