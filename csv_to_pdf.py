import argparse
import csv
import os
from typing import List


def csv_to_lines(path: str) -> List[str]:
    """Read CSV file and return a list of formatted lines."""
    lines = []
    with open(path, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                lines.append("    ".join(row))
            else:
                lines.append("")
    return lines


def create_pdf(lines: List[str], output_path: str) -> None:
    """Create a simple PDF file containing the given lines."""
    # Build the content stream for a single page
    x0, y0 = 72, 720  # starting position
    leading = 14
    text_lines = []
    text_lines.append("BT")
    text_lines.append("/F1 12 Tf")
    text_lines.append(f"{x0} {y0} Td")
    text_lines.append(f"{leading} TL")
    for line in lines:
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        text_lines.append(f"({safe}) Tj")
        text_lines.append("T*")
    text_lines.append("ET")
    content = "\n".join(text_lines)

    objects = []
    # 1: Catalog
    objects.append("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    # 2: Pages
    objects.append("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    # 3: Page
    objects.append(
        "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n"
    )
    # 4: Content stream
    objects.append(
        f"4 0 obj\n<< /Length {len(content)} >>\nstream\n{content}\nendstream\nendobj\n"
    )
    # 5: Font
    objects.append(
        "5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
    )

    offsets = []
    pdf_parts = ["%PDF-1.4\n"]
    for obj in objects:
        offsets.append(sum(len(part) for part in pdf_parts))
        pdf_parts.append(obj)

    xref_offset = sum(len(part) for part in pdf_parts)
    xref_lines = [f"xref\n0 {len(objects)+1}\n", "0000000000 65535 f \n"]
    for off in offsets:
        xref_lines.append(f"{off:010d} 00000 n \n")
    xref = "".join(xref_lines)
    trailer = f"trailer\n<< /Root 1 0 R /Size {len(objects)+1} >>\nstartxref\n{xref_offset}\n%%EOF"
    pdf_content = "".join(pdf_parts) + xref + trailer

    with open(output_path, "wb") as f:
        f.write(pdf_content.encode("latin-1"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a CSV file to a simple PDF report")
    parser.add_argument("csvfile", help="Path to the CSV file")
    parser.add_argument("pdffile", nargs="?", help="Path to output PDF (default: same name with .pdf)")
    args = parser.parse_args()
    csv_path = args.csvfile
    pdf_path = args.pdffile or os.path.splitext(csv_path)[0] + ".pdf"
    lines = csv_to_lines(csv_path)
    create_pdf(lines, pdf_path)
    print(f"Created {pdf_path}")


if __name__ == "__main__":
    main()
