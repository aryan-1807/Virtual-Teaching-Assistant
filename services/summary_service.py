def parse_summary_blocks(raw_text):
    """
    Cleans and structures raw summary text outputs into high-level thesis 
    and detailed takeaway bullet strings for structured UI presentation grids.
    """
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    
    thesis_blocks = []
    bullet_takeaways = []
    
    for line in lines:
        # Check if line marks a standard list bullet item notation
        if line.startswith(("-", "*", "•", "1.", "2.", "3.")):
            cleaned_bullet = line.lstrip("-*•0123456789. ").strip()
            if cleaned_bullet:
                bullet_takeaways.append(cleaned_bullet)
        else:
            if "Format Requirements" not in line and "Task:" not in line:
                thesis_blocks.append(line)
                
    # Reassemble separated blocks safely 
    thesis_paragraph = " ".join(thesis_blocks) if thesis_blocks else "Source analysis complete."
    
    return {
        "thesis": thesis_paragraph,
        "takeaways": bullet_takeaways if bullet_takeaways else ["Review document workspace overview panel for extra text context metrics."]
    }