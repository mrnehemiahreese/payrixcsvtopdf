import argparse
import csv
import os
import re
from typing import List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


def csv_to_table_data(path: str) -> List[List[str]]:
    """Load CSV file and return a list of rows."""
    with open(path, newline="") as f:
        reader = csv.reader(f)
        return [row for row in reader]


def _is_number(val: str) -> bool:
    """Return True if the string looks like a number."""
    try:
        float(re.sub(r"[,$]", "", val))
        return True
    except ValueError:
        return False


def create_pdf(rows: List[List[str]], output_path: str) -> None:
    """Create a PDF file from the given table rows with Excel-like styling."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    if not rows:
        rows = [[]]

    # Normalize row lengths
    num_cols = max(len(r) for r in rows)
    for r in rows:
        if len(r) < num_cols:
            r.extend([""] * (num_cols - len(r)))

    # Calculate column widths based on content length
    col_lens = [max(len(row[i]) for row in rows) for i in range(num_cols)]
    total = sum(col_lens) or num_cols
    col_widths = [doc.width * (l / total) for l in col_lens]

    table = Table(rows, colWidths=col_widths, repeatRows=1)

    style = TableStyle(
        [
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 10),
            ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]
    )

    # Alternate row background colors for readability
    for row_num in range(1, len(rows)):
        if row_num % 2 == 0:
            style.add("BACKGROUND", (0, row_num), (-1, row_num), colors.whitesmoke)

    # Right-align numeric columns
    for col in range(num_cols):
        if all(
            _is_number(rows[row][col]) for row in range(1, len(rows)) if rows[row][col]
        ):
            style.add("ALIGN", (col, 1), (col, -1), "RIGHT")

    table.setStyle(style)
    doc.build([table])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a simple PDF report"
    )
    parser.add_argument("csvfile", help="Path to the CSV file")
    parser.add_argument(
        "pdffile", nargs="?", help="Path to output PDF (default: same name with .pdf)"
    )
    args = parser.parse_args()
    csv_path = args.csvfile
    pdf_path = args.pdffile or os.path.splitext(csv_path)[0] + ".pdf"
    rows = csv_to_table_data(csv_path)
    create_pdf(rows, pdf_path)
    print(f"Created {pdf_path}")


if __name__ == "__main__":
    main()
