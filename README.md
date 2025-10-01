
# OCR and PDF Merger Script

This project uses Python, Tesseract OCR, and Playwright to extract text from images/PDFs and merge PDF files.

## Setup and Installation Batch File
- [Download Batch File Here](https://drive.google.com/file/d/1uoEwz1z8JQt61altt9c5m4RULCepNOZ5/view?usp=sharing)
  
## Prerequisites
- Python 3.9+ installed
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system  
  - On Windows: Download the installer from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)  
  - After installation, add the Tesseract path to your system `PATH` environment variable, or configure it directly in the script:
    ```python
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    ```

## Installation

### 1. Clone or download this repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
````

### 2. Create and activate a virtual environment

```bash
# Create venv
python -m venv venv

# Activate venv
# On Windows (cmd)
venv\Scripts\activate

# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Linux / macOS
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers

```bash
playwright install
```

## Usage

Run your script with:

```bash
python main.py
```

(where `main.py` is your Python file name).

## Notes

* Make sure Tesseract is correctly installed and accessible.
* For PDF merging, ensure your files exist and paths are correct.


