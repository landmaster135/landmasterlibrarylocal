# dir_editor.py

# Library by default
import os, sys, platform
import shutil, pathlib
# Library by third party
# nothing
# Library by local
# nothing
# Library by landmasterlibrary
# nothing

def generate_file_name(dir_name : str, sep : str, filename_with_ext : str) -> str:
    '''
    dirname           : String directory name.
    sep               : String seperator of direcotry.
    filenameWithExt   : String filename with extension. (name of directory is also OK.)
    GeneratedFileName : String FileName Generated in this function.
    '''
    if type(dir_name) != str:
        raise TypeError("dir_name must be str type.")
    if type(sep) != str:
        raise TypeError("sep must be str type.")
    if type(filename_with_ext) != str:
        raise TypeError("filename_with_ext must be str type.")
    generated_file_name = f'{dir_name}{sep}{filename_with_ext}'
    return generated_file_name

def make_directory(file_name : str) -> str:
    '''
    filename  : String fullname of selected file.
    new_name  : String name of folder having rotated files.
    made_path : String path of folder having rotated files.
    '''
    if type(file_name) != str:
        raise TypeError("file_name must be str type.")
    new_name = input("Input a name of new folder: ")
    made_path = generate_file_name(os.path.dirname(file_name), decide_seperator(), new_name)
    while os.path.isdir(made_path) == True:
        new_name = input("That name already exists. Reinput: ")
        # new path entry
        made_path = generate_file_name(os.path.dirname(file_name), decide_seperator(), new_name)

    # make new directory if new directory is none.
    if os.path.isdir(made_path) == False:
        os.mkdir(made_path)

    return made_path

def input_ext_list(ext_range : int = 10) -> list:
    '''
    ext_range   : Integer number of extensions you can selecet
    list_of_ext : List String extension
    more_file    : String extension
    '''
    if type(ext_range) != int:
        raise TypeError("ext_range must be int type.")
    list_of_ext = []
    for i in range(0, ext_range):
        # Varify message by times.
        if i == 0:
            more_file = input("What filetype (extension)?: ")
        else:
            more_file = input('more filetype?(* or "nothing"): ')
        # Store in a list or not.
        if more_file != "nothing":
            list_of_ext.append(more_file)
        else:
            break
    return list_of_ext

def decide_ext(list_of_ext : list) -> list:
    '''
    list_of_ext  : List String extension
    file_types   : List type of file for choose file in the dialog

    ext          : String extension
    ext_by_semic : String extension in arrangement by semicolon (if Windows)
    ext_by_list  : String extension in arrangement by list (if Mac)
    ext_by_tuple : String extension in arrangement by tuple (if Mac)
    '''
    if type(list_of_ext) != str:
        raise TypeError("list_of_ext must be str type.")
    # Discrimination whether Windows or Mac.
    pf = platform.system()
    # Select extension to choose file
    if pf == 'Windows': # OS is Windows
        # wanted to make like this...  ex. fileTypes = [('data files','*.pdf;*.py')]
        ext_by_semic = ''
        for ext in list_of_ext:
            if ext == list_of_ext[0]:
                ext_by_semic = '*.{ext}'.format(ext=ext)
            else:
                ext_by_semic = ext_by_semic + '{semicolon}*.{ext}'.format(ext=ext,semicolon=';')
        file_types = [('data files', ext_by_semic)]
    elif pf == 'Darwin': # OS is Mac
        # wanted to make like this...  ex. fileTypes = [("csv files","*.csv"),("txt files","*.txt")]
        for ext in list_of_ext:
            ext_by_list  = ['{ext} files'.format(ext=ext),'*.{ext}'.format(ext=ext)]
            ext_by_tuple = tuple(ext_by_list)
            if ext == list_of_ext[0]:
                file_types = [ext_by_tuple]
            else:
                file_types.append(ext_by_tuple)
            # set default "ext_by_tuple"
            ext_by_tuple = ""
    return file_types

def decide_seperator() -> str:
    '''
    pf  : String system name of OS.
    sep : String seperator of directory.
    '''
    # Discrimination whether Windows or Mac.
    pf = platform.system()
    sep = ''
    if pf == 'Windows': # OS is Windows
        sep = '\\'
    elif pf == 'Darwin': # OS is Mac
        sep = '/'
    elif pf == 'Linux': # OS is Ubuntu
        sep = '/'
    else:
        raise OSError("Your OS is unknown.")
    return sep

def move_files(src_paths : list, output_dir : str) -> bool:
    if type(src_paths) != list:
        raise TypeError("src_paths must be list type.")
    if len(src_paths) == 0:
        raise ValueError("Length of src_paths must be more than 0.")
    if type(output_dir) != str:
        raise TypeError("output_dir must be str type.")
    src_dir = str(pathlib.Path(src_paths[0]).parent)
    new_output_dir = f"{src_dir}/{output_dir}"
    new_output_path = pathlib.Path(new_output_dir)
    if new_output_path.exists():
        raise FileExistsError(f"\"{str(new_output_path)}\" exists.")
    new_output_path.mkdir()
    for target_file in src_paths:
        move_file(target_file, str(new_output_path))
    return True

def move_file(src_path : str, dest_path : str) -> bool:
    if type(src_path) != str:
        raise TypeError("src_path must be str type.")
    if type(dest_path) != str:
        raise TypeError("dest_path must be str type.")
    shutil.move(src_path, dest_path)
    return True

def main():
    # test code for DecideSeperator()
    decide_seperator()

if __name__ == "__main__":
    main()
