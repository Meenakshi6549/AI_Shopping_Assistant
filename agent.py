
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found. Check your .env file.")

# Connect to Gemini with automatic retry settings
client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        retry_options=types.HttpRetryOptions(
            attempts=5,
            initial_delay=2.0,
            max_delay=20.0,
            exp_base=2.0,
            jitter=1.0,
            http_status_codes=[408, 429, 500, 502, 503, 504]
        )
    )
)

# Gemini model
MODEL_NAME = "gemini-3.5-flash-lite"


# Understand customer shopping requirements
def analyze_requirements(user_request):

    prompt = f"""
    You are an intelligent shopping assistant.

    Understand the customer's shopping request.

    Extract these details:
    - category (Laptop, Mobile, or Headphones)
    - budget (maximum price in INR)
    - min_ram (minimum RAM in GB)
    - min_storage (minimum storage in GB)
    - use_case (purpose of buying)

    If a value is not mentioned, use:
    budget = 100000
    min_ram = 0
    min_storage = 0

    Return only valid JSON.

    Customer request: {user_request}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    requirements = json.loads(response.text)
    return requirements


# Generate product recommendations
def generate_recommendation(user_request, products):

    if products.empty:
        return "Sorry! No matching products were found."

    product_details = products.to_string(index=False)

    prompt = f"""
    You are an AI shopping assistant.

    Customer request:
    {user_request}

    Available matching products:
    {product_details}

    Recommend the best matching products.

    Explain:
    1. Why the products match the request.
    2. Their important features.
    3. Their value for money.

    Only recommend products from the provided list.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
