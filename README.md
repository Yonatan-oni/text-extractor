# Text-Extractor
A Django app that allows users to upload multiple images and extract text from them using Google Cloud Vision API. The extracted text can be downloaded as a .txt file.

# Features
   * Multiple Image Uploads: Supports uploading multiple images at once for processing.
   * Text Extraction: Uses Google Cloud Vision API to extract text from images.
   * File Download: Provides a downloadable .txt file containing the extracted text.

# Technologies Used
  * Backend: Django, Python
  * Frontend: HTML
  * Text Extraction: Google Cloud Vision API

# Setup and Installation
### 1. Clone the repository:
```bash
git clone https://github.com/Yonatan-oni/text-extractor.git
cd text_extractor
```
### 2.  Set Up Virtual Environment:
```bash
python -m venv venv
./venv/bin(Scripts)/activate
```

### 3.  Install dependencies:
```bash
pip install -r requirements.txt
```
### 4.  Set up your Google Cloud Vision API credentials:
   * Obtain the API key from [Google Cloud Console](https://console.cloud.google.com/)
   * Set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your key file
### 5. Update Django settings:
   * Configure the MEDIA_ROOT and MEDIA_URL in your settings.py file.
### 6. Run database migrations:
```bash
python manage.py migrate
```
### 7. Start the app:
```bash
python manage.py runserver
```
   
