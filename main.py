from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from pathlib import Path
import pandas as pd
import openai
import os
from models import ExtractedData, Base
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import shutil
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Create sample data folder
sample_data_folder = Path('sample_data')
sample_data_folder.mkdir(exist_ok=True)

@app.on_event("startup")
def startup_event():
    # Generate sample Excel files on startup
    from sample_data_generator import create_sample_excel_files
    create_sample_excel_files(sample_data_folder)

@app.post("/process_spreadsheets/")
async def process_spreadsheets(background_tasks: BackgroundTasks):
    """
    Endpoint to process all spreadsheets in the sample_data folder.
    """
    background_tasks.add_task(process_excel_files)
    return {"message": "Processing of spreadsheets has started in the background."}

@app.post("/upload_and_process/")
async def upload_and_process(file: UploadFile = File(...)):
    """
    Endpoint to upload and process a single Excel file.
    """
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Only .xlsx files are accepted."})
    
    file_location = f"uploaded_files/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process the uploaded file
    process_single_file(file_location)
    return {"message": f"File {file.filename} has been uploaded and processed."}

def process_excel_files():
    """
    Processes all Excel files in the sample_data folder.
    """
    db = SessionLocal()
    try:
        for excel_file in sample_data_folder.glob('*.xlsx'):
            print(f'Processing file: {excel_file}')
            df = pd.read_excel(excel_file)
            rows = list(df.iterrows())  # Convert generator to list to get the total count
            total_rows = len(rows)
            for index, row in rows:
                print(f'Processing row: [{index + 1}/{total_rows}]')
                extracted_info = extract_info_with_chatgpt(row.to_dict())
                data = ExtractedData(
                    original_id=int(row['ID']),
                    name=row['Name'],
                    description=row['Description'],
                    price=float(row['Price']),
                    extracted_info=extracted_info
                )
                db.add(data)
                db.commit()
                print(f'Processed row ID {row["ID"]}')
    finally:
        db.close()
    print('All files have been processed and data has been stored in the database.')

def process_single_file(file_path):
    """
    Processes a single Excel file.
    """
    db = SessionLocal()
    try:
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            extracted_info = extract_info_with_chatgpt(row.to_dict())
            data = ExtractedData(
                original_id=int(row['ID']),
                name=row['Name'],
                description=row['Description'],
                price=float(row['Price']),
                extracted_info=extracted_info
            )
            db.add(data)
            db.commit()
            print(f'Processed row ID {row["ID"]}')
    finally:
        db.close()
    print(f'File {file_path} has been processed and data has been stored in the database.')

from openai import OpenAI

client = OpenAI()

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

def extract_info_with_chatgpt(row_data):
    """
    Uses ChatGPT to extract and summarize information from a row of data.
    """
    if DEBUG:
        # Return a fake response for development purposes
        return "This is a fake response for development purposes."

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Extract key information and summarize the following product data:\n\n{row_data}"}
    ]
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages
    )
    
    extracted_info = completion.choices[0].message['content'].strip()
    return extracted_info

@app.get("/extracted_data/")
def get_extracted_data():
    """
    Endpoint to retrieve all extracted data from the database.
    """
    db = SessionLocal()
    try:
        data = db.query(ExtractedData).all()
        return data
    finally:
        db.close()
