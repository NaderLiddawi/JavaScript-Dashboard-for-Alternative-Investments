"""
Runner Script for Dashboard

Behavior on Windows:
- User double-clicks this script (or the packaged EXE, which I developed but did not include in the Resent Email).
- A native Windows "Open File" dialog appears (via PowerShell + .NET).
- User selects an Excel workbook. Note that Worksheet name must be: FRL_Portfolio
- The script generates 'alternatives_dashboard.html'.
- The dashboard opens automatically in the default browser.

Behavior on non-Windows (like Linux or Mac):
- Falls back to asking for an Excel path in the console.
"""

import os
import sys
import webbrowser
import subprocess

from dashboard_generator import main  # main(file_path=..., output_path=...)


def select_excel_file_windows() -> str:
    """
    Use Windows PowerShell + .NET WinForms to show a native
    file-open dialog and return the selected Excel file path

    """
    ps_script = r'''
Add-Type -AssemblyName System.Windows.Forms | Out-Null
$ofd = New-Object System.Windows.Forms.OpenFileDialog
$ofd.Filter = "Excel files (*.xlsx;*.xls)|*.xlsx;*.xls|All files (*.*)|*.*"
$ofd.Title = "Select portfolio Excel file"
$null = $ofd.ShowDialog()
$ofd.FileName
'''

    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_script],
        capture_output=True,
        text=True
    )

    if completed.returncode != 0:
        raise RuntimeError(
            f"PowerShell dialog failed: {completed.stderr.strip()}"
        )

    file_path = completed.stdout.strip()

    if not file_path:
        print("No file selected. Exiting.")
        sys.exit(1)

    if not os.path.isfile(file_path):
        raise FileNotFoundError(
            f"Selected file does not exist:\n    {file_path}"
        )

    return file_path


def select_excel_file() -> str:
    """

    - On Windows (nt): use native file dialog via PowerShell.
    - On other Operating Systems (like Linux or Mac): fall back to console input.
    """
    if os.name == "nt":
        return select_excel_file_windows()
    else:
        print("\nNon-Windows OS detected.")
        print("Please enter the full path to the portfolio Excel file.")
        excel_path = input("Excel file path: ").strip()
        if not excel_path:
            print("No file provided. Exiting.")
            sys.exit(1)
        if not os.path.isfile(excel_path):
            raise FileNotFoundError(
                f"Could not find file:\n    {excel_path}"
            )
        return excel_path


if __name__ == "__main__":
    try:
        print("\nStarting Fortitude Re Alternatives Portfolio Dashboard Generator...")
        print("-" * 60)

        # 1. Let the user select the Excel file (dialog on Windows)
        excel_path = select_excel_file()
        print(f"\nSelected file:\n    {excel_path}")

        # 2. Generate the dashboard
        output_html = "alternatives_dashboard.html"

        # This main function call is from dashboard_generator, which then calls data_processor
        main(file_path=excel_path, output_path=output_html)

        # 3. Open the HTML dashboard in the default browser
        html_full_path = os.path.abspath(output_html)
        print(f"\nSuccess! Opening '{html_full_path}' in your browser...")
        webbrowser.open(f"file://{html_full_path}")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("\nPlease check the error message above and try again.")
        sys.exit(1)
