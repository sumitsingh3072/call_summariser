from pydantic import BaseModel

class TranscriptRequest(BaseModel):
    """
    Pydantic model for the incoming request.
    It expects a single field 'transcript' which is a string.
    """
    transcript: str

class AnalysisResponse(BaseModel):
    """
    Pydantic model for the outgoing response.
    It defines the structure of the analysis result.
    """
    transcript: str
    summary: str
    sentiment: str
