from fastapi import FastAPI, APIRouter, File, UploadFile, Form
from pydantic import BaseModel
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import nltk
import docx
import fitz  # PyMuPDF 


nltk.download('punkt')


app = FastAPI()
router = APIRouter()


model_name = "google/pegasus-large"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)


def extract_text_from_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])


def extract_text_from_pdf(file):
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf)):
        page = pdf.load_page(page_num)
        text += page.get_text("text")
    return text


@router.post("/summarize")
async def summarize(length: int = Form(...), text: str = Form(None), file: UploadFile = File(None)):
    extracted_text = ""

   
    if file:
        if file.filename.endswith(".docx"):
            extracted_text = extract_text_from_docx(file.file)
        elif file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file.file)
        else:
            return {"error": "Unsupported file type. Please upload a .docx or .pdf file."}

    
    if text:
        extracted_text = text

    
    if not extracted_text:
        return {"error": "No valid text or file provided."}

 
    inputs = tokenizer(extracted_text, return_tensors="pt", max_length=1024, truncation=True)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=length,  
        min_length=length // 2,  
        length_penalty=1.0,
        num_beams=4,
        early_stopping=True
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

  
    word_count = len(extracted_text.split())
    sentence_count = len(nltk.sent_tokenize(extracted_text))
    summary_word_count = len(summary.split())

    
    stats = f"Input Text - Words: {word_count}, Sentences: {sentence_count}\n"
    stats += f"Summary - Words: {summary_word_count}"

    return {"summary": summary, "stats": stats}

app.include_router(router, prefix="/summarizer", tags=["Text Summarizer"])




