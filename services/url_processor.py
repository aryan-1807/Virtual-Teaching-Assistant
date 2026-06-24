import requests
from bs4 import BeautifulSoup

def extract_url_text(url_string):
    url_string = url_string.strip()
    if not url_string:
        return ""
        
    if "import " in url_string or "def " in url_string or "\n" in url_string:
        return "Error: Invalid URL entered."
        
    if not url_string.startswith(("http://", "https://")):
        url_string = "https://" + url_string
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        response = requests.get(url_string, headers=headers, timeout=10)
        if response.status_code != 200:
            return f"Error: Webpage unreachable. Code {response.status_code}"
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Guard: If it's a YouTube link, extract titles/meta description text 
        # since standard paragraphs don't exist on video play frames
        if "youtube.com" in url_string or "youtu.be" in url_string:
            title_tag = soup.find("title")
            meta_desc = soup.find("meta", attrs={"name": "description"})
            title_text = title_tag.get_text() if title_tag else "YouTube Video"
            desc_text = meta_desc["content"] if meta_desc else "No video description available."
            return f"Source Format: YouTube Video\nTitle: {title_text}\nContext Summary: {desc_text}"

        for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
            element.decompose()
            
        chunks = [p.get_text().strip() for p in soup.find_all(["p", "h1", "h2", "h3", "h4", "li"])]
        return "\n".join([c for c in chunks if len(c) > 10])
        
    except Exception as e:
        return f"Error fetching URL: {str(e)}"