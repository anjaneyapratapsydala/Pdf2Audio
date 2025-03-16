from PyPDF2 import PdfReader
from gtts import gTTS
import re

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)         
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)  
    return text.strip()

def convert_pdf_to_audio(pdf_path, output_path, language='en'):
    full_text = []
    with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text.append(clean_text(page_text))
    
    if not full_text:
        raise ValueError("No text could be extracted from the PDF")

    tts = gTTS(text=' '.join(full_text), lang=language, slow=False)
    tts.save(output_path)