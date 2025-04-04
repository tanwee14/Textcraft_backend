from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import json
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from the .env file
load_dotenv()

app = FastAPI()
router = APIRouter()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily for debugging
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Define a data model for the request body
class ToneEnhanceRequest(BaseModel):
    text: str
    tone: str

class RephraseRequest(BaseModel):
    text: str

# Function to create a prompt for tone enhancement
def create_tone_enhance_prompt(text, tone):
    template = f"""
    Enhance the following text to have a {tone} tone:
    Text: "{text}"
    
    Make sure the text is engaging, appropriate to the tone, and maintains the original message.
    Only give rephrased text don't give information about what you did to rephrase it.
    Don't write Here is a revised version or anything like that. Only return rephrased text.
    """
    return template.strip()

# Function to create a prompt for rephrasing the text
def create_rephrase_prompt(text):
    template = f"""
    Rephrase the following text to make it more fluent, clear, and concise:
    Text: "{text}"
    
    Ensure that the meaning of the original text remains the same.
    Only give rephrased text don't give information about what you did to rephrase it.
    Don't write Here is a revised version or anything like that. Only return rephrased text.
    """
    return template.strip()

# Define endpoint for tone enhancement
@router.post("/enhance_tone")
async def enhance_tone(request: ToneEnhanceRequest):
    url = "https://api.groq.com/openai/v1/chat/completions"  # Groq API endpoint
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",  # Use the API key from the .env file
        "Content-Type": "application/json"
    }

    prompt = create_tone_enhance_prompt(request.text, request.tone)
    data = {
        "model": "llama-3.1-8b-instant",  # Specify the Groq model you want to use
        "messages": [
            {
                "role": "system",
                "content": "You are a tone enhancement assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4096
    }

    try:
        response = requests.post(url, headers=headers, json=data)  # Use json parameter to send data
        response.raise_for_status()
        enhanced_text = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

    return {"enhanced_text": enhanced_text["choices"][0]["message"]["content"]}  # Extract enhanced text content

# Define endpoint for rephrasing text
@router.post("/rephrase")
async def rephrase_text(request: RephraseRequest):
    url = "https://api.groq.com/openai/v1/chat/completions"  # Groq API endpoint
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",  # Use the API key from the .env file
        "Content-Type": "application/json"
    }

    prompt = create_rephrase_prompt(request.text)
    data = {
        "model": "llama-3.1-8b-instant",  # Specify the Groq model you want to use
        "messages": [
            {
                "role": "system",
                "content": "You are a rephrasing assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 4096
    }

    try:
        response = requests.post(url, headers=headers, json=data)  # Use json parameter to send data
        response.raise_for_status()
        rephrased_text = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

    return {"rephrased_text": rephrased_text["choices"][0]["message"]["content"]}  # Extract rephrased text content

app.include_router(router, prefix="/tone", tags=["Tone enhancer"])
