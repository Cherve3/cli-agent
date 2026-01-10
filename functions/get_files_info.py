import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) ==  abs_path

        files_str =  ""

        print(f"Result for {directory} directory:")

        if valid_target_dir == False:
            return f'    Error: "Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(os.path.join(working_directory, directory)):
            return f'    Error: "{directory}" is not a directory'

        directory_list = os.listdir(target_dir)

        for dir in directory_list:
            full_path = str(os.path.join(target_dir, dir))
            files_str += f"  - {dir}: file_size= {str(os.path.getsize(full_path))} bytes, is_dir="
            if os.path.isfile(full_path):
                files_str += "False"
            else:
                files_str += "True"
            files_str += "\n"
        return files_str
    except Exception as e:
        print(e)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)