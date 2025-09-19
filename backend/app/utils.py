import csv
import os
from .models import AnalysisResponse

def save_to_csv(analysis_result: AnalysisResponse, filename="call_analysis.csv"):
    """
    Saves the analysis result to a CSV file.

    Args:
        analysis_result (AnalysisResponse): The Pydantic model containing the data.
        filename (str): The name of the CSV file to save to.
    """
    # Check if the file exists to determine if we need to write the header
    file_exists = os.path.isfile(filename)

    # Open the file in append mode, which creates the file if it doesn't exist
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        # Define the column headers
        fieldnames = ['transcript', 'summary', 'sentiment']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file is new, write the header row first
        if not file_exists:
            writer.writeheader()
        
        # Write the analysis data as a new row
        writer.writerow({
            'transcript': analysis_result.transcript,
            'summary': analysis_result.summary,
            'sentiment': analysis_result.sentiment
        })
