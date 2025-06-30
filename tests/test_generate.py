import subprocess
import sys
from pathlib import Path


def test_pdf_generated(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    csv_path = repo_root / "Disbursement Report - p1_dbm_685dc4a75fc86317cb4b90e.csv"
    pdf_path = tmp_path / "out.pdf"
    subprocess.run([sys.executable, str(repo_root / "csv_to_pdf.py"), str(csv_path), str(pdf_path)], check=True)
    assert pdf_path.is_file() and pdf_path.stat().st_size > 0
