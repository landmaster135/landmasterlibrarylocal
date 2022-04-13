# file_list_getter.py
# code in shift-jis

import glob2
import os, sys, platform
import time
# IMPORT module FROM LandmasterLibrary
import input_controller
import dir_editor
sep = dir_editor.decide_seperator() # String seperator of directory.
import text_editor

def extract_playlist_from_text(file_list : list):
    '''
    folder_list   : List of file filtered with extension in the selected folder.
    file_name     : String absolutely filename.
    extracted_dir : String directory to save file exported extracted data.
    input_message : String message at the time of inputting type of file.
    playlist_type : String type of playlist.
    type_list     : List of String.
    '''
    if len(file_list) != 0:
        file_name = file_list[0]
    else:
        print('\nfile_list_getter.extract_playlist exits because of no target files.')
        sys.exit(0)

    extracted_dir = dir_editor.make_directory(file_name)

    input_message = 'Select type of playlist.\n[ 0: Windows, 1: Walkman, 2: Android ]'
    playlist_type = input_controller.repeat_input_with_multi_choices(input_message, ['0', '1', '2'])
    type_list     = {'0': 'Windows', '1': 'Walkman', '2': 'Android'}
    print('You selected for "{}"'.format(type_list[playlist_type]))

    # --- memorandum ---
    # os.chdir(os.path.dirname(os.path.abspath(__file__))) # 実行ファイルのディレクトリに移動
    # if fileName[:-4] != '.txt':
    #     fileName = input('それでは、基となるテキストファイル名を入力して下さい。')

    for file_name in file_list:
        text_editor.write_playlist(file_name, extracted_dir, playlist_type)

    print('FileListGetter.extract_playlist is terminated.')
    print('Check directory "{dirname}"'.format(dirname=extracted_dir))

def extract_file_name_book(dir_full_path : str):
    '''
    now_dir          : String name of now direcotry.
    file_list        : List of String filename.
    fileName       : String exported filename.
    export_file_name : String exported absolutely filename.
    data_list_exp    : List to export as CSV.           [[], [], ...]
    data_list        : List to memorize to dataListEXP. [, , ...]
    time_mod         : String data of date and time.
    '''
    # now_dir          = dir_editor.decide_now_dir()
    now_dir          = dir_full_path
    file_list        = get_file_list(now_dir, dir_editor.input_ext_list(ext_range=1)[0])
    export_file_name = dir_editor.decide_save_file_name(now_dir, ["csv"])

    data_list_exp = []
    date_format = '%Y/%m/%d %H:%M:%S' # 日付の出力用
    for f in file_list:
        data_list = []
        # get date and time this file is updated
        time_mod = time.strftime(date_format,time.localtime(os.path.getmtime(f)))
        data_list.append(f)
        data_list.append(time_mod)
        data_list_exp.append(data_list)
    for data in data_list_exp:
        text_editor.write_csv(export_file_name, data)

    print('extract_file_name_book is terminated.')
    print('Check directory "{dirname}"'.format(dirname=export_file_name))

def confirm_execution(target : str, replace : str) -> str:
    '''
    target               : String character you wanna delete or replace from.
    replace              : String character you wanna add or replace to.
    input_message        : String message for first input.
    execute_confirmation : String Yes or No. [ 'y' / 'n' ]
    '''
    input_message        = ''
    execute_confirmation = ''
    if target == '' and replace == '':
        print('Nothing to edit fileName.')
        return 'n'
    elif target == '':
        input_message = 'I will add with "{replace}", OK? [ y / n ] : '.format(replace=replace)
    elif replace == '':
        input_message = 'I will delete "{target}", OK? [ y / n ] : '.format(target=target)
    else:
        input_message = 'I will rename {target} → {replace}, OK? [ y / n ] : '.format(target=target,replace=replace)
    execute_confirmation = input_controller.repeat_input_with_multi_choices(input_message, ['y', 'n'])
    return execute_confirmation

