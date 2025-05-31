import traceback
from config import client

def generate_description(product_name, category, keywords):
    keyword_str = ", ".join(keywords)
    prompt = (
        f"Ürün Adı: {product_name}\n"
        f"Kategori: {category}\n"
        f"Anahtar Kelimeler: {keyword_str}\n\n"
        f"Lütfen aşağıdaki ürün için SEO uyumlu, 50-70 kelimelik bir açıklama yaz:\n"
        f"- Ürün: \"{product_name}\"\n"
        f"- Açıklama dili: Türkçe\n"
        f"- Tüm aşağıdaki anahtar kelimeleri kullan: {keyword_str}\n"
        f"- Anahtar kelimeleri açıklamaya doğal şekilde yerleştir (zorlama olmamalı).\n"
        f"- Açıklama etkileyici, akıcı ve müşteri çekici olmalı.\n"
        f"- Anahtar kelimeler eksiksiz ve yalnızca verilen haliyle kullanılmalı.\n\n"
        "Not: Tüm anahtar kelimelerin açıklamada yer aldığından emin ol. Gerekiyorsa cümleleri yeniden düzenle ama hiçbir anahtar kelimeyi atlama."
    )

    print("\nPrompt sent to OpenAI:\n" + "-"*40)
    print(prompt)
    print("-"*40)

    try:
        print(f"Generating description for: {product_name}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        description = response.choices[0].message.content.strip()
        print(f"Description for '{product_name}': {description}")
        return description
    except Exception as e:
        error_msg = f"[GPT Error] {product_name}: {str(e)}"
        print(error_msg)
        traceback.print_exc()
        if "invalid api key" in str(e).lower() or "unauthorized" in str(e).lower():
            raise RuntimeError("API configuration error")
        return error_msg