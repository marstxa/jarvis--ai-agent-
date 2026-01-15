import os
from google.genai import types

def write_file(working_directory, file_path, content):

    working_directory_abs = os.path.abspath(working_directory) #Get absolute directory

    #Construct dir string
    target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
    validate_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    #Check if directory falls within the target directory
    if not validate_target_dir:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        # Make parent directory of file path if it does not exist
        parent_dir = os.path.dirname(target_dir)
        os.makedirs(parent_dir, exist_ok=True)

        with open(target_dir, "w", encoding="utf-8") as f:
            f.write(content)
        f.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except UnicodeEncodeError:
        return f'Error: Unable to write file "{file_path}" (Binary or unknown encoding)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a file within a working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
    ),
)