import os.path
import json
import pathlib
import magic


# saves file from binary data. e.g. from image upload
def save_file_from_binary_content(file_binary, file_name, save_path):
    try:
        with open(os.path.join(save_path, file_name), "wb") as file:
            file.write(file_binary)
    except Exception as e:
        return e
    finally:
        return f"Successfully uploaded {file_name}"


# read directory
def get_directory_values(path):
    return os.listdir(path)


# reads directory and creates list with name path and a path to a matching icon.
def generate_div_info_list(path):
    result = []
    files = get_directory_values(path)

    settings = {}

    with open("filePickerSettings.json", 'r') as file:
        settings = json.load(file)

    for i in files:
        if os.path.isdir(os.path.join(path, i)):
            result.append({'name': i,
                           'path': os.path.join(path, i),
                           'icon_path': settings['icons']['Directory']})
        elif os.path.isfile(os.path.join(path, i)):
            try:
                result.append({'name': i,
                               'path': os.path.join(path, i),
                               'icon_path': settings['icons']['files'][pathlib.Path(i).suffix.upper()]})
            except KeyError:
                result.append({'name': i, 'path': path,
                               'icon_path': settings['icons']['files']['unknown']})

    return result
