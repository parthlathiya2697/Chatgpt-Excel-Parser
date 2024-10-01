uvicorn main:app --reload
1. Start the FastAPI Server
Run the following command in your project directory:

bash
Copy code
uvicorn main:app --reload
This will start the server on http://127.0.0.1:8000.


Process Spreadsheets
You can trigger the processing of all sample spreadsheets by making a POST request to the /process_spreadsheets/ endpoint.

Using a Browser or API Client:
Navigate to http://127.0.0.1:8000/docs to access the interactive API docs.
Find the process_spreadsheets endpoint and click "Try it out" -> "Execute".


Upload and Process a Single Spreadsheet
You can upload and process a single Excel file using the /upload_and_process/ endpoint.


Using the API Docs:
Navigate to http://127.0.0.1:8000/docs.
Find the upload_and_process endpoint.
Click "Try it out", upload your file, and click "Execute".


Retrieve Extracted Data
To retrieve all extracted data from the database:


Using a Browser:
Navigate to http://127.0.0.1:8000/extracted_data/.


How It Works
FastAPI Application
Endpoints:

POST /process_spreadsheets/: Processes all Excel files in the sample_data folder.
POST /upload_and_process/: Allows users to upload and process a single Excel file.
GET /extracted_data/: Retrieves all extracted data from the database.
Background Tasks: The processing of spreadsheets is done as a background task to prevent blocking the main thread.

Data Processing
Sample Data Generation: On startup, the application generates sample Excel files with mock data.

Processing Excel Files:

Reads each Excel file using pandas.
Iterates over each row and sends the data to the OpenAI ChatGPT API for extraction and summarization.
Stores the original and extracted data in a SQLite database using SQLAlchemy ORM.
OpenAI ChatGPT Interaction
Prompt Construction: For each row, a prompt is created to instruct ChatGPT to extract key information and summarize the product data.

API Call: Uses the openai.ChatCompletion.create() method to interact with the ChatGPT model.

Database Integration
SQLite Database: The application uses SQLite for simplicity, but you can replace it with any other database by adjusting the connection string and setup.

SQLAlchemy ORM: Handles database interactions and models.

