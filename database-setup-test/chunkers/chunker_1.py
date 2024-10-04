import PyPDF2
import nltk

# Download the punkt tokenizer for sentence splitting
nltk.download('punkt_tab')

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
        return text

def chunk_text(text, chunk_size=5):
    # Split text into sentences
    sentences = nltk.tokenize.sent_tokenize(text)
    
    # Chunk sentences into groups of 5
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    
    return chunks

def chunk_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    chunks = chunk_text(text, chunk_size=5)
    return chunks
