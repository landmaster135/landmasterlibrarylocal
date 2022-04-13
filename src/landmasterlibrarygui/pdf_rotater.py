# pdf_rotater.py
# code in shift-jis

import os, sys
# IMPORT module FROM LandmasterLibrary
import dir_editor
sep = dir_editor.decide_seperator() # String seperator of directory.
import file_list_getter

def make_vertical(folder_list : list):
    '''
    folderList        : list of file filtered with extension in the selected folder.
    filename          : fullname of selected file.
    original          : PdfFileReader of original files.
    rotated           : PdfFileWriter of rotated files.
    rotated_dir       : path of folder having rotated files.
    sum_page          : sum of page.
    sum_rotating_page : rotating pages. count 1 if make their vertical.
    '''
    # PyPDF2 version is 1.26.0
    from PyPDF2 import PdfFileWriter, PdfFileReader
    if len(folder_list) != 0:
        filename = folder_list[0]
    else:
        print('\nPDFRotater exits because of no target files.')
        sys.exit(0)

    rotated_dir = dir_editor.make_directory(filename)

    for filename in folder_list:
        print("Rotate all page of PDF:", filename)

        original = PdfFileReader(filename)
        rotated  = PdfFileWriter()

        # Display number of pages of original PDF file
        sum_page = original.getNumPages()
        print("page_num: ", sum_page)

        # Count pages at the same time as making vertical.
        sum_rotating_page = 0
        for i in range(0, sum_page, 1):
            print("Page ", i, " is ", original.getPage(i).get('/Rotate'), " degrees rotating")
            angle_rotating = original.getPage(i).get('/Rotate')
            if angle_rotating != 0:
                sum_rotating_page += 1
            rotated.addPage(original.getPage(i).rotateClockwise(360 - angle_rotating))

        # new file entry
        # output_filename = '{dirname}{sep}{basename}'.format(dirname=rotated_dir, sep=sep, basename=os.path.basename(filename))
        output_filename = dir_editor.generate_file_name(rotated_dir, sep, os.path.basename(filename))
        with open(output_filename, "wb") as outputStream:
            rotated.write(outputStream)

        print("\nPDFRotater is terminated.\nsum_rotating_page: ", sum_rotating_page, " / ", sum_page)

    print('\n\nCheck new folder. "{}"'.format(rotated_dir))

def main():
    make_vertical(file_list_getter.get_file_list(dir_editor.decide_now_dir(),'pdf'))

if __name__ == "__main__":
    main()
