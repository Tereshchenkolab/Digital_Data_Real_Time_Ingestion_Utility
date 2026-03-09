# Digital Data Real-Time Ingestion Utility
A database utility for reliable real-time ingestion of digital physiological signal data

**Version:** 1.0  
**Authors:** Shivangi Kewalramani, Hayden Caldwell, Larisa Tereshchenko  
**Institution:** Cleveland Clinic Main Campus  
**License:** This project will be distributed under the license selected on the PhysioNet publication platform.

---
## Overview

The **Digital Data Real-Time Ingestion Utility** is a Python-based application designed to automatically ingest digital physiological signal files (e.g., ECG, PCG) and corresponding metadata into an **Oracle database** in real time.

The tool integrates:
- **File Monitoring:** Automated detection of new files in a watched directory  
- **GUI Interface:** Research-assistant-friendly metadata input (patient demographics and history)  
- **Database Insertion:** Secure, traceable data entry using Oracle thin-mode connectivity  
This ensures that each physiological recording is **accurately paired with metadata**, improving traceability, reproducibility, and compliance with institutional data integrity standards.

---

## Background

Accurate and timely metadata collection is critical for longitudinal clinical research.  
Manual data entry often leads to inconsistencies and omissions.  
This utility addresses those gaps by integrating **real-time folder monitoring** and **controlled user input dialogs**, ensuring all digital recordings are synchronized with validated metadata at the moment of creation.

Developed within the **Cleveland Clinic** research environment, the system adheres to recognized data quality principles:
**completeness, consistency, integrity, and audit traceability.**

---

## Software Architecture

| Layer | Description |
|-------|--------------|
| **Database Layer** | Oracle instance with `ds_ecg_t1` target table for metadata ingestion |
| **Application Layer** | Python GUI using `tkinter` and `tkcalendar` |
| **Monitoring Layer** | Real-time file watcher using `watchdog` |
| **Database Driver** | `oracledb` (thin mode, no Oracle client installation required) |

---

## Database Schema

```sql
CREATE TABLE ds_ecg_t1 (
    study_id   NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 10001 INCREMENT BY 1) PRIMARY KEY,
    name       VARCHAR2(200) NOT NULL,
    mrn        VARCHAR2(6)   NOT NULL,
    dob        DATE          NOT NULL,
    age        NUMBER(5,2)   NOT NULL,
    sex        VARCHAR2(10)  NOT NULL,
    race_eth   VARCHAR2(10)  NOT NULL,
    shd_hist   NUMBER(1)     NOT NULL,
    as_hist    NUMBER(1)     NOT NULL,
    shd_eko    NUMBER(1)     NOT NULL,
    file_path  VARCHAR2(1024),
    study_date TIMESTAMP(6) DEFAULT SYSTIMESTAMP NOT NULL,
    usr_info   VARCHAR2(64)
);
```
---

## Configuration
The database schema `ds_ecg_t1` represents our laboratory’s system for storing the necessary information required for our study. However, this schema can easily be adapted to serve any requested database layout, provided that the database is hosted within an **Oracle Database server or instance**.
After creating your database schema in Oracle Database, several configuration steps must be performed in the `DB-GitHub.py` script to connect the ingestion utility to your database and correctly map user input variables.

### Connecting to Your Database
Update the following configuration variables in `DB-GitHub.py` to establish a connection to your Oracle database:
| Variable         | Description                                                             |
| ---------------- | ----------------------------------------------------------------------- |
| `DB_USERNAME`    | Username used to access the Oracle database                             |
| `DB_PASSWORD`    | Password associated with the database account                           |
| `DB_HOST`        | Host address of the Oracle database server                              |
| `DB_SERVICENAME` | Oracle service name for the database                                    |
| `BASE_FOLDER`    | Base directory where data-entry folders will be automatically generated |



**Note**

