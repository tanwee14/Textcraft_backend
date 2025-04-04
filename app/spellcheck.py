from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # Import Pydantic BaseModel
import language_tool_python


app = FastAPI()
router = APIRouter()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a LanguageTool object f
tool = language_tool_python.LanguageTool('en-US')


class SpellCheckRequest(BaseModel):
    text: str


@router.post("/correct-text")
async def spell_check(request: SpellCheckRequest):  
    text = request.text  
    print(text)
    errors = tool.check(text)

 
    corrected_text = tool.correct(text)
    print(corrected_text)

    grammar_corrections = []
    for match in errors:
        grammar_corrections.append({
            "error": text[match.offset:match.offset + match.errorLength],
            "suggestions": match.replacements,
            "message": match.message
        })

    print(grammar_corrections)    


    return {
        "corrected_text": corrected_text,
        "grammar_corrections": grammar_corrections
    }

app.include_router(router, prefix="/spellCheck", tags=["Image To Text"])
