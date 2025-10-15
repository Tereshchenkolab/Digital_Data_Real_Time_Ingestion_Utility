import os
import time
import threading
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import oracledb
import getpass

# Use thin mode (pure Python, no Oracle Client needed)
# Oracle DB connection config
DB_USERNAME = "Enter Database Username Here"
DB_PASSWORD = "Enter Database Password Here"
DB_HOST = "Enter Database Hostname Here"
DB_SERVICENAME = "Enter Database Servicename here"
sys_username = getpass.getuser()
BASE_FOLDER = r"folder/path/here"


def create_new_watch_folder(base_folder):
    """Create a new folder with numeric name, starting at 10001, incrementing each run."""
    existing = [f for f in os.listdir(base_folder) if f.isdigit()]
    existing_nums = sorted([int(f) for f in existing])
    global next_num

    if existing_nums:
        next_num = existing_nums[-1] + 1
    else:
        next_num = 10001

    new_folder = os.path.join(base_folder, str(next_num))
    os.makedirs(new_folder, exist_ok=False)
    prompt_user()
    return new_folder

# --- Custom Dialog with Dropdown ---
class CustomInputDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("File Info Input")
        self.result = None
        
        tk.Label(self, text = "Data for patient " +str(next_num)).pack(padx=10,pady=5)

        tk.Label(self, text="Enter the patient's first and last name:").pack(padx=10, pady=5)
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(padx=10, pady=5)

        tk.Label(self, text="Sex of patient:").pack(padx=10, pady=5)
        self.sex_combo = ttk.Combobox(self, values=["Male", "Female"], state="readonly")
        self.sex_combo.current(0)
        self.sex_combo.pack(padx=10, pady=5)
        
        tk.Label(self, text="Race/ethnicity of patient:").pack(padx=10, pady=5)
        self.race_combo = ttk.Combobox(self, values=["American Native", "Asian", "Black", "Hispanic", "Middle Eastern", "Hawaiian or Pacific", "White"], state="readonly")
        self.race_combo.current(0)
        self.race_combo.pack(padx=10, pady=5)
        
        tk.Label(self, text="History of SHD:").pack(padx=10, pady=5)
        self.hiss_combo = ttk.Combobox(self, values=[0, 1], state="readonly")
        self.hiss_combo.current(0)
        self.hiss_combo.pack(padx=10, pady=5)
        
        tk.Label(self, text="History/Presence of AS").pack(padx=10, pady=5)
        self.hisa_combo = ttk.Combobox(self, values=[0, 1, 2, 3], state="readonly")
        self.hisa_combo.current(0)
        self.hisa_combo.pack(padx=10, pady=5)
        
        tk.Label(self, text="Patient date of birth:").pack(pady=5)
        self.date_picker = DateEntry(self, width=12, background='darkblue',foreground='white', borderwidth=2,date_pattern='yyyy-mm-dd')
        self.date_picker.pack(pady=5)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.LEFT, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.grab_set()
        self.name_entry.focus_set()
        self.wait_window()

    def on_ok(self):
        self.result = {
            'name': self.name_entry.get(),
            'sex': self.sex_combo.get(),
            'race': self.race_combo.get(),
            'hiss': self.hiss_combo.get(),
            'hisa': self.hisa_combo.get(),
            'dob': self.date_picker.get_date()
        }
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

# --- Prompt Function ---
def prompt_user():
    dialog = CustomInputDialog(root)
    if dialog.result is None:
        print("User cancelled input.")
        return

    global user_name 
    user_name = dialog.result['name']
    global sex 
    sex = dialog.result['sex']
    global race 
    race = dialog.result['race']
    global hiss 
    hiss = dialog.result['hiss']
    global hisa 
    hisa = dialog.result['hisa']
    global dob 
    dob = dialog.result['dob']
    today = date.today()
    global age 
    age = (today - dob).days / 365.25
    
def insert_into_db(filename,filepath):
    try:
        with oracledb.connect(user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=1521, service_name = DB_SERVICENAME) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO table_name_here 
                        (name, dob, age, sex, race_eth, shd_hist, as_hist, file_path, study_date, usr_info, study_id)
                    VALUES 
                        (:name, :dob, :age, :sex, :race, :hiss, :hisa, :path, SYSTIMESTAMP, :sys_user, :study_id)
                """, {
                    'name': user_name,
                    'dob': dob,
                    'age': age,
                    'sex': sex,
                    'race': race,
                    'hiss': hiss,
                    'hisa': hisa,
                    'path': filepath,
                    'sys_user': sys_username,
                    'study_id': int(filepath[27:32])
                })
            conn.commit()
            print(f"Inserted record for {filename}")
    except oracledb.Error as e:
        print("Oracle error:", e)

# --- File Watcher Class ---
class FileHandler(FileSystemEventHandler):
    def __init__(self, tk_root):
        self.tk_root = tk_root

    def on_created(self, event):
        if event.is_directory:
            return

        filepath = event.src_path
        filename = os.path.basename(filepath)
        
        print(f"[Watchdog] New file detected in {os.path.dirname(filepath)}")
        print(f"    Name: {filename}")

        self.tk_root.after(0, lambda: insert_into_db(filename, filepath))

# --- Main Setup ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # Step 1: Create new folder
    WATCHED_FOLDER = create_new_watch_folder(BASE_FOLDER)
    print(f"[Setup] Created and monitoring folder: {WATCHED_FOLDER}")

    # Step 2: Start watchdog
    event_handler = FileHandler(root)
    observer = Observer()
    observer.schedule(event_handler, path=WATCHED_FOLDER, recursive=False)
    observer.start()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()