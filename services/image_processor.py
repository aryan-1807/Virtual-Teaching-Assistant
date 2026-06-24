import easyocr
import numpy as np
from PIL import Image

# Initialize the reader once to keep execution fast
reader = easyocr.Reader(['en'], gpu=False)

def extract_image_text(image_file):
    """
    Extracts text from uploaded images or hand-drawn sketches.
    Accepts a Streamlit UploadedFile object.
    """
    try:
        # Convert Streamlit file upload to PIL Image, then to a numpy array for EasyOCR
        img = Image.open(image_file)
        img_np = np.array(img)
        
        # Read text sequences from the image
        results = reader.readtext(img_np, detail=0)
        
        # Join extracted sentences with line breaks
        extracted_text = "\n".join(results)
        return extracted_text
        
    except Exception as e:
        return f"Error parsing image files: {str(e)}"