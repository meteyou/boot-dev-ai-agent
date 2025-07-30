import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_list = os.listdir(working_directory)

    if directory not in working_dir_list and directory != ".":
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    path = os.path.join(working_directory, directory)

    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    try:
        dir_list = os.listdir(path)
        output = []
        for file in dir_list:
            file_path = os.path.join(path, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)

            output.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(output)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)