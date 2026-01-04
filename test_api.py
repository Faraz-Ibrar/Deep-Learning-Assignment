"""
Test the prediction API with a random image
"""
import requests
import numpy as np
from PIL import Image
import io

# Create a random test image (128x128 RGB)
np.random.seed(42)
random_image = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
img = Image.fromarray(random_image)

# Save to bytes
img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Send to API
print("Sending test image to prediction API...")
try:
    response = requests.post(
        "http://localhost:8000/predict",
        files={"file": ("test.png", img_bytes, "image/png")}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
