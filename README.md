# JavaScript Dashboard for Alternative Investments

## Overview

This project generates an interactive analytics dashboard from portfolio data stored in Excel.  
It processes investment records, calculates performance metrics, and produces a self-contained HTML dashboard viewable in any web browser.

The system is designed primarily for Windows users and requires no coding to operate.

---

## What the System Produces

- Portfolio composition by asset class  
- Quarterly performance metrics  
- NAV and return trends  
- Income, contributions, and distributions  
- Interactive charts and tables  

Final output:

`alternatives_dashboard.html` – a complete interactive dashboard file.

---

## Technologies Used

This project combines three main technologies:

### Python  
Used for:
- Reading Excel data  
- Cleaning and processing financial records  
- Calculating returns and metrics  
- Generating the final dashboard file  

### HTML  
Provides:
- Page structure  
- Layout of dashboard tabs  
- Tables and content containers  

### JavaScript  
Handles:
- Interactive charts (via Chart.js)  
- Navigation between dashboard sections  
- Data visualization and formatting  

---

## Repository Files and Their Roles

### `run_dashboard.py` – User Interface Script

**Purpose:**  
Main entry point for end users.

**What it does:**
- Opens a native Windows file-selection dialog  
- Lets the user choose an Excel workbook  
- Calls the data processor and dashboard generator  
- Opens the final dashboard in the browser  

This file provides the “one-click” experience.

---

### `data_processor.py` – Data Analytics Engine

**Purpose:**  
Performs all data loading and financial calculations.

**Key functions:**

- Loads portfolio data from Excel  
- Identifies “Alternatives” investments  
- Calculates:
  - Returns  
  - NAV changes  
  - Income yields  
  - Asset class summaries  
- Produces structured JSON used by the dashboard  

**Core business logic lives here.**

---

### `dashboard_generator.py` – HTML Builder

**Purpose:**  
Transforms processed data into a working dashboard.

**What it does:**

- Takes JSON output from `data_processor.py`  
- Embeds data into an HTML/JavaScript template  
- Creates charts, tables, and metric cards  
- Writes the final file:

`alternatives_dashboard.html`

This file bridges Python analytics with front-end visualization.

---

### `alternatives_dashboard.html` – Final Output

**Purpose:**  
The finished product users interact with.

**Contains:**

- Embedded portfolio data  
- Interactive JavaScript charts  
- Performance tables  
- Multiple dashboard views  

No server is required—just open in a browser.

---

### `FRL_Portfolio - Interview Use.xlsx`

**Purpose:**  
Sample input dataset.

**Requirements:**

- Must contain a worksheet named:  
  `FRL_Portfolio`
- Expected fields include:
  - Date  
  - Asset_Class  
  - Beg_NAV  
  - End_NAV  
  - Contributions  
  - Distributions  
  - Net_Investment_Income  

Any Excel file with this structure can be used.

---

### `Manually Verified Dashboard Metrics.xlsx`

**Purpose:**  
Reference file used to validate that dashboard calculations are correct via Pivot Table.

---

### `requirements.txt`

Lists required Python libraries:
- pandas, numpy, openpyxl


________________________________________________________________________



## HOW TO RUN ON TERMINAL (Windows)

### 1. Open a Terminal
Press **Start → type `cmd` or `PowerShell` → press Enter.**

---

### 2. Navigate to the Project Folder

Replace the path with your actual project location:

```
cd C:\Users\YourName\YourProjectFolder
```

This folder must contain the following files:

- `run_dashboard.py`
- `dashboard_generator.py`
- `data_processor.py`
- `requirements.txt`

---

### 3. Create a Virtual Environment

Run:

```
python -m venv .venv
```

---

### 4. Activate the Virtual Environment

```
.venv\Scripts\activate
```

You should now see something like this at the start of your terminal prompt:

```
(.venv) C:\Users\...
```

This means the virtual environment is active.

---

### 5. Install Required Packages

Install all dependencies:

```
pip install -r requirements.txt
```

---

### 6. Run the Dashboard Script

Start the dashboard generator:

```
python run_dashboard.py
```

---

### 7. Choose Your Excel File

A Windows file picker will automatically appear.

#### Requirements for the Excel file:

- Must be `.xlsx` or `.xls`
- Must contain a worksheet named exactly:

```
FRL_Portfolio
```

---

### 8. Dashboard Output

After selecting the file, the script will generate:

```
alternatives_dashboard.html
```

The dashboard will then **automatically open in your default web browser.**

---

## Re-running the Dashboard

Whenever you want to update results:

Activate the environment and run again:

```
.venv\Scripts\activate
python run_dashboard.py
```

Pick a new Excel file → a new HTML dashboard will be generated instantly.
