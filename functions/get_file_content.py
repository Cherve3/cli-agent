import os

from google.genai import types

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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file in the working directory.",
    parameters=types.Schema(
        required=["file_path"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)