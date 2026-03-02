import os
from config import CHARACTER_LIMIT
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns the text content of the specified file up to a limit of {CHARACTER_LIMIT} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_directory_abspath, file_path))
        target_isvalid = (
            os.path.commonpath([working_directory_abspath, target])
            == working_directory_abspath
        )
        if not target_isvalid:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target, "r") as reader:
            file_content = reader.read(CHARACTER_LIMIT)
            if reader.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
                )
        return file_content

    except Exception as err:
        return f"Error: unexpected {err}"
