import os


def get_files_info(working_directory, directory="."):
    working_directory_abspath = os.path.abspath(working_directory)
    target_directory = os.path.normpath(
        os.path.join(working_directory_abspath, directory)
    )
    target_directory_isvalid = (
        os.path.commonpath([working_directory_abspath, target_directory])
        == working_directory_abspath
    )

    if not target_directory_isvalid:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_directory):
        return f'Error: "{directory}" is not a directory'

    file_metadata = []
    try:
        for filename in os.listdir(target_directory):
            full_path = os.path.join(target_directory, filename)
            file_metadata.append(
                f"- {filename}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
            )
        return "\n".join(file_metadata)
    except Exception as err:
        return f"Error: unexpected {err}"
