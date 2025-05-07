import re
import tempfile

from docx import Document
import pdfplumber

# Heuristic regex for “formula‐like” content:
FORMULA_PATTERN = re.compile(
    r"([∑∫√∆≈≠≤≥×÷]|\\frac|[A-Za-z0-9]+\s*[/^_]\s*[A-Za-z0-9]+)"
)

def convert_doc_to_text(file_bytes: bytes, suffix: str) -> str:
    """
    Read through a .docx or .pdf (bytes), detect formula lines,
    and return one big text with "Formula: ..." injected inline.
    """
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        path = tmp.name

    if suffix.lower() == ".docx":
        return _process_docx(path)
    elif suffix.lower() == ".pdf":
        return _process_pdf(path)
    else:
        raise ValueError("Unsupported suffix")

def _explain_formula(expr: str) -> str:
    """Very basic symbol→word replacements."""
    t = expr
    t = re.sub(r"\\frac\{(.+?)\}\{(.+?)\}", r"(\1) divided by (\2)", t)
    t = t.replace("/", " divided by ")
    t = t.replace("^", " to the power ")
    t = t.replace("_", " sub ")
    t = t.replace("∑", "sum ")
    t = t.replace("√", "square root ")
    t = t.replace("×", " times ")
    t = t.replace("÷", " divided by ")
    # Strip leftover braces/slashes
    t = re.sub(r"[{}\\]", "", t)
    return t.strip()

def _process_docx(path: str) -> str:
    parts = []
    doc = Document(path)
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if FORMULA_PATTERN.search(text):
            parts.append(f"Formula: {_explain_formula(text)}")
        else:
            parts.append(text)
    return "\n\n".join(parts)

def _process_pdf(path: str) -> str:
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                if FORMULA_PATTERN.search(line):
                    parts.append(f"Formula: {_explain_formula(line)}")
                else:
                    parts.append(line)
    return "\n\n".join(parts)
