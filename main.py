import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from functions.call_function import available_functions, call_function

def main():
    print("Hello from cli-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == "":
        raise RuntimeError("gemini api key not found")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)] ) ]

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if args.verbose == True:
        if response.usage_metadata != None:
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        else:
            raise RuntimeError("usage metadata returned None")

    function_results_list = []

    if response.function_calls != None:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            
            if function_call_result.parts[0].function_response == None:
                raise Exception("Error: function response is None")

            if function_call_result.parts[0].function_response.response == None:
                raise Exception("Error: function response content is None")
            
            function_results_list.append(function_call_result.parts[0])
            
            if args.verbose == True:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
