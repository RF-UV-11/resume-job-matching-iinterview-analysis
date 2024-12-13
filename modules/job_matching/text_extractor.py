import os
from PyPDF2 import PdfReader
from docx import Document

def extract_text_from_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("Unsupported file type. Only .pdf, .docx, and .txt are allowed.")

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