If your database uses an **SID instead of a service name**, modify the
`oracledb.connect()` call by replacing the `service_name` parameter with `dsn`.
Note:
If your database uses an SID instead of a service name, modify the connection call in `oracledb.connect()` by replacing the `service_name` parameter with `dsn`.
For production or institutional use, credentials should not be hard-coded. Instead, users should provide them through environment variables or a protected. env-style configuration mechanism and load them securely at runtime.

### Matching and Mapping Variables
The metadata collection interface is built using Tkinter GUI elements. Each input field is defined using a `tk.Label` statement followed by an input widget (e.g., text entry field, dropdown menu, or other input type).
Example GUI input definition:
```python
tk.Label(self, text="Enter the patient's first and last name:").pack(padx=10, pady=5)
self.name_entry = tk.Entry(self)
self.name_entry.pack(padx=10, pady=5)
```
Each user input must be mapped to a dialog result variable inside the `on_ok()` function. This is accomplished by calling the appropriate getter method for the input widget.
Example mapping:
```python
'name': self.name_entry.get(),
```
This syntax remains the same regardless of the type of input widget used.
### Declaring Global Variables
Inside the `prompt_user()` function, declare global variables for each dialog result. These variables must be global so they can be accessed later by the SQL insertion statement.
Example:
```python
global user_name
user_name = dialog.result['name']
```
### Inserting User Inputs into the Database
After establishing a connection to the Oracle database instance, insert the collected metadata into the target table using an `INSERT INTO` SQL command.
In the SQL statement:
1. Specify the table name.
2. List the database column names inside the first set of parentheses.
3. Provide corresponding variable values in the `VALUES` section.
Example:
```sql
INSERT INTO ds_ecg_t1 (name, mrn, dob, age, sex, study_date)
VALUES (:name, :mrn, :dob, :age, :sex, SYSTIMESTAMP)
```
Each SQL parameter must correspond to a previously defined variable, typically mapped from global variables created in `prompt_user()`.
Example variable mapping:
```python
'name': user_name
```

After completing these configuration steps, the script will be ready to connect to the Oracle database and ingest physiological signal metadata in real time.

---

## Getting Started
1.	Install Python 3.10 or later.
2.	Clone or download this repository.
3.	Install dependencies:
```bash
        pip install -r requirements.txt
```
4.	Open DB-GitHub.py and set the following configuration values:
DB_USERNAME, DB_PASSWORD, DB_HOST, DB_SERVICENAME, BASE_FOLDER
5.	Ensure the Oracle target table exists and that your user has INSERT privileges.
6.	Run the launcher:
Double-click `DB_entry-GH.bat`, or run:
```bash
python DB-GitHub.py
```
7.	A new watch folder will be created automatically inside BASE_FOLDER.
8.	Place a physiological signal file into the generated folder.
9.	Complete the metadata form when prompted.
10.	Verify successful insertion in the console output

---
## Usage Workflow

The typical workflow for using the Digital Data Real-Time Ingestion Utility is as follows:

1. Start the ingestion utility by running `DB_entry-GH.bat` or executing `python DB-GitHub.py`.

2. The application automatically creates a **watch folder** inside the directory specified by `BASE_FOLDER`.

3. The system continuously monitors this folder for newly added physiological signal files.

4. When a new signal file is detected, a **GUI metadata entry dialog** appears prompting the research assistant to enter patient and study information.

5. After the metadata form is completed and submitted, the application:
   - Associates the signal file with the entered metadata
   - Generates a new study identifier
   - Inserts the metadata and file reference into the Oracle database.

6. The database insertion status is displayed in the console output, confirming successful ingestion.

This workflow ensures that physiological signal recordings are immediately paired with validated metadata, improving traceability and data integrity for clinical research studies.

---

## Repository File List
- `DB-GitHub.py` — Main Python application for folder monitoring, GUI metadata entry, and Oracle database insertion.
- `DB_entry-GH.bat` — Windows batch launcher that opens the monitored folder and starts the Python application.
- `README.md` — Project overview, installation instructions, configuration details, usage workflow, and troubleshooting notes.
- `requirements.txt` — Python package dependencies and versions required to run the software.
---
