from services.llm_service import ask_gemini

def convert_to_qa_format(context, level="Intermediate"):
    """
    Converts the raw document context into structural study Q&As based on complexity level.
    """
    execution_query = "Read the following context text content thoroughly and reorganize its core underlying data framework into clear, comprehensive, and structural Question and Answer (Q&A) pairs optimized for learning study guides."
    
    # Delegate cleanly to your core working Gemini service layer
    answer = ask_gemini(execution_query, context, level=level, task_type="QA")
    return answer