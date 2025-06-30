import argparse
import csv
import os
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def csv_to_table_data(path: str) -> List[List[str]]:
    """Load CSV file and return a list of rows."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return [row for row in reader]


def create_pdf(rows: List[List[str]], output_path: str) -> None:
    """Create a PDF file from the given table rows."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    para_style = styles["Normal"]
    if not rows:
        rows = [[]]
    # Determine the maximum column count so every row has the same length
    num_cols = max(len(r) for r in rows)
    padded_rows = [r + [""] * (num_cols - len(r)) for r in rows]
    wrapped_rows = [
        [Paragraph(cell, para_style) for cell in row]
        for row in padded_rows
    ]
    table = Table(wrapped_rows, colWidths=[doc.width / num_cols] * num_cols, repeatRows=1)
    style = TableStyle(
        [
            ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ]
    )
    table.setStyle(style)
    doc.build([table])


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a CSV file to a simple PDF report")
    parser.add_argument("csvfile", help="Path to the CSV file")
    parser.add_argument("pdffile", nargs="?", help="Path to output PDF (default: same name with .pdf)")
    args = parser.parse_args()
    csv_path = args.csvfile
    pdf_path = args.pdffile or os.path.splitext(csv_path)[0] + ".pdf"
    rows = csv_to_table_data(csv_path)
    create_pdf(rows, pdf_path)
    print(f"Created {pdf_path}")


if __name__ == "__main__":
    main()
