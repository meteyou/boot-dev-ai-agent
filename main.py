import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT
from functions.call_function import call_function
from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


def main():
    print("Hello from boot-dev-agent!")
    verbose = "--verbose" in sys.argv
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) < 2:
        print("No prompt provided")
        exit(1)

    user_prompt=sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    llm_loop = 0
    response = None

    try:
        while llm_loop < 20:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=SYSTEM_PROMPT
                )
            )

            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_response = call_function(function_call_part, verbose)

                    if not function_response.parts[0].function_response.response:
                        raise Exception()
                    elif verbose:
                        print(f"-> {function_response.parts[0].function_response.response}")

                    messages.append(function_response)

            else:
                llm_loop = 20

        print(f"\nLLM Output:")
        print(response.text)

        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except Exception as e:
        print(f"Error ({e.code}): {e.message}")


if __name__ == "__main__":
    main()
