import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, file_path))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) ==  abs_path

        if valid_target_dir == False:
            return f'    Error: "Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(os.path.join(working_directory, file_path)):
            return f'    Error: "{file_path}" does not exist or is not a regular file: '

        if file_path.endswith(".py") == False:
            return f'    Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args:
            command.extend(args)

        str_result = ""
        process_result = subprocess.run(command, timeout=30, capture_output=True, check=True, text=True)
        return_code = process_result.returncode

        if return_code  != 0:
            str_result += f"Process exited with code {return_code}.\n"

        if process_result.stdout == None and process_result.stderr == None:    
            str_result += "No output produced\n" 
        else:
            str_result += f"- STDOUT:\n{process_result.stdout}\n- STDERR:\n{process_result.stderr}\n"
    
        return str_result

    except Exception as e:
        print(f"Error: executing Python file {e}")