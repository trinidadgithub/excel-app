from sqlalchemy.orm import Session
from app.models import Spreadsheet
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text  # Add this import
from typing import Optional
import json

def create_spreadsheet(db: Session, name: str):
    try:
        # Create spreadsheet metadata
        db_spreadsheet = Spreadsheet(name=name)
        db.add(db_spreadsheet)
        db.commit()
        db.refresh(db_spreadsheet)
        
        # Create dynamic table with JSONB index
        table_name = f"spreadsheet_{db_spreadsheet.id}"
        db.execute(text(f"""
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))
        # Add GIN index for JSONB search
        db.execute(text(f"CREATE INDEX idx_{table_name}_data ON {table_name} USING GIN (data)"))
        db.commit()
        
        return db_spreadsheet
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to create spreadsheet: {str(e)}")

def create_record(db: Session, spreadsheet_id: int, data: dict):
    try:
        table_name = f"spreadsheet_{spreadsheet_id}"
        # Verify table exists
        result = db.execute(text(f"SELECT to_regclass('{table_name}')"))
        if result.scalar() is None:
            raise Exception(f"Spreadsheet {spreadsheet_id} does not exist")
        
        # Insert record
        result = db.execute(text(f"INSERT INTO {table_name} (data) VALUES (:data) RETURNING id, data, created_at"), {"data": json.dumps(data)})
        db.commit()
        return result.fetchone()
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to create record: {str(e)}")

def read_records(db: Session, spreadsheet_id: int, tab_id: Optional[int] = None):
    try:
        table_name = f"spreadsheet_{spreadsheet_id}"
        # Verify table exists
        result = db.execute(text(f"SELECT to_regclass('{table_name}')"))
        if result.scalar() is None:
            raise Exception(f"Spreadsheet {spreadsheet_id} does not exist")
        
        # Fetch all records (tab filtering TBD)
        result = db.execute(text(f"SELECT id, data, created_at FROM {table_name}"))
        return [dict(row) for row in result.fetchall()]
    except SQLAlchemyError as e:
        raise Exception(f"Failed to read records: {str(e)}")

def update_record(db: Session, spreadsheet_id: int, record_id: int, data: dict):
    try:
        table_name = f"spreadsheet_{spreadsheet_id}"
        # Verify table exists
        result = db.execute(text(f"SELECT to_regclass('{table_name}')"))
        if result.scalar() is None:
            raise Exception(f"Spreadsheet {spreadsheet_id} does not exist")
        
        # Update record
        result = db.execute(text(f"UPDATE {table_name} SET data = :data WHERE id = :id RETURNING id, data, created_at"), {"data": json.dumps(data), "id": record_id})
        db.commit()
        row = result.fetchone()
        if row is None:
            raise Exception(f"Record {record_id} not found")
        return row
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to update record: {str(e)}")

def delete_record(db: Session, spreadsheet_id: int, record_id: int):
    try:
        table_name = f"spreadsheet_{spreadsheet_id}"
        # Verify table exists
        result = db.execute(text(f"SELECT to_regclass('{table_name}')"))
        if result.scalar() is None:
            raise Exception(f"Spreadsheet {spreadsheet_id} does not exist")
        
        # Delete record
        result = db.execute(text(f"DELETE FROM {table_name} WHERE id = :id RETURNING id"), {"id": record_id})
        db.commit()
        if result.rowcount == 0:
            raise Exception(f"Record {record_id} not found")
        return {"message": "Record deleted"}
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Failed to delete record: {str(e)}")

def search_records(db: Session, spreadsheet_id: int, query: str):
    try:
        table_name = f"spreadsheet_{spreadsheet_id}"
        # Verify table exists
        result = db.execute(text(f"SELECT to_regclass('{table_name}')"))
        if result.scalar() is None:
            raise Exception(f"Spreadsheet {spreadsheet_id} does not exist")
        
        # Simple JSONB search (e.g., query="name:John" or "age>30")
        if ":" in query:
            field, value = query.split(":", 1)
            sql_query = f"SELECT id, data, created_at FROM {table_name} WHERE data->>'{field}' ILIKE :value"
            result = db.execute(text(sql_query), {"value": f"%{value}%"})
        else:
            # Search across all fields in JSONB
            sql_query = f"SELECT id, data, created_at FROM {table_name} WHERE data::text ILIKE :value"
            result = db.execute(text(sql_query), {"value": f"%{query}%"})
        
        return [dict(row) for row in result.fetchall()]
    except SQLAlchemyError as e:
        raise Exception(f"Failed to search records: {str(e)}")
