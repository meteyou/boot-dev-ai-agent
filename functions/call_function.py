from config import WORKING_DIRECTORY
from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    match function_call_part.name:
        case "get_file_content":
            function_result = get_file_content(WORKING_DIRECTORY, **function_call_part.args)
        case "get_files_info":
            function_result = get_files_info(WORKING_DIRECTORY, **function_call_part.args)
        case "run_python_file":
            function_result = run_python_file(WORKING_DIRECTORY, **function_call_part.args)
        case "write_file":
            function_result = write_file(WORKING_DIRECTORY, **function_call_part.args)

        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )