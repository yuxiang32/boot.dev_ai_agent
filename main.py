import argparse
import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for i in range(20):
        try:
            is_done = generate_content(client, messages, args.verbose)
            if is_done:
                break
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                print(f"Server overloaded, retrying in {2**i} seconds...")
                time.sleep(2**i)
                continue
            print(f"Error: {e}")
            break


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # Check the .candidates property
    # print(f"Candidates: {response.candidates[0].content}")
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        print("Response:")
        print(response.text)
        return True

    function_call_list = []
    for function_call_part in response.function_calls:
        function_result = call_function(function_call_part, verbose)
        if not function_result.parts[0].function_response.response:
            print("No .parts[0].function_response.response")
            sys.exit(1)
        function_call_list.append(function_result.parts[0])
        if verbose:
            print(f"-> {function_result.parts[0].function_response.response}")

    # Using types.Content constructor to convert the list of responses into a message
    messages.append(types.Content(role="user", parts=function_call_list))
    return False


if __name__ == "__main__":
    main()
