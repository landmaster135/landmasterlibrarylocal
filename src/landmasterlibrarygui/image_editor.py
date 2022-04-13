# image_editor.py
# code in shift-jis

import os, sys
import cv2 # opencv 3.4.2
# IMPORT module FROM LandmasterLibrary
import input_controller
import dir_editor
sep = dir_editor.decide_seperator() # String seperator of directory.
import file_list_getter
import text_editor

def select_area(filename : str) -> dict:
    '''
    filename   : String absolutely path of selected file

    img       : PIL.JpegImagePlugin.JpegImageFile
    frameDict  : Dictionary of integer ([top : bottom, left : right])
    '''
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider

    img = Image.open(filename) # this function has no exception handling
    width, height = img.size

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.35)
    plt.xlim(0, width)
    plt.ylim(0, height)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    delta_f = 1.0
    ax.imshow(img, extent=[*xlim, *ylim], aspect='auto')

    # set borderline. (Top and Bottom turn over.)
    borderTop,    = plt.plot([0, width], [0, 0], lw=0.7)
    borderBottom, = plt.plot([0, width], [height, height], lw=0.7)
    borderLeft,   = plt.plot([0, 0], [0, height], lw=0.7)
    borderRight,  = plt.plot([width, width], [0, height], lw=0.7)

    axcolor = 'lightgoldenrodyellow'
    axTop    = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
    axBottom = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    axLeft   = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
    axRight  = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

    sliderTop    = Slider(axTop, 'Top', 0, height/2 - 1, valinit=0, valstep=delta_f)
    sliderBottom = Slider(axBottom, 'Bottom', 0, height/2 - 1, valinit=0, valstep=delta_f)
    sliderLeft   = Slider(axLeft, 'Left', 0, width/2 - 1, valinit=0, valstep=delta_f)
    sliderRight  = Slider(axRight, 'Right', 0, width/2 - 1, valinit=0, valstep=delta_f)

    # image size before trimming
    top    = sliderTop.val
    bottom = height - sliderBottom.val
    left   = sliderLeft.val
    right  = width - sliderRight.val

    def update(val):
        '''
        top    : String number of y-coordinate of top (global variable)
        bottom : String number of y-coordinate of bottom (global variable)
        left   : String number of x-coordinate of left (global variable)
        right  : String number of x-coordinate of right (global variable)
        '''
        global top
        top    = sliderTop.val
        bottom = height - sliderBottom.val
        left   = sliderLeft.val
        right  = width - sliderRight.val
        borderTop.set_ydata([height - top, height - top])
        borderBottom.set_ydata([height - bottom, height - bottom])
        borderLeft.set_xdata([left, left])
        borderRight.set_xdata([right,right])
        fig.canvas.draw_idle()

    # attach a trigger to Slider
    sliderTop.on_changed(update)
    sliderBottom.on_changed(update)
    sliderLeft.on_changed(update)
    sliderRight.on_changed(update)
    plt.show()

    # image size after trimming
    top    = sliderTop.val
    bottom = height - sliderBottom.val
    left   = sliderLeft.val
    right  = width - sliderRight.val

    frame_dict = {'top': int(top), 'bottom': int(bottom), 'left': int(left), 'right': int(right)}
    print("FrameSize for trimming is ", frame_dict)
    return frame_dict

def trim_image(trimmed_img_ext : str = "jpg"):
    '''
    fileList                 : List of file filtered with extension in the selected folder.
    basefilename_without_ext : String name of base file without extension.
    selectTimes              : String of times to input.
    extracted_dir            : String absolutely path of directory has selected file.
    img                      : Dictionary of pixels of image. (img [height] [width] [color channel])
    trimmed_img              : Dictionary of pixels of image.
    trimmed_img_ext          : String of extension of trimmed_img.
    trimmed_img_name         : String of filename of trimmed_img.
    '''
    file_list = file_list_getter.get_file_list(dir_editor.decide_now_dir(),trimmed_img_ext)

    # Error Handling
    if len(file_list) == 0:
        print('\nImageEditor exits because of no target files.')
        sys.exit(0)

    # selectTimes = input('What times do you choosing? ("1" or "every"): ')
    # while selectTimes != '1' and selectTimes != 'every':
    #     selectTimes = input('Retry. ("1" or "every"): ')
    select_times = input_controller.repeat_input_with_multi_choices('\nWhat times do you choosing? ("1" or "every"): ', ['1', 'every'])

    extracted_dir = dir_editor.make_directory(file_list[0])

    # Error Handling
    if input_controller.check_whether_sjis_exists([file_list[0], extracted_dir], __file__) == True:
        sys.exit(0)

    for i in range(0, len(file_list)):
        if select_times == '1':
            if i == 0:
                frameDict = select_area(file_list[i])
        elif select_times == 'every':
            frameDict = select_area(file_list[i])
        # img[top : bottom, left : right]
        img = cv2.imread(file_list[i])
        trimmed_img      = img[frameDict['top'] : frameDict['bottom'], frameDict['left'] : frameDict['right']]
        trimmed_img_name = "image{num:0=3}.{trimmed_img_ext}".format(num=i,trimmed_img_ext=trimmed_img_ext)
        cv2.imwrite("{dirname}{sep}{trimmed_img_name}".format(dirname=extracted_dir,sep=sep,trimmed_img_name=trimmed_img_name), trimmed_img)
        print("saved: {trimmed_img_name}".format(trimmed_img_name=trimmed_img_name))
    print('Check directory "{dirname}"'.format(dirname=extracted_dir))

