import re

def parse_flashcards(raw_text):
    """
    Extracts conceptual Front/Back key pairs from blockquote notation models.
    """
    cards = []
    # Find text matching blockquote indicators
    matches = re.findall(r'>\s*\*\*Front.*?\*\*:(.*?)\n>\s*\*\*Back.*?\*\*:(.*?)(?=\n>|\n\n|$)', raw_text, re.DOTALL)
    
    for match in matches:
        front = match[0].replace("[", "").replace("]", "").strip()
        back = match[1].replace("[", "").replace("]", "").strip()
        if front and back:
            cards.append({"front": front, "back": back})
            
    # Fallback parsing strategy if regex layout slips due to variable LLM punctuation
    if not cards:
        lines = [line.replace(">", "").strip() for line in raw_text.split("\n") if line.strip()]
        current_card = {}
        for line in lines:
            if "Front" in line:
                current_card["front"] = line.split(":", 1)[-1].strip()
            elif "Back" in line and "front" in current_card:
                current_card["back"] = line.split(":", 1)[-1].strip()
                cards.append(current_card)
                current_card = {}
                
    return cards[:4]