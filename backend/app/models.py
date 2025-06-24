from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from app.database import Base

class Spreadsheet(Base):
    __tablename__ = "spreadsheets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Tab(Base):
    __tablename__ = "tabs"
    id = Column(Integer, primary_key=True, index=True)
    spreadsheet_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    filter_conditions = Column(JSON, nullable=True)  # e.g., {"column": "age", "operator": ">", "value": 30}
    display_settings = Column(JSON, nullable=True)   # e.g., {"visible_columns": ["name", "age"]}
    created_at = Column(DateTime, server_default=func.now())

# Note: Dynamic tables (spreadsheet_<id>) are created at runtime with:
# CREATE TABLE spreadsheet_<id> (
#     id SERIAL PRIMARY KEY,
#     data JSONB NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# )
