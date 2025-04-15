
# Hospital_DBMS

## Description

This project aims to implement a Database Management System (DBMS) for a hospital. The application is designed to perform hospital operations by managing patient records, staff information, appointments, and other related data.

## Features

- Login/Signup for Patient and Doctor
- Schedule doctor appointments 
- Access entire medical history 
- Review prescriptions and test reports

## Technologies Used

- Python
- Mysql

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/drbals/Hospital_DBMS.git
    ```

2. Navigate to the project directory:
  
    ```bash
    cd Hospital_DBMS
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create hospital database and create schema:
  
    ```bash
   Install MySql community server and MySql WorkBench
   create schema hospital;
   Run app.sql script on hospital database using WorkBench
    ```

## Usage

1. start the server:

    ```bash
    python server.py
    ```

2. start the client:

    ```bash
    python hospital.py
    ```

## Project Structure

- `server.py`: The script to run the backend server connecting to db
- `app.sql`: Database schema
- `dataload.py`: Commands to populate database tables
- `hospital.py`: The entrypoint for frontend GUI
- `app.py`: OOP logic for multiple frontend pages

## Application Screenshots

![Login Form](./images/loginForm.png)

![Signup From](./images/patientSignup.png)

![Patient Dashboard](./images/dashboard.png)

![Doctor Dashboard](./images/docDashboard.png)