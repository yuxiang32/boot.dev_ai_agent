import os

from config import CHAR_LIMIT


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_full_path, "r") as file:
            content = file.read()
            if len(content) >= CHAR_LIMIT:
                content = (
                    content[:CHAR_LIMIT]
                    + "...File "
                    + file_path
                    + " truncated at 10000 characters"
                )
            return content
    except Exception as e:
        return f"Error: {str(e)}"
