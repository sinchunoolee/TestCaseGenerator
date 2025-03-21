from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Configure API key for Generative AI


api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Check Your API - Something Seems Wrong!!!")

genai.configure(api_key=api_key)

# Configure model generation settings
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Start chat session for the model
chat_session = model.start_chat()

# Initialize FastAPI app
app = FastAPI()

# Ensure the uploads directory exists
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Test Case Generator API"}

# Function to generate test cases using the AI model
def generate_test_cases(code_input: str) -> str:
    prompt = (
        "You are a code testing assistant with knowledge of all programming languages. "
        "Please generate test cases for the following code according to the latest industry standards. "
        "Generate the test cases with numbers as first test case and what does it do using minimal text. "
        "Your output will be displayed in a test case output window, so generate accordingly.\n\n"
        f"{code_input}\n\n"
        "Provide the number of test cases possible followed by the test cases."
    )
    response = chat_session.send_message(prompt)
    return response.text

# API to handle file uploads and direct code input
@app.post("/upload-and-generate")
async def upload_and_generate(
    code: str = Form(None), 
    file: UploadFile = File(None)
):
    # Check if code is provided in the text input
    if code and code.strip():
        code_input = code.strip()
    elif file:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            buffer.write(file.file.read())

        with file_path.open("r") as f:
            code_input = f.read()
    else:
        raise HTTPException(status_code=400, detail="No code or file provided")

    # Generate test cases
    result = generate_test_cases(code_input)

    # Split response into number of test cases and test case details
    num_test_cases = result.split('\n', 1)[0]
    test_cases = result.split('\n', 1)[1] if '\n' in result else result

    return JSONResponse(content={
        "num_test_cases": num_test_cases.strip(),
        "test_cases": test_cases.strip()
    })

