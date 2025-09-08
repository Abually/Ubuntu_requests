import os
import requests
from urllib.parse import urlparse
import uuid
import hashlib

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename or '.' not in filename:
        filename = f"image_{uuid.uuid4().hex}.jpg"
    return filename

def is_image_content(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type.startswith('image/')

def get_image_hash(image_bytes):
    return hashlib.sha256(image_bytes).hexdigest()

def main():
    urls = input("Enter image URLs separated by commas:\n").split(',')
    urls = [url.strip() for url in urls if url.strip()]
    os.makedirs("Fetched_Images", exist_ok=True)

    # Track hashes to prevent duplicates
    existing_hashes = set()
    for fname in os.listdir("Fetched_Images"):
        fpath = os.path.join("Fetched_Images", fname)
        if os.path.isfile(fpath):
            with open(fpath, "rb") as f:
                existing_hashes.add(get_image_hash(f.read()))

    for url in urls:
        print(f"\nProcessing: {url}")
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")
            continue

        # Security precaution: check content length
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) > 10_000_000:  # 10MB limit
            print("Image too large, skipping.")
            continue

        # Check for image content-type
        if not is_image_content(response):
            print("URL does not point to an image, skipping.")
            continue

        image_bytes = response.content
        image_hash = get_image_hash(image_bytes)
        if image_hash in existing_hashes:
            print("Duplicate image detected, skipping.")
            continue

        filename = get_filename_from_url(url)
        image_path = os.path.join("Fetched_Images", filename)
        # Prevent overwriting files
        if os.path.exists(image_path):
            filename = f"{uuid.uuid4().hex}_{filename}"
            image_path = os.path.join("Fetched_Images", filename)

        with open(image_path, "wb") as f:
            f.write(image_bytes)
        print(f"Image saved as {image_path}")
        existing_hashes.add(image_hash)