# utils.py

import docx  # Only DOCX, no PDF

def read_uploaded_file(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith('.txt'):
        return uploaded_file.read().decode("utf-8")
    
    elif file_name.endswith('.docx'):
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        return None
