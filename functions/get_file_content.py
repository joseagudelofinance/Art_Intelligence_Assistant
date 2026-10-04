import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "gets the file content trunctated to specified length, provided it is in a valid directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to get the content from, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}

def get_file_content(working_directory:str, file_path: str) -> str:
    try:
        path = os.path.abspath(working_directory)
        target_file = os.path.join(path, file_path)
        target_file = os.path.normpath(target_file)
    
        valid_target_dir = os.path.commonpath([path, target_file]) == path
    
   
        if valid_target_dir == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
        if os.path.isfile(target_file) == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        max_length = 10000

        with open(target_file, "r") as file_object:
            file_contents = file_object.read(max_length)
        
            if file_object.read(1):
                file_contents += f'[...File "{file_path}" truncated at {max_length} characters]'

        return file_contents
        
    except Exception as e:
            return f"Error: {e}"