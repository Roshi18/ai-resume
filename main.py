# main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure you have your key in .env

app = FastAPI(title="AI Resume Analyzer & Question Generator")

@app.post("/analyze_resume/")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.endswith(".pdf"):
            return JSONResponse(
                status_code=400,
                content={"error": "Only PDF files are allowed."}
            )

        # Read PDF content
        contents = await file.read()
        pdf = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()

        if not text.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "The PDF appears to be empty or unreadable."}
            )

        # Prepare prompt for OpenAI
        prompt = f"Analyze this resume and generate interview questions:\n{text}"

        # Call OpenAI API using the new Chat Completions
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response.choices[0].message.content

        return {"questions": result_text}

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Something went wrong: {str(e)}"}
        )

@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer is running! Use /analyze_resume/ to POST your resume PDF."}
