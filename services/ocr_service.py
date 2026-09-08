import base64
import json
import os

EXTRACTION_PROMPT = """You are reading a restaurant bill photo. Extract the data and
respond with ONLY valid JSON (no markdown, no explanation) in exactly this shape:

{
  "items": [
    {"name": str, "quantity": number, "unit_price": number, "line_total": number, "confidence": 0-1}
  ],
  "subtotal": number, "subtotal_confidence": 0-1,
  "discount": number, "discount_confidence": 0-1,
  "tax": number, "tax_confidence": 0-1,
  "service_charge": number, "service_charge_confidence": 0-1,
  "printed_total": number, "printed_total_confidence": 0-1
}

Rules:
- If a field is not visible/printed on the bill, use 0 for the number and a low confidence (e.g. 0.1).
- confidence reflects how sure you are the value is correctly read (1 = certain, 0 = guess).
- Numbers only, no currency symbols.
"""


def load_demo_bills():
    """Returns the list of all 15 demo bill presets with metadata."""
    demo_path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "demo_bills.json")
    if os.path.exists(demo_path):
        with open(demo_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def get_demo_bill(bill_id):
    """Fetch a single demo bill preset by its ID."""
    all_bills = load_demo_bills()
    for b in all_bills:
        if b.get("id") == bill_id:
            return b
    if all_bills:
        return all_bills[0]
    return {"bill": load_demo_data()}


def load_demo_data(filename=None):
    """
    Returns bill dict for mock/demo mode.
    If filename is given, attempts to find the matching demo bill preset.
    """
    all_bills = load_demo_bills()
    if all_bills and filename:
        fn_lower = filename.lower()
        for b in all_bills:
            b_id = b.get("id", "").lower()
            b_img = b.get("image_file", "").lower()
            if (b_id and b_id in fn_lower) or (b_img and b_img in fn_lower):
                return b["bill"]

    # Default fallback
    if all_bills:
        return all_bills[0]["bill"]

    fallback_path = os.path.join(os.path.dirname(__file__), "..", "sample_data", "demo_bill.json")
    with open(fallback_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_bill_data(image_path, api_key, demo_mode=False, model="claude-sonnet-4-5"):
    """
    Returns a dict matching the schema in EXTRACTION_PROMPT.
    Falls back to demo data if demo_mode is True, no api_key, or the API call fails.
    """
    filename = os.path.basename(image_path) if image_path else ""

    if demo_mode or not api_key:
        return load_demo_data(filename=filename)

    try:
        import anthropic

        with open(image_path, "rb") as f:
            image_data = base64.standard_b64encode(f.read()).decode("utf-8")

        ext = image_path.rsplit(".", 1)[-1].lower()
        media_type = "image/png" if ext == "png" else "image/jpeg"

        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}},
                    {"type": "text", "text": EXTRACTION_PROMPT}
                ]
            }]
        )

        raw_text = response.content[0].text.strip()
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        return json.loads(raw_text)

    except Exception as e:
        print(f"[OCR] API extraction failed, using demo data. Reason: {e}")
        return load_demo_data(filename=filename)

