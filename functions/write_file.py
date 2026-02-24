import os


def write_file(working_directory, file_path, content):
    try:
        working_directory_abspath = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(working_directory_abspath, file_path))
        target_isvalid = (
            os.path.commonpath([working_directory_abspath, target])
            == working_directory_abspath
        )
        if not target_isvalid:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as err:
        return f"Error: unexpected {err}"
