import unicodedata
import re

def normalize_string(text):
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return re.sub(r"\s+", " ", text).strip().lower()
