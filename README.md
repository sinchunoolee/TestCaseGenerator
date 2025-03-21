# **Unit Test Case Generator**

## **1. Introduction**
The **Unit Test Case Generator** is an API built with **FastAPI** that generates test cases for a given piece of code. It leverages **Google's Gemini AI** to analyze the input code and provide structured test cases. Users can either upload a file containing the code or directly input the code as a string.

## **2. Features & Functionality**
### **2.1 Core Features**
- Accepts **code input** via form submission.
- Supports **file uploads** for code submission.
- Generates **test cases** based on best practices.
- Returns structured **JSON response** containing:
  - Number of test cases.
  - Detailed test case descriptions.

### **2.2 API Endpoints**
#### **2.2.1 Root Endpoint**
- **Endpoint:** `GET /`
- **Description:** Returns a welcome message to verify API availability.
- **Response:**
  ```json
  {
    "message": "Welcome to the Test Case Generator API"
  }
  ```

#### **2.2.2 Upload and Generate Test Cases**
- **Endpoint:** `POST /upload-and-generate`
- **Parameters:**
  - `code` (optional, string) - The source code to analyze.
  - `file` (optional, file) - A file containing the source code.
- **Response:**
  ```json
  {
    "num_test_cases": "5 test cases found",
    "test_cases": "1. Test for positive numbers\n2. Test for negative numbers\n..."
  }
  ```

---

## **3. Technical Implementation**
### **3.1 Architecture**
- **FastAPI** is used for the backend.
- **Google Gemini AI** is integrated for test case generation.
- **Python dotenv** loads the API key from an environment file.
- **Pathlib** ensures proper file handling.
- **Uvicorn** runs the server.

### **3.2 Code Breakdown**
#### **3.2.1 Environment Setup**
```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```
Loads the Gemini API key from `.env`.

#### **3.2.2 AI Model Configuration**
```python
import google.generativeai as genai
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config={
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 500,
})
chat_session = model.start_chat()
```
Initializes the AI model and chat session.

#### **3.2.3 Test Case Generation Logic**
```python
def generate_test_cases(code_input: str) -> str:
    prompt = (
        "You are a code testing assistant. Generate test cases for the given code."
        f"\n\n{code_input}\n\n"
        "Provide test cases in a structured format."
    )
    response = chat_session.send_message(prompt)
    return response.text
```
Sends the provided code to Gemini AI for test case generation.

#### **3.2.4 API Endpoint for Upload & Processing**
```python
@app.post("/upload-and-generate")
async def upload_and_generate(code: str = Form(None), file: UploadFile = File(None)):
    if code:
        code_input = code.strip()
    elif file:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            buffer.write(file.file.read())
        with file_path.open("r") as f:
            code_input = f.read()
    else:
        raise HTTPException(status_code=400, detail="No code or file provided")
    
    result = generate_test_cases(code_input)
    num_test_cases = result.split('\n', 1)[0]
    test_cases = result.split('\n', 1)[1] if '\n' in result else result

    return JSONResponse(content={"num_test_cases": num_test_cases.strip(), "test_cases": test_cases.strip()})
```
Handles both **direct code input** and **file uploads**.

---

## **4. Installation & Usage**
### **4.1 Requirements**
- Python 3.8+
- FastAPI
- Uvicorn
- Google Generative AI SDK
- Dotenv for environment variables

### **4.2 Setup Instructions**
1. **Clone the repository**
   ```sh
   git clone <repo_url>
   cd <project_folder>
   ```

2. **Create a virtual environment & activate it**
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**
   ```sh
   pip install fastapi uvicorn python-dotenv google-generativeai
   ```

4. **Set up the API key**
   - Create a `.env` file in the root directory.
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=api_key
     ```

5. **Run the FastAPI server**
   ```sh
   uvicorn main:app --reload
   ```

6. **Access API documentation** at:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## **5. Testing the API**
### **5.1 Using cURL**
#### **Direct Code Input**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/upload-and-generate' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'code=def add(a, b): return a + b'
```

#### **File Upload**
```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/upload-and-generate' \
  -F 'file=@example.py'
```

---

## **6. Potential Improvements**
### **6.1 Enhancements**
- Add **multi-language support** (Python, JavaScript, Java, etc.).
- Implement **test case formatting** in JSON format.
- Introduce **authentication & rate limiting**.
- Improve **error handling** for better debugging.

### **6.2 Possible Extensions**
- Deploy on **AWS/GCP/Azure** for cloud availability.
- Integrate with **CI/CD pipelines** for automated testing.
- Provide a **frontend UI** for better user experience.

---

## **7. Conclusion**
The **Unit Test Case Generator API** provides an automated way to generate test cases for different code inputs using **Google Gemini AI**. It is built with **FastAPI** for efficiency and scalability. Future improvements can make it even more robust by adding **multi-language support, authentication, and cloud deployment.**