def judge_match_rate_by_feature_point(file_name_1 : str, file_name_2 : str) -> float:
    '''
    file_name_1   : String absolutely path of selected file
    file_name_2   : String absolutely path of selected file
    img1          : List of pixels of image. (img [height] [width] [color channel])
    img2          : List of pixels of image. (img [height] [width] [color channel])
    ret           : Float
    '''
    processing_method = 99
    if os.path.splitext(os.path.basename(file_name_1))[1] == '.DS_Store':
        while processing_method != 0 and processing_method != 10000:
            processing_method = int(input('This is not image. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processing_method
    if os.path.splitext(os.path.basename(file_name_2))[1] == '.DS_Store':
        while processing_method != 0 and processing_method != 10000:
            processing_method = int(input('This is not image. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processing_method
    # Grayscale is more correctly than RGB: 3 channel.
    img1 = cv2.imread(file_name_1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(file_name_2, cv2.IMREAD_GRAYSCALE)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (img1_kp, img1_des) = detector.detectAndCompute(img1, None)
    try:
        (img2_kp, img2_des) = detector.detectAndCompute(img2, None)
        matches = bf.match(img1_des, img2_des)
        dist = [m.distance for m in matches]
        similarity = sum(dist) / len(dist)
    except cv2.error:
        while processing_method != 0 and processing_method != 10000:
            processing_method = int(input('cv2.error occured. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processing_method
    except ZeroDivisionError:
        while processing_method != 0 and processing_method != 10000:
            processing_method = int(input('ZeroDivisionError occured. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processing_method

    return similarity

def judge_match_rate_by_pixel_match(file_name_1 : str, file_name_2 : str) -> float:
    '''
    file_name_1   : String absolutely path of selected file
    file_name_2   : String absolutely path of selected file
    color_mode    : Integer color mode for cv2.imread
    img1          : List of pixels of image. (img [height] [width] [color channel])
    img2          : List of pixels of image. (img [height] [width] [color channel])
    match_count   : Integer number of matching between img1 and img2
    num_all_pixel : Integer number of all pixels
    match_rate    : Float rate
    '''
    color_mode = cv2.IMREAD_GRAYSCALE
    # coloeMode = 1
    img1 = cv2.imread(file_name_1, color_mode) # 2nd variable =0: monochrome, >0: 3 channel, <0: original
    img2 = cv2.imread(file_name_2, color_mode)
    match_count = 0
    if len(img1) == len(img2):
        # j: pixels in the height, k: pixels in the width
        for j in range(0, len(img1)):
            for k in range(0, len(img1[j])):
                if color_mode == cv2.IMREAD_GRAYSCALE:
                    # judge by shading whether they match or not
                    if img1[j][k] == img2[j][k]:
                        match_count = match_count + 1
                elif color_mode == 1:
                    # judge by color whether they match or not
                    for m in range(0, len(img1[j][k])): # 3
                        if img1[j][k][m] != img2[j][k][m]:
                            break
                        if m == 2:
                            match_count = match_count + 1
    num_all_pixel = len(img1) * len(img1[0])
    match_rate = match_count/num_all_pixel

    return match_rate

def remove_duplication(folder_list : list):
    '''
    folder_list   : List String absolutely path, of file filtered with extension in the selected folder.
    extracted_dir : String absolutely path of directory has selected file
    match_rate    : Float rate
    border_line   : border line
    '''
    if len(folder_list) == 0:
        print('\nImageEditor exits because of no target files.')
        sys.exit(0)

    extracted_dir = os.path.dirname(folder_list[0])

    # Error Handling
    if input_controller.check_whether_sjis_exists([folder_list[0], extracted_dir], __file__) == True:
        sys.exit(0)

    # Decide to remove or don't
    execute_mode = input_controller.repeat_input_with_multi_choices('\nYou wanna Remove or Assessment overlapped images? (R/A)', ['R', 'A'])

    assess_mode = 'N'
    border_line = 70
    list_for_text = []
    # compare both image to remove img1 or not
    for i in range(0, len(folder_list) - 1):
        img_name_1 = os.path.splitext(os.path.basename(folder_list[i]))[0]
        img_name_2 = os.path.splitext(os.path.basename(folder_list[i+1]))[0]
        # Decide method of assessment
        while assess_mode != 'F' and assess_mode != 'P':
            assess_mode = input_controller.repeat_input_with_multi_choices('\nWhich method to assess?\n[ F: FeaturePoint, P: PixelMatch ] : ', ['F', 'P'])
            if execute_mode == 'R':
                if assess_mode == 'F':
                    border_line = input_controller.repeat_input_with_multi_choices('How many matches are required not to remove? : ', [0, 100])
                elif assess_mode == 'P':
                    border_line = input_controller.repeat_input_with_multi_choices('How many matches are required to remove? : ', [0, 100])
            elif execute_mode == 'S':
                pass
        # do assessment
        if assess_mode == 'F':
            match_rate = judge_match_rate_by_feature_point(folder_list[i], folder_list[i+1])
            match_rate = int(match_rate * 100)
            print('degree of similarity between "{img_name_1}" and "{img_name_2}" is {rate}'.format(img_name_1=img_name_1,img_name_2=img_name_2,rate=match_rate))
        elif assess_mode == 'P':
            match_rate = judge_match_rate_by_pixel_match(folder_list[i], folder_list[i+1])
            match_rate = int(match_rate * 100)
            print('match rate between "{img_name_1}" and "{img_name_2}" is {rate}'.format(img_name_1=img_name_1,img_name_2=img_name_2,rate=match_rate))
        list_for_text.append('"{img_name_1}" and "{img_name_2}" is {rate}'.format(img_name_1=img_name_1,img_name_2=img_name_2,rate=match_rate))
        # Remove files
        if execute_mode == 'R':
            if assess_mode == 'F':
                if match_rate <= border_line:
                    os.remove(folder_list[i])
            elif assess_mode == 'P':
                if match_rate >= border_line:
                    os.remove(folder_list[i])
    # write to .txt file
    text_editor.write_text(dir_editor.generate_file_name(extracted_dir, sep, 'match_rate.txt'), list_for_text)

    print('RemoveDuplication is terminated.\nCheck directory "{dirname}"'.format(dirname=extracted_dir))

def extract_image(video_name : str):
    '''
    video_name    : String absolutely path of selected file
    extracted_dir : String absolutely path of directory has selected file
    frame_count   : Integer number of frame of selected video
    fps           : Integer number of fps of selected video
    num_of_image  : Integer number of extracted images from video
    '''
    # Error Handling
    if video_name == '':
        print("ERROR: No file is selected.")
        sys.exit(0)

    extracted_dir = dir_editor.make_directory(video_name)

    # Error Handling
    if input_controller.check_whether_sjis_exists([video_name, extracted_dir], __file__) == True:
        sys.exit(0)

    cap = cv2.VideoCapture(video_name)
    # width
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # number of frame
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("movie's width: ", width, ", height: ", height)

    for num_of_image in range(1, int(frame_count), int(fps)):
        # set a property, where frame in this case, in the VideoCapture
        cap.set(cv2.CAP_PROP_POS_FRAMES, num_of_image)
        # read the next video frame to extract image file ("cap.read()[1]" is arrays of image's pixels.)
        cv2.imwrite("{dirname}{sep}image{num:0=3}.jpg".format(dirname=extracted_dir,sep=sep,num=int((num_of_image-1)/int(fps))), cap.read()[1])
        # cv2.imwrite("{video_dir}image{:0=3}.jpg".format(int((num_of_image-1)/int(fps))), cap.read()[1])
        print("saved: image{num:0=3}.jpg".format(num=int((num_of_image-1)/int(fps))))
    print('Check directory "{dirname}"'.format(dirname=extracted_dir))
    cap.release()

def main():
    # # test code for select_area()
    # list_of_ext = ["jpg"]
    # select_area(dir_editor.decide_now_file(list_of_ext))

    # test code for trim_image()
    # trim_image('jpg')

    # test code for remove_duplication()
    file_list = file_list_getter.get_file_list(dir_editor.decide_now_dir(),'jpg')
    remove_duplication(file_list)

    # test code for extract_image()
    # list_of_ext = ["mp4"]
    # extract_image(dir_editor.decide_now_file(list_of_ext))

if __name__ == "__main__":
    main()
