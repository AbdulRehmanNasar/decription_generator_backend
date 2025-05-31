import traceback
from services.keyword_service import fetch_keywords
from services.openai_service import generate_description

def process_row(index_row_tuple, df):
    idx, row = index_row_tuple
    try:
        product = str(row["URUNADI"])
        category = str(row["KATEGORILER"])
        keywords = fetch_keywords(category)
        description = generate_description(product, category, keywords)
        return idx, description
    except Exception as e:
        error_msg = f"[Row Error] Row {idx}: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        return idx, error_msg