import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors
from utils.prompts import LEVEL_GUIDELINES, get_qa_prompt, get_summarize_prompt, get_mcq_prompt, get_flashcard_prompt

load_dotenv()

# Initialize the official Gemini client instance globally
client = genai.Client()

def ask_gemini(question, context, level="Intermediate", task_type="QA"):
    guideline = LEVEL_GUIDELINES.get(level, LEVEL_GUIDELINES["Intermediate"])

    # Determine prompt layout strategy based on active mode
    if task_type == "SUMMARIZE":
        prompt = get_summarize_prompt(context, guideline, level)
    elif task_type == "MCQ":
        prompt = get_mcq_prompt(context, guideline, level)
    elif task_type == "FLASHCARD":
        prompt = get_flashcard_prompt(context, guideline, level)
    else:
        prompt = get_qa_prompt(context, question, guideline, level)

    # Try the request up to 3 times to handle temporary 429 rate limits seamlessly
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            
            if not response.text:
                return "Error: Empty text payload returned from Gemini architecture."
                
            return response.text.strip()
            
        except errors.APIError as e:
            if e.code == 429:
                if attempt < 2:
                    # Wait 4 seconds and automatically retry the transaction backend loop
                    time.sleep(4)
                    continue
                else:
                    return "⚠️ **Gemini API Free Tier Limit Exceeded.** Please pause for 60 seconds before resubmitting."
            return f"Gemini API Error ({e.code}): {e.message}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"