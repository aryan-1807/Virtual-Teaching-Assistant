LEVEL_GUIDELINES = {
    "Beginner": "Explain concepts using basic, simple language, clear everyday analogies, and zero advanced jargon.",
    "Intermediate": "Provide well-structured answers using accurate academic terminology, clear analytical depth, and structured breakdowns.",
    "Advanced": "Deliver comprehensive, deeply technical breakdowns, high-level theoretical analysis, and precise professional terminology."
}

def get_qa_prompt(context, question, guideline, level):
    return f"""
Context Material Provided (Extracted via RAG from the uploaded file/image):
{context}

User Input/Question:
{question}

Target Audience Complexity Level: {level} ({guideline})

STRICT GROUNDING CONSTRAINT RULES:
1. Answer the question using **ONLY** the facts directly mentioned in the Context Material provided above.
2. ABSOLUTELY FORBIDDEN: Do not use any external knowledge. Do not add extra examples, protocols (like HTTP, FTP, SMTP, DNS), or definitions that are not explicitly written in the text above.
3. If the user asks about a specific layer, look at what the text says for that layer, clean up any typos or scanning layout errors, and present *only* those facts in clean Markdown format.
4. Output the tag "===START_STUDY_GUIDE_FINAL_ANSWER===" immediately before your final answer text. Do not output any brainstorming or thinking steps.
"""

def get_summarize_prompt(context, guideline, level):
    return f"""
Context Material:
{context}

Task: Generate a summary based ONLY on the provided text. Do not add outside information.
MANDATORY OUTPUT INSTRUCTION:
You must output the special tag "===START_STUDY_GUIDE_FINAL_ANSWER===" right before you write your final summary content.
"""

def get_mcq_prompt(context, guideline, level):
    return f"""
Context Material:
{context}

Task: Construct 3 Multiple Choice Questions based strictly on the provided context facts only.
MANDATORY OUTPUT INSTRUCTION:
You must output the special tag "===START_STUDY_GUIDE_FINAL_ANSWER===" right before you write your questions list.
"""

def get_flashcard_prompt(context, guideline, level):
    return f"""
Context Material:
{context}

Task: Create 4 concise conceptual flashcards based strictly on the provided context facts only.
MANDATORY OUTPUT INSTRUCTION:
You must output the special tag "===START_STUDY_GUIDE_FINAL_ANSWER===" right before you write your flashcards block.
"""

def get_convert_qa_prompt(context, guideline, level):
    return f"""
Context Material:
{context}

Task: Transform the provided context material into a structured Question & Answer format based strictly on the text facts only.
MANDATORY OUTPUT INSTRUCTION:
You must output the special tag "===START_STUDY_GUIDE_FINAL_ANSWER===" right before you write your transcript content lines.
"""