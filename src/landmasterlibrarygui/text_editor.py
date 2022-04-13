# text_editor.py
# code in shift-jis

import os, sys, platform
# IMPORT module FROM LandmasterLibrary
import input_controller
import dir_editor
sep = dir_editor.decide_seperator() # String seperator of directory.

def write_playlist(file_name : str, extracted_dir : str, playlist_type : str):
    '''
    file_name     : String absolutely filename of target file.
    extracted_dir : String directory to save file exported extracted data.
    playlist_type : String type of Playlist.
    head_windows  : String directory of music you wanna listen to in Windows. Edit suitably.
    head_walkman  : String directory of music you wanna listen to in Walkman. Edit suitably.
    head_android  : String directory of music you wanna listen to in Android. Edit suitably.
    data_line     : String text data for playlist.
    head_dict     : Dictionary of String directory of music you wanna listen to.
    ext_dict      : Dictionary of String extension of a file of playlist.
    sep_dict      : Dictionary of String seperator for playlist.
    export_name   : String absolutely filename to export.
    '''

    head_windows = 'C:\\Users\\Riku\\Music\\MusicBee\\Music\\'
    head_walkman = '#EXTINF:,\n'
    head_android = '/sdcard/Music/Musik/'
    data_line    = ''

    head_dict = {'0': head_windows, '1': head_walkman, '2': head_android}
    ext_dict  = {'0': '.m3u', '1': '.M3U8', '2': '.m3u'}
    sep_dict  = {'0': '\\',   '1': '/',     '2': '/'}

    with open(file_name, encoding="utf-8") as f: # ファイルを読み込み
        data_line = f.read()

    data_line = data_line.replace("\n", "\n{}".format(head_dict[playlist_type])) # テキストデータ内の先頭のパスを編集
    data_line = data_line.replace('\\', sep_dict[playlist_type])                 # テキストデータ内の区切り文字を編集
    data_line = head_dict[playlist_type] + data_line                             # テキストデータ内の1行目の先頭のパスを編集
    # only Walkman.
    if playlist_type == '1':
        data_line = '#EXTM3U\n' + data_line

    export_name = dir_editor.generate_file_name(extracted_dir, sep, os.path.basename(file_name).replace('.txt', ext_dict[playlist_type]))
    with open(export_name, mode="w", encoding="utf-8") as f:
        f.write(data_line)


def write_csv(target_file, target_list):
    '''
    target_file : String absolutely filename of target file.
    target_list : List of contents to write.
    '''
    # write 1 line.
    with open(target_file, mode='a') as f:
        for m in range(0, len(target_list)):
            # memorize to "should_not_exist_yubin.csv" sheet
            if m != len(target_list) - 1:
                f.write("%s," % target_list[m])
            else:
                f.write("%s" % target_list[m])
        f.write("\n")

def write_text(file_name, now_list):
    '''
    file_name : String absolutely path of selected file
    now_list  : List of statement to write
    '''
    with open(file_name, 'w') as f:
        for n in now_list:
            f.write("%s\n" % n)

def main():
    # test code for WriteText()
    write_text(dir_editor.decide_now_dir(), ['apple', 'banana', 'orange'])

if __name__ == "__main__":
    main()
