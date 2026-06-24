from sarvamai import SarvamAI
import os
from utils.prompts import LEVEL_GUIDELINES, get_convert_qa_prompt

def convert_to_qa_format(context, level="Intermediate"):
    """
    Converts raw text streams into structured Question and Answer study layout strings.
    """
    api_key = os.getenv("SARVAM_API_KEY")
    client = SarvamAI(api_subscription_key=api_key)
    guideline = LEVEL_GUIDELINES.get(level, LEVEL_GUIDELINES["Intermediate"])
    
    prompt = get_convert_qa_prompt(context, guideline, level)
    
    try:
        response = client.chat.completions(
            messages=[{"role": "user", "content": prompt}],
            model="sarvam-30b",
            temperature=0.3,
            max_tokens=1500
        )
        
        choice = response.choices[0]
        content = getattr(choice.message, "content", None)
        if content is None:
            content = getattr(choice.message, "reasoning_content", None)
            
        return content if content else "Error rendering QA document structure conversion."
    except Exception as e:
        return f"QA Generation error encountered: {str(e)}"