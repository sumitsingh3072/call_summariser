from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .models import TranscriptRequest, AnalysisResponse
from .services import analyze_transcript
from .utils import save_to_csv

# Initialize the FastAPI app
app = FastAPI(
    title="Transcript Analysis API",
    description="An API to analyze call transcripts for summary and sentiment using Groq.",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the frontend (running on a different domain/port) to communicate with the backend.
origins = [
    "http://localhost",
    "http://localhost:3000", # Default port for React development server
]

# Add common dev server origins (Vite default port 5173) and allow 127.0.0.1.
# For local development it's often convenient to allow these origins. In
# production you should restrict CORS to specific trusted origins only.
dev_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Merge the lists and add a permissive wildcard for quick local development.
# NOTE: Using ['*'] is convenient for dev but not recommended for production.
allowlist = origins + dev_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowlist,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (GET, POST, etc.)
    allow_headers=["*"], # Allow all headers
)


@app.get("/", tags=["Root"])
async def read_root():
    """
    Root endpoint to check if the API is running.
    """
    return {"message": "Welcome to the Transcript Analysis API!"}


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_transcript_endpoint(file: UploadFile = File(...)):
    """
    Analyzes a transcript from an uploaded .txt file, saves the result, 
    and returns the analysis.
    """
    # 1. Validate the file type
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload a .txt file."
        )

    # 2. Read the content of the file
    try:
        contents = await file.read()
        transcript = contents.decode("utf-8")
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="There was an error reading the file."
        )
    finally:
        await file.close()

    # 3. Call the service function to perform the analysis
    summary, sentiment = analyze_transcript(transcript)
    
    if summary is None or sentiment is None:
        raise HTTPException(
            status_code=500, 
            detail="Failed to analyze transcript due to an internal server error."
        )
        
    # 4. Create the response object
    analysis_result = AnalysisResponse(
        transcript=transcript,
        summary=summary,
        sentiment=sentiment
    )
    # Save the result to a CSV file
    save_to_csv(analysis_result)
    
    # Return the analysis result
    return analysis_result
