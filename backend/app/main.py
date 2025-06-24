from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import engine, Base, get_db
from typing import List, Optional

app = FastAPI()

# Create metadata tables
Base.metadata.create_all(bind=engine)

@app.post("/spreadsheets/", response_model=schemas.SpreadsheetResponse, status_code=201)
async def create_spreadsheet(spreadsheet: schemas.SpreadsheetCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_spreadsheet(db, spreadsheet.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/spreadsheets/{spreadsheet_id}/data", response_model=schemas.RecordResponse, status_code=201)
async def create_record(spreadsheet_id: int, record: schemas.RecordCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_record(db, spreadsheet_id, record.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/spreadsheets/{spreadsheet_id}/data", response_model=List[schemas.RecordResponse])
async def read_spreadsheet_data(spreadsheet_id: int, tab_id: Optional[int] = None, db: Session = Depends(get_db)):
    try:
        return crud.read_records(db, spreadsheet_id, tab_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/spreadsheets/{spreadsheet_id}/data/{record_id}", response_model=schemas.RecordResponse)
async def update_record(spreadsheet_id: int, record_id: int, record: schemas.RecordUpdate, db: Session = Depends(get_db)):
    try:
        return crud.update_record(db, spreadsheet_id, record_id, record.data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/spreadsheets/{spreadsheet_id}/data/{record_id}", status_code=200)
async def delete_record(spreadsheet_id: int, record_id: int, db: Session = Depends(get_db)):
    try:
        return crud.delete_record(db, spreadsheet_id, record_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/spreadsheets/{spreadsheet_id}/search", response_model=List[schemas.RecordResponse])
async def search_data(spreadsheet_id: int, query: str, db: Session = Depends(get_db)):
    try:
        return crud.search_records(db, spreadsheet_id, query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
