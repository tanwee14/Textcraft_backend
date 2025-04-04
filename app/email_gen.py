from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import json
import requests
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Initialize the API router
router = APIRouter()

# Define a data model using Pydantic for the request body
class GenerateRequest(BaseModel):
    email_length: str
    tone: str
    purpose: str
    recipient_name: str
    sender_name: str
    important_keywords: list

# Function to create a prompt for the email generation
def create_email_prompt(email_length, tone, purpose, recipient_name, sender_name, important_keywords):
    template = f"""
    Write a {email_length} email in a {tone} tone for the purpose of {purpose}.
    Include the following details:
    - Recipient: {recipient_name}
    - Sender: {sender_name}
    - Important Keywords: {', '.join(important_keywords)}

    Ensure the email has a clear subject, greeting, body, and closing.
    Make it professional, concise, and engaging.
    Take the email length into consideration and then generate.
    Only return the email, don't write "here is an email" at the beginning. 
    """
    
    return template.strip()

# Define endpoint to handle requests for email generation
@router.post("/generate")
async def generate_email(request: GenerateRequest):
    url = "https://api.groq.com/openai/v1/chat/completions"  #  Groq API 
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",  
        "Content-Type": "application/json"
    }
    
    prompt = create_email_prompt(
        email_length=request.email_length,
        tone=request.tone,
        purpose=request.purpose,
        recipient_name=request.recipient_name,
        sender_name=request.sender_name,
        important_keywords=request.important_keywords
    )
    print("Sending this data to the model API:", prompt)
    
    data = {
        "model": "llama-3.1-8b-instant",  # Specify the model you want to use
        "messages": [
            {
                "role": "system",
                "content": "You are an email generation assistant."
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
        generated_email = response.json()
        print("Generated Email Response:", generated_email)  
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    
    return {"generated_email": generated_email["choices"][0]["message"]["content"]}  # Extract generated email content
