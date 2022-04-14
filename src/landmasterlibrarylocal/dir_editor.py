# dir_editor.py
# code in shift-jis

import os, sys, platform
from tkinter import filedialog
# IMPORT module FROM LandmasterLibrary
import input_controller

def decide_save_file_name(dirname : str, list_of_ext : list) -> str:
    '''
    list_of_ext    : List String extension
    dirname        : String absolutely directory of default folder
    save_file_path : String absolutely path of selected file
    '''
    if list_of_ext == []:
        list_of_ext = input_ext_list()
    else:
        pass
    save_file_path = filedialog.asksaveasfilename(filetypes=decide_ext(list_of_ext), initialdir=dirname ,title = "Save As")
    print("File's Absolutely Path: {quotation}{filepath}{quotation}".format(quotation='"',filepath=save_file_path))
    return save_file_path

def generate_file_name(dirname : str, sep : str, filename_with_ext : str) -> str:
    '''
    dirname           : String directory name.
    sep               : String seperator of direcotry.
    filenameWithExt   : String filename with extension. (name of directory is also OK.)
    GeneratedFileName : String FileName Generated in this function.
    '''
    generated_file_name = '{dirname}{sep}{filename}'.format(dirname=dirname,sep=sep,filename=filename_with_ext)
    return generated_file_name

def make_directory(filename : str) -> str:
    '''
    filename  : String fullname of selected file.
    new_name  : String name of folder having rotated files.
    made_path : String path of folder having rotated files.
    '''
    new_name = input("Input a name of new folder: ")
    # made_path = '{dirname}{sep}{newpath}'.format(dirname=os.path.dirname(filename),sep=DecideSeperator(),newpath=new_name)
    made_path = generate_file_name(os.path.dirname(filename), decide_seperator(), new_name)
    while os.path.isdir(made_path) == True:
        new_name = input("That name already exists. Reinput: ")
        # new path entry
        # made_path = '{dirname}{sep}{newpath}'.format(dirname=os.path.dirname(filename),sep=DecideSeperator(),newpath=new_name)
        made_path = generate_file_name(os.path.dirname(filename), decide_seperator(), new_name)

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

def decide_now_file(list_of_ext : list) -> str:
    '''
    list_of_ext   : List String extension
    now_dir       : String absolutely directory of default folder
    now_file_path : String absolutely path of selected file
    '''
    if list_of_ext == []:
        list_of_ext = input_ext_list()
    else:
        pass
    now_dir = os.path.abspath(os.path.dirname(__file__))
    now_file_path = filedialog.askopenfilename(filetypes=decide_ext(list_of_ext), initialdir=now_dir)
    print("File's Absolutely Path: {quotation}{filepath}{quotation}".format(quotation='"',filepath=now_file_path))
    return now_file_path

def decide_now_dir() -> str:
    '''
    now_dir      : String absolutely directory default folder
    now_dir_path : String absolutely path selected folder
    '''
    now_dir = os.path.abspath(os.path.dirname(__file__))
    now_dir_path = filedialog.askdirectory(initialdir=now_dir)

    # Discrimination whether Windows or Mac.
    pf = platform.system()
    if pf == 'Windows': # OS is Windows
        now_dir_path = now_dir_path.replace('/', '\\')
    print("Folder's Absolutely Path: {quotation}{folderpath}{quotation}".format(quotation='"',folderpath=now_dir_path))
    return now_dir_path

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
    return sep

def main():
    # test code for DecideSeperator()
    decide_seperator()

if __name__ == "__main__":
    main()
