import os
import argparse
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key is None:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content:
                    messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("Failed API request")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []

        if response.function_calls:
            for call in response.function_calls:
                result = call_function(call, args.verbose)
                if not result.parts:
                    raise Exception("Error: empty result.parts")
                if result.parts[0].function_response is None:
                    raise Exception("Error: empty function_response attribute")
                if result.parts[0].function_response.response is None:
                    raise Exception("Error: no function result")

                function_results.append(result.parts[0])
                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")

                # print(f"Calling function: {call.name}({call.args})")
        else:
            print(response.text)
            return

        messages.append(types.Content(role="user", parts=function_results))
    print("Error: maximum iterations reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
