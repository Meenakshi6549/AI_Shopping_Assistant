
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key not found! Check your .env file.")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Say hello in one sentence."
        )

        print("Gemini connection successful!")
        print(response.text)

    except Exception as e:
        print("Connection failed:")
        print(type(e).__name__, e)
