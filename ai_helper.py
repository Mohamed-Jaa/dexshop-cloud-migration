import os
import json
import base64
import requests

def generate_product_metadata(product_name: str, image_bytes: bytes = None, mime_type: str = "image/jpeg"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY environment variable is not set.")
        return None

    prompt = f"""You are an expert e-commerce catalog assistant.
Input Product Name: "{product_name}"

INSTRUCTIONS:
1. Extract EXACT technical specifications (CPU model, RAM capacity, Storage size/type, Screen size/resolution). Priority goes to explicit details found in the input text.
2. Generate a clean, refined product title.
3. Estimate a reasonable market price in USD (numeric string only, e.g. "650").
4. Write a professional 2-3 sentence product description.

Return ONLY a valid JSON object matching this schema:
{{
    "clean_name": "Full Clean Product Name",
    "description": "Professional 2-3 sentence description.",
    "price_usd": "650",
    "condition": "New",
    "specs": [
        {{"title": "CPU", "desc": "Exact CPU from specs"}},
        {{"title": "RAM", "desc": "Exact RAM from specs"}},
        {{"title": "Storage", "desc": "Exact Storage from specs"}},
        {{"title": "Display", "desc": "Exact Display from specs"}}
    ]
}}
Do NOT return markdown code blocks. Return pure raw JSON only."""

    parts = [{"text": prompt}]
    if image_bytes:
        parts.append({
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(image_bytes).decode("utf-8")
            }
        })

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": parts}]}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        if response.status_code != 200:
            print(f"API Error ({response.status_code}): {response.text}")
            return None

        result_json = response.json()
        text = result_json["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text.strip())
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return None
