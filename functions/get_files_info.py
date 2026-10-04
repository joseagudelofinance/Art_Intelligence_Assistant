import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    try:
        path = os.path.abspath(working_directory)
        target_dir = os.path.join(path, directory)
        target_dir = os.path.normpath(target_dir)

        valid_target_dir = os.path.commonpath([path, target_dir]) == path
        first_reply = ""

        if directory == ".":
            first_reply = f"Result for current directory:\n"
        else:
            first_reply = f"Result for '{directory}' directory:\n"


        if valid_target_dir == False:
            return f'{first_reply}\tError: Cannot list "{directory}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir) == False:
            return f'{first_reply}\tError: "{directory}" is not a directory'

        desc_dir: str = ""

        for item in os.listdir(target_dir):
            desc_dir = desc_dir + f"\t- {item}: file_size={os.path.getsize(target_dir+"/"+item)} bytes, is_dir={os.path.isdir(target_dir+"/"+item)} \n"

        return f"{first_reply}{desc_dir}"       
    
        # return f'Success: "{directory}" is within the working directory'
    
    except Exception as e:
        return f"{first_reply}\tError: {e}"
