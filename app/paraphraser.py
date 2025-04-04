from fastapi import FastAPI, Request,APIRouter
from pydantic import BaseModel
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from typing import List
import nltk

nltk.download('punkt_tab')


router=APIRouter()

# Load the Pegasus paraphrase model and tokenizer
model_name = "tuner007/pegasus_paraphrase"
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name)

app = FastAPI()

# Define a request model for input data
class ParaphraseRequest(BaseModel):
    text: str
    num_paraphrases: int = 5
    num_beams: int = 10

# Paraphrasing function
def paraphrase_text(text: str, num_return_sequences: int = 5, num_beams: int = 10) -> List[str]:
    inputs = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    paraphrase_ids = model.generate(
        inputs['input_ids'],
        num_beams=num_beams,
        num_return_sequences=num_return_sequences,
        temperature=1.5,
        max_length=60
    )
    paraphrases = [tokenizer.decode(p, skip_special_tokens=True) for p in paraphrase_ids]
    return paraphrases

# FastAPI route to paraphrase text
@router.post("/paraphrase")
async def paraphrase(request: ParaphraseRequest):
    paraphrases = paraphrase_text(request.text, request.num_paraphrases, request.num_beams)
    return {"paraphrases": paraphrases}

# Run with: uvicorn main:app --reload
app.include_router(router, prefix="/paraphraser", tags=["Text Paraphraser"])