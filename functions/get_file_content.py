import os

MAX_CHARS = 10_000

def get_file_content(working_directory, file_path):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) ==  abs_path

        if valid_target_dir == False:
            return f'    Error: "Cannot list "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(os.path.join(working_directory, file_path)):
            return f'    Error: File not found or is not a regular file: "{file_path}"'

        with open(target_dir, 'r') as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        print(e)