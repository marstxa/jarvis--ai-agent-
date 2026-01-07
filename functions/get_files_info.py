import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    
    working_directory_abs = os.path.abspath(working_directory) #Get absolute directory

    #Construct dir string
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
    validate_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    #Check if directory falls within the target directory
    if not validate_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    dir_list = os.listdir(target_dir)
    if dir_list == []:
        return f"Error {directory} is empty"
    
    dir_info = ""

    #Print files and directory within the target directory
    for file in dir_list:
        file_path = os.path.join(target_dir, file)
        dir_info += f'- {file}: {os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n'

    return dir_info

#LLM Function declaration
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