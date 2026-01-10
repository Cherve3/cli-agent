import os

from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) ==  abs_path

        if valid_target_dir == False:
            return f'    Error: "Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path):
            return f'    Error: Cannot write to "{file_path}" as it is a directory'
        else:
            print(f"Creating directories for {file_path} if necessary...")
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        

        with open(target_dir, 'w') as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print(e)
        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file in the working directory.",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)