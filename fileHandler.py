import os.path


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


# reads directory and creates list with name path and a path to a matching icon. Currently only directory,
# but should return all types of files with matching icon.
def generate_div_info_list(path):
    divs = []
    result = get_directory_values(path)

    for i in result:
        if os.path.isdir(os.path.join(path, i)):
            divs.append({'name': i, 'path': os.path.join(path, i), 'icon_path': 'static/icons/folder_icon.svg'})

    return divs
