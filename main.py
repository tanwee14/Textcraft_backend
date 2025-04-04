from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.email_gen import router as email_gen_router
from app.spellcheck import router as spellcheck_router
from app.imagetotext import router as imagetoText_router
from app.summarizer import router as summarizer_router
from app.paraphraser import router as paraphraser_router
from app.literature_review import router as literature_review_router
from app.tone_enhancer import router as tone_enhancer_router

app = FastAPI()

# Allow frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust based on your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the email generation router
app.include_router(email_gen_router, prefix="/email", tags=["Email Generation"])

# Include the spell checking router
app.include_router(spellcheck_router, prefix="/spellCheck", tags=["Spell Check"])

# Include the image-to-text router
app.include_router(imagetoText_router, prefix="/image-to-text", tags=["Image To Text"])

app.include_router(summarizer_router, prefix="/summarizer", tags=[" Text Summarizer"])

app.include_router(paraphraser_router, prefix="/paraphraser", tags=["Text Paraphraser"])

app.include_router(literature_review_router, prefix="/lit", tags=["Literature Review Generator"])

app.include_router(tone_enhancer_router, prefix="/tone", tags=["Tone enhancer"])