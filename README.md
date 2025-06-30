# CSV to PDF Report

This repository provides a small Python script to convert CSV files into a simple PDF report using the [ReportLab](https://www.reportlab.com/) library.

## Installation

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 csv_to_pdf.py your_report.csv
```

By default the output PDF will be written next to the input CSV with the same base name. You can also specify an explicit PDF path:

```bash
python3 csv_to_pdf.py your_report.csv output.pdf
```

The script reads your CSV file and renders the rows in a table inside the generated PDF document.
