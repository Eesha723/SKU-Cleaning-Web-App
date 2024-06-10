# SKU-Cleaning-Web-App
## Overview
The SKU Cleaning Web App is designed to upload, validate, and update SKU (Stock Keeping Unit) data in an Excel file format. The application performs several validation checks on the uploaded data, filters out invalid records, updates existing records in the database, and allows users to download a sample file. **(code can be found in webapp branch)**

## Project Structure
The project consists of two main files:

validation.py: Contains the functions for validating and updating SKU data. <br>
app.py: Contains the Flask application that handles file uploads, validations, and database updates.
## Setup
1. Clone the repository: <br> 
~~~
git clone https://github.com/yourusername/SKU-Cleaning-Web-App.git <br>
cd SKU-Cleaning-Web-App
~~~
2. Install the required packages: <br>
~~~
python Libraries.py
~~~
3. Configure database connection: <br>
Ensure your database connection settings are correctly configured in the connection.py file, which should include a function (in my case) uat_connection() returning the database connection string.

## Files Description
### validation.py
This script handles the validation and updating of SKU data. <br>

- #### Imports: <br>
  - Required modules for database connection, logging, and data processing. <br>
  - `pandas` for handling Excel files. <br>
  - `tqdm` for progress tracking. <br>
  - `re` for regular expression operations. <br>
  - `sqlalchemy.sql.text` for executing SQL queries. <br>
- #### Functions: <br>
  - `get_connection_uat()`: Establishes a connection to the UAT database. <br>
  - `validate_cat_CB_Packaging(row)`: Validates the categories, companies, brands, and packaging fields. <br>
  - `validate_measurement(row)`: Validates the measurement and measurement type fields. <br>
  - `validate_existing_data(df_excel)`: Validates the entire DataFrame, returning cleaned and uncleaned records. <br>
  - `update_existing_data(df_excel)`: Updates existing records in the database based on the cleaned data. <br>
### app.py
This script runs the Flask web application. <br>
- #### Routes: <br>
  - `/`: Handles file uploads and triggers validation and update functions. <br>
  - `/uploads/<filename>`: Displays the results of the upload and validation process. <br>
  - `/download_uncleaned/<filename>`: Allows downloading of uncleaned records. <br>
  - `/download_sample_file`: Provides a sample Excel file for users. <br>
- #### Functions: <br>
  - `allowed_file(filename)`: Checks if the uploaded file has an allowed extension (`.xlsx`). <br>
  - `upload_file()`: Handles the file upload, validation, and database update process. <br>
  - `uploaded_file(filename)`: Displays the results of the file upload and validation. <br>
  - `download_uncleaned_file(filename)`: Allows users to download the uncleaned records. <br>
  - `download_sample_file()`: Provides a sample Excel file. <br>

## Running the Application
#### 1. Start the Flask server: 
~~~
python app.py
~~~
#### 2. Access the application:
Open your web browser and go to `http://127.0.0.1:5000`.

## Usage
#### 1. Upload an Excel file:
  - Click on "Choose File" and select your Excel file (.xlsx). 
  - Click "Upload". 
#### 2. View results:
  - After the upload, the app will display the number of records updated and the number of uncleaned records.
  - If there are uncleaned records, you can download them for review.
#### 3. Download sample file:
  - Click on "Download Sample File" to get a template of the expected Excel file format.
## Logs
  - The application logs activities in the app.log file, including loading master files and applying validations.
## Dependencies
  - Flask
  - pandas
  - sqlalchemy
  - tqdm
