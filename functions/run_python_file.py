import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the Python file at the specified file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of target Python file to execute, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_directory_abspath, file_path))
        target_isvalid = (
            os.path.commonpath([working_directory_abspath, target])
            == working_directory_abspath
        )

        if not target_isvalid:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target]
        if args:
            command.extend(args)

        process = subprocess.run(
            command,
            capture_output=True,
            cwd=working_directory_abspath,
            text=True,
            timeout=30,
        )
        string_builder = []
        if process.returncode != 0:
            string_builder.append(f"Process exited with code {process.returncode}")
        if not process.stdout and not process.stderr:
            string_builder.append("No output produced")
        if process.stdout:
            string_builder.append(f"STDOUT: {process.stdout}")
        if process.stderr:
            string_builder.append(f"STDERR: {process.stderr}")

        return "\n".join(string_builder)

    except Exception as err:
        return f"Error: executing Python file: {err}"
