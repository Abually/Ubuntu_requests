import os
import requests
from urllib.parse import urlparse
import uuid

# Create directory
os.makedirs("Fetched_Images", exist_ok=True)

# Prompt for image URL
image_url = input("Enter the image URL: ")

try:
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()  # Check for HTTP errors
except requests.exceptions.RequestException as e:
    print(f"Error fetching image: {e}")
    exit(1)

parsed_url = urlparse(image_url)
filename = os.path.basename(parsed_url.path)
if not filename:
    filename = f"image_{uuid.uuid4().hex}.jpg"

image_path = os.path.join("Fetched_Images", filename)
with open(image_path, "wb") as f:
    f.write(response.content)
print(f"Image saved as {image_path}")