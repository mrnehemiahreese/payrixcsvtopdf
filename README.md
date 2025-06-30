# CSV to PDF Report

This repository provides a small Python script to convert CSV files into a simple PDF report. It does not require any third-party dependencies and relies only on the Python standard library.

## Usage

```bash
python3 csv_to_pdf.py your_report.csv
```

By default the output PDF will be written next to the input CSV with the same base name. You can also specify an explicit PDF path:

```bash
python3 csv_to_pdf.py your_report.csv output.pdf
```

The script reads each row of the CSV file and writes the values as text lines in a single-page PDF file.
