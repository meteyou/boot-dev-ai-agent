import os
from config import MAX_READ_LENGTH
from google.genai import types

def get_file_content(working_directory, file_path):
    if file_path.startswith("/"):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    full_file_path = os.path.join(working_directory, file_path)
    if not os.path.isfile(full_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_file_path, "r") as f:
            content = f.read(MAX_READ_LENGTH)
            if len(content) == MAX_READ_LENGTH:
                content += f'[...File "{file_path}" truncated at 10000 characters]'

            return content
    except Exception as e:
        return f"Error: {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
    ),
)