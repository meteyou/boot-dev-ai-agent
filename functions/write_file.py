import os
from google.genai import types

def write_file(working_directory, file_path, content):

    if file_path.startswith("/"):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    full_file_path = os.path.join(working_directory, file_path)

    if not os.path.exists(full_file_path):
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

    try:
        with open(full_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a string to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)