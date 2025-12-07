import os
import subprocess

from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    if not str(abs_full_path).endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        result = subprocess.run(
            ["python", abs_full_path] + (args or []),
            timeout=30,
            capture_output=True,
            cwd=abs_working_directory,
            text=True,  # Decode stdout/stderr as strings instead of bytes
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"\nSTDERR:\n{result.stderr}")
        if result.returncode != 0:
            output.append(f"\nProcess exited with code {result.returncode}")
        return "\n".join(output) if output else "No output produced"
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of command-line arguments to pass to the Python script.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