def edit_file_name(dir_full_path : str):
    '''
    sep                           : String sperator of directory. It varies by os platform.
    ext                           : String extension.
    file_list                     : List, String absolutely path, of file filtered with extension in the selected folder.
    mode_selected                 : String selected mode.
    mode_dict_declare             : Dictionary of String to declare current mode.
    mode_dict_message_for_target  : Dictionary of String message for inputting target character in current mode.
    mode_dict_message_for_replace : Dictionary of String message for inputting replace character in current mode.
    input_message                 : String message for input.
    forward_or_back               : String which point do you input new character, Forward or Back. [ 'F' / 'B' ]
    target_character_alignment    : String character you wanna delete or replace from.
    replace_character_alignment   : String character you wanna add or replace to.
    execute_confirmation          : String Yes or No. [ 'y' / 'n' ]
    after_replace_name            : String replaced filename. (only filename)
    target_file_name              : String absolutely target filename.
    replace_file_name             : String absolutely replaced filename.
    '''
    ext = input('What Extension? (without ".") : ')
    now_dir = dir_editor.decide_now_dir()
    # now_dir = dir_full_path
    file_list = get_file_list(now_dir, ext)
    input_message = 'Select mode. [ A: Add, D: Delete, R: Replace, E: Exit ]'
    mode_selected = input_controller.repeat_input_with_multi_choices(input_message, ['A', 'D', 'R', 'E'])
    if mode_selected == 'E':
        print('Exit.')
        sys.exit(0)

    target_character_alignment  = ''
    replace_character_alignment = ''
    mode_dict_declare             = {'A': '--- Add mode ---', 'D': '--- Delete mode ---', 'R': '--- Replace mode ---'}
    mode_dict_message_for_target  = {'A': '', 'D': 'What character do you wanna delete? : ', 'R': 'What character do you wanna edit?\n(You should copy character from target file.) : '}
    mode_dict_message_for_replace = {'A': 'What character do you wanna add with? : ', 'D': '', 'R': 'What character do you wanna edit with? : '}
    print(mode_dict_declare[mode_selected])
    if mode_selected == 'A':
        # F : edit by using directory's seperator, B : edit by using extension's dot.
        input_message  = 'Which point do you wanna edit, Forward or Back? [ F / B ] : '
        forward_or_back = input_controller.repeat_input_with_multi_choices(input_message, ['F', 'B'])
    try:
        if mode_selected != 'A':
            target_character_alignment  = input(mode_dict_message_for_target[mode_selected])
        if mode_selected != 'D':
            replace_character_alignment = input(mode_dict_message_for_replace[mode_selected])
        execute_confirmation = confirm_execution(target_character_alignment, replace_character_alignment)
    except KeyError:
        print('Error. Exit.')
        sys.exit(0)

    if execute_confirmation == 'y':
        for i in file_list:
            after_replace_name = ''
            if mode_selected == 'A':
                if forward_or_back == 'F':
                    after_replace_name = replace_character_alignment + os.path.splitext(os.path.basename(i))[0]
                elif forward_or_back == 'B':
                    after_replace_name = os.path.splitext(os.path.basename(i))[0] + replace_character_alignment
            elif mode_selected == 'D' or mode_selected == 'R':
                after_replace_name = os.path.splitext(os.path.basename(i))[0].replace(target_character_alignment, replace_character_alignment)
            target_file_name  = i
            replace_file_name = dir_editor.generate_file_name(os.path.dirname(i), sep, '{filename}.{ext}'.format(filename=after_replace_name, ext=ext))
            os.rename(target_file_name, replace_file_name)
    else:
        sys.exit(0)

def get_file_list(folder_dir : str, ext : str) -> list:
    '''
    folder_dir  : String selected folder's absolutely directory.
    ext         : String extension
    folder_list : List about selected folder
    '''

    if folder_dir == '':
        print("ERROR: No directory is selected.")
        sys.exit(0)

    folder_list = glob2.glob(dir_editor.generate_file_name(folder_dir, sep, '*.{ext}'.format(ext=ext)))

    # sort order of list is irregulary if you use "glob"
    list.sort(folder_list, reverse=False)
    print('Get file list in this folder.\n"', folder_dir, '"\n\n........................\n')
    # Get list about files.
    for file in folder_list:
        print(file)
    return folder_list

def main():
    # # test code for extract_playlist()
    # extract_playlist(get_file_list(dir_editor.decide_now_dir(),'txt'))

    # # test code for extract_file_name_book()
    extract_file_name_book(dir_editor.decide_now_dir())

    # # test code for confirm_execution()
    # confirm_execution('a', 'b')

    # test code for edit_file_name()
    # edit_file_name(dir_editor.decide_now_dir())

    # # test code for get_file_list()
    # get_file_list(dir_editor.decide_now_dir(), 'jpg')

if __name__ == "__main__":
    main()
