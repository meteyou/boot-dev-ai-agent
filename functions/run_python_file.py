import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    if file_path.startswith("/") or ".." in file_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    full_file_path = os.path.join(working_directory, file_path)
    if not os.path.isfile(full_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: File "{file_path}" is not a Python file.'

    try:
        full_args = ['python3', file_path]
        full_args.extend(args)

        process = subprocess.run(
            full_args,
            timeout=30,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_directory
        )
        output = [f"STDOUT: {process.stdout}", f"STDERR: {process.stderr}"]
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass to the Python file.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)