import os

from config import MAX_CHARS


def get_file_content(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path, "r") as file:
            content = file.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                content = (
                    content[:MAX_CHARS]
                    + "...File "
                    + file_path
                    + " truncated at 10000 characters"
                )
        return content
    except Exception as e:
        return f'Error reading file "{file_path}": {str(e)}'
