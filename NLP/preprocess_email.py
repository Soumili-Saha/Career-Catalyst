import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Download NLTK resources
import nltk

# Specify the download directory
nltk.data.path.append(r"D:\python project\edtechwebsite\myenv\nltk_data")

# Download required NLTK resources
nltk.download('punkt', download_dir=r"D:\python project\edtechwebsite\myenv\nltk_data")
nltk.download('stopwords', download_dir=r"D:\python project\edtechwebsite\myenv\nltk_data")


def clean_text(text):
    """
    Cleans the input text by:
    - Removing non-alphanumeric characters.
    - Converting to lowercase.
    - Tokenizing and removing stopwords.
    """
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    tokens = word_tokenize(text)  # Tokenize text
    cleaned_tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    return cleaned_tokens

def preprocess_email(email):
    """
    Extracts and preprocesses only the body, subject, snippet, and label fields from an email dictionary.
    """
    preprocessed_data = {
        "subject": clean_text(email.get("subject", "")),
        "body": clean_text(email.get("body", "")),
        "snippet": clean_text(email.get("snippet", "")),
        "label": clean_text(email.get("label", ""))
    }
    return preprocessed_data
