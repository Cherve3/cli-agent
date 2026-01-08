import os
import argparse

from dotenv import load_dotenv
from google import genai


def main():
    print("Hello from cli-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == "":
        raise RuntimeError("gemini api key not found")
    client = genai.Client(api_key=api_key)

    contents = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    response = client.models.generate_content(model="gemini-2.5-flash", contents=args.user_prompt)

    if response.usage_metadata != None:
        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
    else:
        raise RuntimeError("usage metadata returned None")

    print(response.text)

if __name__ == "__main__":
    main()
