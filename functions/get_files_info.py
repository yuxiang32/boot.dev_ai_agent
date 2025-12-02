import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_full_path = os.path.abspath(full_path)
        abs_working_directory = os.path.abspath(working_directory)
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        print("Result for current directory")
        files_list = os.listdir(abs_full_path)
        output_string = ""
        for file in files_list:
            file_size = os.path.getsize(os.path.join(abs_full_path, file))
            is_dir = os.path.isdir(os.path.join(abs_full_path, file))
            output_string += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return output_string
    except Exception as e:
        return f"Error: {e}"
