import os
import json
from groq import Groq
from dotenv import load_dotenv
from typing import Tuple, Optional

load_dotenv()


def analyze_transcript(transcript: str) -> Tuple[Optional[str], Optional[str]]:
    """Analyzes a transcript using the Groq API to get a summary and sentiment.

    Returns a tuple (summary, sentiment) or (None, None) on error.
    """
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        if not os.environ.get("GROQ_API_KEY"):
            print("Error: GROQ_API_KEY not found in environment variables.")
            return None, None

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert conversation analyst. "
                        "Your task is to analyze the provided customer call transcript. "
                        "Please provide a concise summary of the conversation in 2-3 sentences. "
                        "Then, determine the customer's sentiment (Positive, Negative, or Neutral). "
                        "Return your analysis in a structured JSON format with two keys: 'summary' and 'sentiment'."
                    ),
                },
                {"role": "user", "content": transcript},
            ],
            model="openai/gpt-oss-20b",
            response_format={"type": "json_object"},
        )

        response_content = chat_completion.choices[0].message.content
        if not response_content:
            return None, None
        analysis_result = json.loads(response_content)

        summary = analysis_result.get("summary", "No summary provided.")
        sentiment = analysis_result.get("sentiment", "No sentiment provided.")
        return summary, sentiment

    except Exception as e:
        print(f"An error occurred during transcript analysis: {e}")
        return None, None
