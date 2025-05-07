import re
import tempfile
from typing import List

from unstructured.partition.auto import partition
from unstructured.documents.elements import Element
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


PDF = ".pdf"
DOCX = ".docx"

class UnstructuredFormulaLoader:
    """
    A LangChain‐style loader that uses Unstructured to read DOCX or PDF,
    detects equation elements, and emits plain‑English formula lines.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> List[Document]:
        # detect by suffix
        suffix = self.file_path.lower().split('.')[-1]
        if suffix == PDF.lstrip('.'):
            text = self._process_with_unstructured(self.file_path)
        elif suffix == DOCX.lstrip('.'):
            text = self._process_with_unstructured(self.file_path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")
        return [Document(page_content=text, metadata={"source": self.file_path})]

    def _process_with_unstructured(self, path: str) -> str:
        elements = partition(filename=path)
        parts: List[str] = []
        for el in elements:
            txt = getattr(el, "text", "") or ""
            txt = txt.strip()
            if not txt:
                continue

            is_math = (
                getattr(el, "category", None) == "math" or
                el.__class__.__name__.lower().startswith("equation")
            )
            if is_math:
                # strip LaTeX delimiters if present
                latex = re.sub(r"^\$+|\\begin\{.*?\}|\\end\{.*?\}|\$+$", "", txt)
                parts.append("Formula: " + _latex_to_text(latex))
            else:
                parts.append(txt)

        # preserve paragraph breaks
        return "\n\n".join(parts)

def _latex_to_text(latex: str) -> str:
    # fractions
    latex = re.sub(r"\\frac\{(.+?)\}\{(.+?)\}", r"(\1) divided by (\2)", latex)
    # summations
    latex = re.sub(
        r"\\sum_{(.+?)=(.+?)}\^\{(.+?)\}",
        r"Summation from \1 = \2 to \3 of",
        latex
    )
    # subscripts
    latex = re.sub(r"([A-Za-z0-9])_\{(.+?)\}", r"\1 sub \2", latex)
    # superscripts
    latex = re.sub(r"([A-Za-z0-9])\^\{(.+?)\}", r"\1 to the power \2", latex)
    # clean up leftovers
    return latex.replace("\\", "").replace("{", "").replace("}", "").strip()
