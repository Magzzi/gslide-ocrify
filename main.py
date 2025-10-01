import os
from PIL import Image
from pathlib import Path
from playwright.sync_api import sync_playwright
import pytesseract
from PyPDF2 import PdfMerger

import shutil

# Tesseract Path
tesseract_path = shutil.which('tesseract')

# Check if Tesseract Path exists in ENV Variables
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    raise FileNotFoundError("⚠️ Tesseract not found. Please install it and add to PATH.")

# Configure Tesseract path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ask user for a title
title = input("Please enter title: ")

# Create a folder with the title name (safe for filesystem)
folder = Path(title.strip().replace(" ", "_"))
folder.mkdir(parents=True, exist_ok=True)

p_id = input("Enter embedded id: ")
url = f"https://docs.google.com/presentation/d/e/{p_id}/pub?start=false&loop=false&delayms=3000"

total_slides = int(input("Enter page range: "))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for i in range(1, total_slides + 1):
        slide_url = f"{url}&slide=id.p{i}"
        page.goto(slide_url)
        page.wait_for_timeout(5000)  # wait 5 sec for slide to render
        page.screenshot(path=folder / f"screenshot_{i}.png", full_page=True)
        print(f'Capturing slide #{i}')

    browser.close()

print(f"✅ Screenshots saved in folder: {folder.resolve()}")

def convert_to_pdf(folder_path):
    import re

    # Collect only image files
    images = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    if not images:
        print(f"⚠️ No images found in {folder_path}")
        return None

    # Extract slide number from "screenshot_X.png"
    def slide_number(filename):
        match = re.search(r"screenshot_(\d+)", filename)
        return int(match.group(1)) if match else 0

    # Sort numerically by extracted number
    images.sort(key=slide_number)

    # Convert to full paths
    image_paths = [os.path.join(folder_path, f) for f in images]

    # Open and convert images
    pil_images = [Image.open(p).convert("RGB") for p in image_paths]

    output_path = os.path.join(folder_path, f"{title}_output.pdf")
    if pil_images:
        pil_images[0].save(output_path, save_all=True, append_images=pil_images[1:])
        print(f"📄 Non-searchable PDF saved at: {output_path}")
        return output_path
    else:
        print("⚠️ No images to save.")
        return None


pdf_path = convert_to_pdf(folder)

def make_pdf_readable(folder_path, input_pdf):
    import re

    # Collect only image files
    images = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    # Extract slide number from "screenshot_X.png"
    def slide_number(filename):
        match = re.search(r"screenshot_(\d+)", filename)
        return int(match.group(1)) if match else 0

    # Sort images numerically
    images.sort(key=slide_number)

    # Convert to full paths
    image_paths = [os.path.join(folder_path, f) for f in images]

    output_path = os.path.join(folder_path, f"MAIN_{title}.pdf")

    if image_paths:
        temp_pdfs = []
        # OCR each image -> temp PDFs
        for idx, img in enumerate(image_paths, start=1):
            pdf_bytes = pytesseract.image_to_pdf_or_hocr(img, extension='pdf')
            temp_path = os.path.join(folder_path, f"temp_{idx}.pdf")
            with open(temp_path, "wb") as f:
                f.write(pdf_bytes)
            temp_pdfs.append(temp_path)

        # Merge in order
        merger = PdfMerger()
        for pdf in temp_pdfs:
            merger.append(pdf)
        merger.write(output_path)
        merger.close()

        # Cleanup temp files
        for pdf in temp_pdfs:
            os.remove(pdf)

        print(f"✅ Searchable PDF saved at: {output_path}")
    else:
        print("⚠️ No images found!")


make_pdf_readable(folder, pdf_path)
