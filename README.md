# Digital_Data_Real_Time_Ingestion_Utility
a database with real-time ingestion utility for reliable digital signal data collection 

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

Developed within the **Institution** research environment, the system adheres to recognized data quality principles:
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

###  Database Schema

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

## Repository File List
- `DB-GitHub.py` — Main Python application for folder monitoring, GUI metadata entry, and Oracle database insertion.
- `DB_entry-GH.bat` — Windows batch launcher that opens the monitored folder and starts the Python application.
- `README.md` — Project overview, installation instructions, configuration details, usage workflow, and troubleshooting notes.
- `requirements.txt` — Python package dependencies and versions required to run the software.

