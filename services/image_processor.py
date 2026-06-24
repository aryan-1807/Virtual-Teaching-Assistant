import easyocr
import numpy as np
from PIL import Image

def extract_image_text(image_file):
    try:
        # Convert uploaded file to OpenCV/Numpy format
        image = Image.open(image_file)
        img_np = np.array(image)
        
        # Initialize the reader inside the function (Lazy Loading)
        # This keeps the app from hanging during deployment boot!
        reader = easyocr.Reader(['en'], gpu=False)
        
        results = reader.readtext(img_np)
        extracted_text = " ".join([res[1] for res in results])
        
        return extracted_text if extracted_text.strip() else "Error: No text detected in image."
    except Exception as e:
        return f"Error processing image text: {str(e)}"