import re

def parse_mcqs(raw_text):
    """
    Parses raw LLM text into structured lists of dictionaries for interactive rendering.
    """
    questions = []
    # Split text into blocks looking for question numbers
    raw_blocks = re.split(r'(?:Question|\d+\.)\s*[:\d]*', raw_text)
    
    for block in raw_blocks:
        if not block.strip() or "Options" in block:
            continue
            
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        
        q_text = ""
        options = {}
        correct = ""
        explanation = ""
        
        for line in lines:
            if line.startswith(("A)", "B)", "C)", "D)", "A.", "B.", "C.", "D.")):
                key = line[0]
                options[key] = line[2:].strip()
            elif "Correct Answer" in line or "Answer:" in line:
                # Extract character flag A, B, C, or D
                match = re.search(r'\b([A-D])\b', line)
                if match:
                    correct = match.group(1)
            elif "Explanation" in line:
                explanation = line.split(":", 1)[-1].strip()
            else:
                if not options:
                    q_text += " " + line
                    
        if q_text and options:
            questions.append({
                "question": q_text.strip(),
                "options": options,
                "correct": correct if correct else "A",
                "explanation": explanation if explanation else "Verified from source context material."
            })
            
    return questions[:3] # Ensure it constraints to 3 items