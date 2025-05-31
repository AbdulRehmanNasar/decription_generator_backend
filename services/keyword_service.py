import requests
import re
import traceback
from .utils import normalize_string
from config import serpapi_key

keyword_cache = {}

def fetch_keywords(category_raw):
    category = normalize_string(category_raw)
    if category in keyword_cache:
        print(f"[Keyword Cache hit] {category}")
        print(f"Keywords (cached): {keyword_cache[category]}")
        return keyword_cache[category]

    params = {
        "engine": "google",
        "q": category_raw,
        "hl": "tr",
        "gl": "tr",
        "location": "Turkey",
        "api_key": serpapi_key
    }

    try:
        print(f"Fetching keywords for category: {category_raw}")
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        related = data.get("related_searches", [])
        raw_keywords = [item["query"] for item in related]

        blocklist = ["trendyol", "hepsiburada", "amazon", "n11", "çiceksepeti", "gittigidiyor"]
        domain_pattern = re.compile(r'\.com|\.tr|\.net|\bwww\b', re.IGNORECASE)

        keywords = [
            kw for kw in raw_keywords
            if not any(b in kw.lower() for b in blocklist)
            and not domain_pattern.search(kw)
            and not any(char.isdigit() for char in kw)
        ][:5]

        keyword_cache[category] = keywords
        print(f"Keywords for '{category_raw}': {keywords}")
        return keywords
    except Exception as e:
        print(f"[Keyword Error] {category_raw}: {e}")
        traceback.print_exc()
        raise
