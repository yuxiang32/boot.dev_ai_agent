import os


def write_file(working_directory, file_path, content):
    abs_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_file_directory = os.path.dirname(abs_full_path)
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_directory):
        try:
            os.makedirs(abs_file_directory, exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {str(e)}"
    if os.path.exists(abs_full_path) and os.path.isdir(abs_full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(abs_full_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: writing to file: {str(e)}"
