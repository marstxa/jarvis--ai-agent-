import os
import subprocess
import sys

def run_python_file(working_directory, file_path, args=None):
        
    working_directory_abs = os.path.abspath(working_directory) #Get absolute directory

    #Construct dir string
    target_dir = os.path.normpath(os.path.join(working_directory_abs, file_path))
    validate_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

    #Check if directory falls within the target directory
    if not validate_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_dir):
        return f'Error: "{file_path}" does not exist'
    
    if not target_dir.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    

    try:
        #SUBPROCESS
        command = [sys.executable, target_dir]
        
        if args is not None:
            command.extend(args)
        
        completed_process = subprocess.run(command, capture_output=True, text=True, timeout=30) #run subprocess

        output_log = ""

        #check if process was successful 
        if completed_process.returncode != 0:
            output_log += f"Process exited with code {completed_process.returncode}\n"
        elif completed_process.stdout is None or completed_process.stderr is None:
            output_log += "No output produced"
        else:
            output_log += f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
        
        return output_log
    
    except subprocess.TimeoutExpired:
        return f"Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}"
