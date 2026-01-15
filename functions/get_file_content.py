import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):

    working_directory_abs = os.path.abspath(working_directory) #Get absolute directory

    #Construct dir string
    target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
    validate_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    #Check if directory falls within the target directory
    if not validate_target_dir:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        # Read the file and return contents as a string
        with open(target_dir, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
        return content
    except UnicodeDecodeError:
        return f'Error: Unable to read file "{file_path}" (Binary or unknown encoding)'
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read contents of files within a working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
    ),
)