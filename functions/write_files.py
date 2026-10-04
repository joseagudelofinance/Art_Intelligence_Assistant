import os

schema_write_files = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "gets a file info a writes specified content on it. It received a file path within a specified folders, and creates parent if needed",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to be written, relative to the working directory",
                },
                "content": {
                     "type": "string",
                     "description": "content provided by user of function and to be written into the file"
                },
            },
            "required": ["file_path", "content"], 
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        path = os.path.abspath(working_directory)
        target_file = os.path.join(path, file_path)
        target_file = os.path.normpath(target_file)
    
        valid_target_dir = os.path.commonpath([path, target_file]) == path
    
   
        if valid_target_dir == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isdir(target_file) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_path = os.path.dirname(target_file)
        os.makedirs(parent_path, exist_ok=True)

        with open(target_file, "w") as file_object:
            file_contents = file_object.write(content)
        
            return f'Successfully wrote to "{target_file}" ({len(content)} characters written)'

    except Exception as e:
            return f"Error: {e}"