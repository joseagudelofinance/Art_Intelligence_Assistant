import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "opens python file via command line and records and prints exit code, stderrc, stdout, provided it is in a valid directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                     "type": "array",
                     "items": {
                         "type": "string",
                     },
                     "description": "optional addicional string arguments to be run in python file"
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        path = os.path.abspath(working_directory)
        target_file = os.path.join(path, file_path)
        target_file = os.path.normpath(target_file)
    
        valid_target_dir = os.path.commonpath([path, target_file]) == path
    
   
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isfile(target_file) == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python",target_file]
        
        if args is not None:
            command.extend(args)

        result = subprocess.run(command, cwd=path, capture_output=True, timeout=30, text=True)

        result_str = ""
        result2_str = ""
        result3_str = ""
        result4_str = ""

        if result.returncode != 0:
             result_str = f"Process exited with code {result.returncode}"
        if len(result.stdout) == 0 and len(result.stderr) == 0:
             result2_str = "No output produced" 
        if len(result.stdout) >= 1:
            result3_str = f"STDOUT: {result.stdout}"
        if len(result.stderr) >= 1:
            result4_str = f"STDERR: {result.stderr}"

        composite_str = "\n".join([result_str, result2_str, result3_str, result4_str])

        return composite_str

    except Exception as e:
            return f"Error: executing Python file: {e}"