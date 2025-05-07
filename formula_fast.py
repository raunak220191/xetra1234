import re
from typing import List

from langchain.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPDFLoader
from langchain.schema import Document

# A simple heuristic for formula‐like lines
FORMULA_PATTERN = re.compile(
    r"(\\frac\{.+?\}\{.+?\}|∑|√|÷|×|/|\^[0-9]+|_[0-9]+)"
)

def _explain_formula(expr: str) -> str:
    """Turn a little bit of LaTeX or symbol soup into plain English."""
    t = expr
    t = re.sub(r"\\frac\{(.+?)\}\{(.+?)\}", r"(\1) divided by (\2)", t)
    t = t.replace("/", " divided by ")
    t = t.replace("^", " to the power ")
    t = t.replace("_", " sub ")
    t = t.replace("∑", "sum ")
    t = t.replace("√", "square root ")
    t = t.replace("×", " times ")
    t = t.replace("÷", " divided by ")
    # strip remaining backslashes/braces
    t = re.sub(r"[\\\{\}]", "", t)
    return t.strip()

def load_and_annotate(path: str) -> List[Document]:
    """
    Load a DOCX or PDF via LangChain's Unstructured loaders (fast strategy),
    detect formula‐like lines, and inject "Formula: ..." explanations inline.
    Returns a list of Documents.
    """
    path_lower = path.lower()
    if path_lower.endswith(".docx"):
        loader = UnstructuredWordDocumentLoader(
            path,
            unstructured_kwargs={"strategy": "fast"}
        )
    elif path_lower.endswith(".pdf"):
        loader = UnstructuredPDFLoader(
            path,
            unstructured_kwargs={"strategy": "fast"}
        )
    else:
        raise ValueError("Only .docx and .pdf supported")

    raw_docs = loader.load()  # List[Document]
    out_docs: List[Document] = []

    for doc in raw_docs:
        annotated_lines = []
        for line in doc.page_content.splitlines():
            line = line.strip()
            if not line:
                continue
            if FORMULA_PATTERN.search(line):
                annotated_lines.append(f"Formula: {_explain_formula(line)}")
            else:
                annotated_lines.append(line)
        new_content = "\n".join(annotated_lines)
        out_docs.append(Document(page_content=new_content, metadata=doc.metadata))

    return out_docs
