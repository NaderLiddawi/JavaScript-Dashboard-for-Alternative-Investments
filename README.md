HOW TO RUN ON TERMINAL:


1. Open a Terminal

Press Start → type cmd or PowerShell → press Enter.


2. Navigate to the Project Folder

Replace the path with your actual folder:

cd C:\Users\YourName\YourProjectFolder


This folder must contain:

run_dashboard.py

dashboard_generator.py

data_processor.py

requirements.txt


3. Create a Virtual Environment
python -m venv .venv

4. Activate the Virtual Environment
.venv\Scripts\activate


You should now see:

(.venv) C:\Users\...


5. Install Requirements
pip install -r requirements.txt


6. Run the Dashboard Script
python run_dashboard.py


7. Choose Your Excel File

A Windows file picker will appear.

Requirements for the Excel file:

Must be .xlsx or .xls

Must contain a worksheet named exactly:

FRL_Portfolio


8. Dashboard Output

After selecting the file, the script will generate:

alternatives_dashboard.html


Then it will automatically open it in your default browser.


9. Re-running the Dashboard

Whenever you want to update results:

.venv\Scripts\activate
python run_dashboard.py


Pick a new Excel file → new HTML dashboard generated instantly.