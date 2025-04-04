# from fastapi import FastAPI, Form, APIRouter
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# import google.generativeai as genai
# import os
# from PIL import Image
# import requests
# from io import BytesIO
# from fastapi.middleware.cors import CORSMiddleware

# # Initialize FastAPI app and Router
# app = FastAPI()
# router = APIRouter()

# # CORS middleware to allow communication with React frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins temporarily for debugging
#     allow_credentials=True,
#     allow_methods=["*"],  # Allow all HTTP methods
#     allow_headers=["*"],  # Allow all headers
# )

# # Set your Google API key for the Generative AI model
# os.environ["GOOGLE_API_KEY"] = "AIzaSyAzwFSGUGpUtGv-JOKah4UBER5gKUR5GV8"
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# # Use the Generative Model
# model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# # Pydantic Model to handle the form data from the frontend
# class ImageQueryInput(BaseModel):
#     image_url: str
#     query: str

# # Function to convert image to text
# def image_to_text(img):
#     response = model.generate_content(img)
#     return response.text

# # Function to generate content based on image and query
# def image_and_query(img, query):
#     response = model.generate_content([query, img])
#     return response.text

# # Endpoint to handle image URL and query input from frontend
# @router.post("/text-to-image")
# async def upload_image(image_url: str = Form(...), query: str = Form(...)):
#     try:
#         # Download the image from the URL
#         response = requests.get(image_url)
#         img = Image.open(BytesIO(response.content))  # Open the image in binary mode

#         # Extract details from image
#         extracted_details = image_to_text(img)

#         # Generate content based on image and query
#         generated_details = image_and_query(img, query)

#         # Return response with extracted and generated details
#         return JSONResponse(content={
#             "extracted_details": extracted_details,
#             "generated_details": generated_details
#         })
#     except Exception as e:
#         return JSONResponse(content={"error": str(e)}, status_code=500)

# # Include the router in the FastAPI app
# app.include_router(router, prefix="/image-to-text", tags=["Image To Text"])

from fastapi import FastAPI, Form, APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
import os
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app and Router
app = FastAPI()
router = APIRouter()

# CORS middleware to allow communication with React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily for debugging
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Set your Google API key for the Generative AI model
os.environ["GOOGLE_API_KEY"] = "AIzaSyAzwFSGUGpUtGv-JOKah4UBER5gKUR5GV8"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Use the Generative Model
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

# Pydantic Model to handle the form data from the frontend
class ImageQueryInput(BaseModel):
    image_url: str
    query: str


def image_to_text(img):
    try:
      
        response = model.generate_content(["Describe the image", img])
        return response.text
    except Exception as e:
        raise ValueError(f"Error generating text from image: {e}")


def image_and_query(img, query):
    try:
        response = model.generate_content([query, img])
        return response.text
    except Exception as e:
        raise ValueError(f"Error generating text from image and query: {e}")


@router.post("/text-to-image")
async def upload_image(image_url: str = Form(...), query: str = Form(...)):
    try:
        # Download the image from the URL
        response = requests.get(image_url)
        if response.status_code != 200:
            raise ValueError("Failed to fetch the image. Ensure the URL is correct.")
        
        try:
            img = Image.open(BytesIO(response.content))  # Open the image in binary mode
        except UnidentifiedImageError:
            raise ValueError("The provided URL does not point to a valid image.")


        extracted_details = image_to_text(img)


        generated_details = image_and_query(img, query)


        return JSONResponse(content={
            "extracted_details": extracted_details,
            "generated_details": generated_details
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


app.include_router(router, prefix="/image-to-text", tags=["Image To Text"])

