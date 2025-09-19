from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from .models import TranscriptRequest, AnalysisResponse
from .services import analyze_transcript
from .utils import save_to_csv

app = FastAPI(
    title="Transcript Analysis API",
    description="An API to analyze call transcripts for summary and sentiment using Groq.",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

dev_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

allowlist = origins + dev_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowlist,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Transcript Analysis API!"}


@app.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_transcript_endpoint(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .txt file.")

    try:
        contents = await file.read()
        transcript = contents.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=500, detail="There was an error reading the file.")
    finally:
        await file.close()

    summary, sentiment = analyze_transcript(transcript)
    if summary is None or sentiment is None:
        raise HTTPException(status_code=500, detail="Failed to analyze transcript due to an internal server error.")

    analysis_result = AnalysisResponse(transcript=transcript, summary=summary, sentiment=sentiment)
    save_to_csv(analysis_result)
    return analysis_result
