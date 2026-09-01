import os
import json
from google import genai
from google.genai import types

def generate_product_metadata(product_name: str, image_bytes: bytes = None, mime_type: str = "image/jpeg"):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an expert e-commerce catalog assistant.
    Input Product Name: "{product_name}"

    INSTRUCTIONS:
    1. If an image is provided, carefully read any visible text, specs, labels, or badges inside the image (OCR).
    2. Extract EXACT technical specifications (CPU model, RAM capacity, Storage size/type, Screen size/resolution). Priority goes to explicit details found in the input text or image.
    3. Generate a clean, refined product title.
    4. Estimate a reasonable market price in USD (numeric string only, e.g. "650").
    5. Write a professional 2-3 sentence product description.

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
    Do NOT return markdown code blocks. Return pure raw JSON only.
    """

    contents = [prompt]
    if image_bytes:
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=mime_type
            )
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents
        )
        
        text = response.text.strip()
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