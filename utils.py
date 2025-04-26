# utils.py

import fitz  # PyMuPDF for PDFs
import docx  # python-docx for DOCX files

def read_uploaded_file(uploaded_file):
    """
    Reads uploaded file (txt, pdf, docx) and returns extracted text.
    """
    file_name = uploaded_file.name.lower()

    if file_name.endswith('.txt'):
        return uploaded_file.read().decode("utf-8")
    
    elif file_name.endswith('.pdf'):
        # Read PDF using PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    
    elif file_name.endswith('.docx'):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        return None

def clean_text(text: str) -> str:
    """
    Basic text cleaning (remove line breaks, trim spaces).
    """
    return text.replace("\n", " ").strip()
