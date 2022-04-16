# image_editor.py
# code in shift-jis

# Library by default
import os, sys
import math
import subprocess
import pathlib
import shutil
# Library by third party
import cv2
from PIL import Image
# Library by landmasterlibrary
from input_controller import check_whether_sjis_exists, repeat_input_with_multi_choices
from dir_editor import decide_seperator, make_directory, generate_file_name, move_files
sep = decide_seperator() # String seperator of directory.
from file_list_getter import get_file_list
from text_editor import write_text

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

    if type(filename) != str:
        raise TypeError("filename must be str type.")
    if filename[-4:] not in [".jpg", ".png", ".JPG", ".PNG"] and filename[-5:] not in [".jpeg"]:
        raise TypeError("filename must contain image extension.")
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

    sliderTop    = Slider(axTop, 'Top', 0, height - 1, valinit=0, valstep=delta_f)
    sliderBottom = Slider(axBottom, 'Bottom', 0, height - 1, valinit=0, valstep=delta_f)
    sliderLeft   = Slider(axLeft, 'Left', 0, width - 1, valinit=0, valstep=delta_f)
    sliderRight  = Slider(axRight, 'Right', 0, width - 1, valinit=0, valstep=delta_f)

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
    top    = int(sliderTop.val)
    bottom = int(height - sliderBottom.val)
    left   = int(sliderLeft.val)
    right  = int(width - sliderRight.val)

    if top >= bottom:
        raise ValueError("top must be less than bottom.")
    if left >= right:
        raise ValueError("left must be less than right.")

    frame_dict = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    print("FrameSize for trimming is ", frame_dict)
    return frame_dict

def trim_image(target_dir : str, trimmed_img_ext : str = "jpg") -> bool:
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
    if type(target_dir) != str:
        raise TypeError("target_dir must be str type.")
    if type(trimmed_img_ext) != str:
        raise TypeError("trimmed_img_ext must be list type.")
    file_list = get_file_list(target_dir, trimmed_img_ext)

    # Error Handling
    if len(file_list) == 0:
        raise ValueError("ImageEditor exits because of no target files.")
        print('\nImageEditor exits because of no target files.')
        sys.exit(0)

    select_times = repeat_input_with_multi_choices('\nWhat times do you choosing? ("1" or "every"): ', ['1', 'every'])
    extracted_dir = make_directory(file_list[0])

    # Error Handling
    if check_whether_sjis_exists([file_list[0], extracted_dir], __file__) == True:
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

    return True

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
    if check_whether_sjis_exists([folder_list[0], extracted_dir], __file__) == True:
        sys.exit(0)

    # Decide to remove or don't
    execute_mode = repeat_input_with_multi_choices('\nYou wanna Remove or Assessment overlapped images? (R/A)', ['R', 'A'])

    assess_mode = 'N'
    border_line = 70
    list_for_text = []
    message_how_many_matches = "How many matches are required not to remove?(0 to 100) : "
    # compare both image to remove img1 or not
    for i in range(0, len(folder_list) - 1):
        img_name_1 = os.path.splitext(os.path.basename(folder_list[i]))[0]
        img_name_2 = os.path.splitext(os.path.basename(folder_list[i+1]))[0]
        # Decide method of assessment
        while assess_mode != 'F' and assess_mode != 'P':
            assess_mode = repeat_input_with_multi_choices('\nWhich method to assess?\n[ F: FeaturePoint, P: PixelMatch ] : ', ['F', 'P'])
            if execute_mode == 'R':
                if assess_mode == 'F':
                    border_line = repeat_input_with_multi_choices(message_how_many_matches, [0, 100])
                elif assess_mode == 'P':
                    border_line = repeat_input_with_multi_choices(message_how_many_matches, [0, 100])
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
    write_text(generate_file_name(extracted_dir, sep, 'match_rate.txt'), list_for_text)

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
    if type(video_name) != str:
        raise TypeError("video_name must be str type.")
    if video_name == '':
        raise ValueError("No file is selected.")
    if video_name[-4:] not in [".mov", ".mp4"]:
        raise TypeError("video_name must contain video extension.")

    extracted_dir = make_directory(video_name)

    # Error Handling
    if check_whether_sjis_exists([video_name, extracted_dir], __file__) == True:
        raise ValueError("video_name contained s-jis.")

    cap = cv2.VideoCapture(video_name)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
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

def get_times_of_movie_in_folder(dir_full_path : str, movie_file_ext : str = "mov"):
    if type(dir_full_path) != str:
        raise TypeError("dir_full_path must be str type.")
    if type(movie_file_ext) != str:
        raise TypeError("movie_file_ext must be str type.")
    file_list = get_file_list(dir_full_path, movie_file_ext)
    print(file_list)
    total_time = 0
    for file in file_list:
        cap = cv2.VideoCapture(file)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        time = frame_count / fps
        total_time += time

    ONE_HOUR_TO_SECOND = 3600
    ONE_MINUTE_TO_SECOND = 60
    print(total_time)
    hour = math.floor(total_time / ONE_HOUR_TO_SECOND)
    minute = math.floor((total_time - ONE_HOUR_TO_SECOND * hour) / ONE_MINUTE_TO_SECOND)
    second = math.floor(total_time - ONE_HOUR_TO_SECOND * hour - ONE_MINUTE_TO_SECOND * minute)
    total_time_to_display = "{}:{}:{}".format(str(hour), str(minute), str(second))
    print("Total_time is {}".format(total_time_to_display))

def extract_sound_to_text(dir_full_path : str, movie_file_ext : str = "mov"):
    if type(dir_full_path) != str:
        raise TypeError("dir_full_path must be str type.")
    if type(movie_file_ext) != str:
        raise TypeError("movie_file_ext must be str type.")
    file_list = get_file_list(dir_full_path, movie_file_ext)
    dir_name_list = dir_full_path.split("/")
    base_dir_name = dir_name_list[len(dir_name_list) - 1]
    sound_dir_name = "sound"
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    for file_name in file_list:
        # TODO: dir_editor直した後に動作確認
        output_file_name = file_name.replace(f".{movie_file_ext}", ".mp3").replace(base_dir_name, f"{base_dir_name}/{sound_dir_name}")
        cmd = "ffmpeg -i {}  {}".format(file_name, output_file_name)
        print(file_name)
        print(output_file_name)
        print("=========================")
        subprocess.call(cmd, shell=True)

def resize_img(dir_full_path : str, img_file_ext : str = "jpg"):
    if type(dir_full_path) != str:
        raise TypeError("dir_full_path must be str type.")
    if type(img_file_ext) != str:
        raise TypeError("img_file_ext must be str type.")
    # TODO:動くかどうかを確認
    # file_list = get_file_list(dir_full_path, movie_file_ext)
    file_list = get_file_list(dir_full_path, img_file_ext)
    convert_dir = dir_full_path + "convert/"

    for file_name in file_list:
        img = Image.open(file_name)
        img_resize = img.resize((int(img.width / 4), int(img.height / 4)))
        title, ext = os.path.splitext(file_name)
        img_resize.save(convert_dir + os.path.basename(file_name))

def get_statistics(youtube, id : str):
    # if type(youtube) != str:
    #     raise TypeError("youtube must be str type.")
    if type(id) != str:
        raise TypeError("id must be str type.")
    # TODO:動くかどうかを動作確認
    statistics = youtube.videos().list(part="statistics", id=id).execute()["items"][0]["statistics"]
    return statistics

# def get_youtube_statistics():
#     # TODO:動くかどうかを動作確認
#     youtube = build("youtube", "v3", developerKey=settings.APIKEY)

#     search_response = youtube.search().list(
#         part="snippet",
#         maxResults="50",
#         q="python",
#         relevanceLanguage="ja",
#         type="video"
#     ).execute()
#     df = pd.DataFrame()
#     for item in search_response["items"]:
#         statistics = get_statistics(item["id"]["videoId"])
#         se = pd.Series([int(statistics["viewCOunt"]), item["snippet"]["title"]], ["再生回数", "タイトル"])
#         df = df.append(se, ignore_index=True)

#     df_s = df.sort_values("再生回数", "タイトル")
#     print(df_s)

# def does_dir_exist(target_dir : str, target_dir_searched : str):
#     if type(target_dir) != str:
#         raise TypeError("TypeError: target_dir must be str type.")
#     if type(target_dir_searched) != str:
#         raise TypeError("TypeError: target_dir_searched must be str type.")


def convert_image_format(file_name : str, src_ext : str = "png", dest_ext : str = "jpg") -> str:
    if type(file_name) != str:
        raise TypeError("file_name must be str type.")
    # if type(output_dir) != str:
    #     raise TypeError("output_dir must be str type.")
    if type(src_ext) != str:
        raise TypeError("src_ext must be str type.")
    if type(dest_ext) != str:
        raise TypeError("dest_ext must be str type.")
    if f".{src_ext}" not in file_name:
        raise ValueError("ValueError: src_ext must be contained by file_name.")
    file_name_without_ext = file_name.replace(f".{src_ext}", "")
    im = Image.open(f"{file_name_without_ext}.{src_ext}")
    im = im.convert("RGB")
    src_path = f"{file_name_without_ext}.{dest_ext}"
    im.save(src_path)
    # dest_path = f"{str(pathlib.Path(src_path).parent)}/{output_dir}"
    # dest_path = output_dir
    print(str(pathlib.Path(src_path).parent))
    # shutil.move(src_path, dest_path)
    return src_path

def convert_image_format_in_folder(src_dir : str, output_dir : str = "outputs", src_ext : str = "png", dest_ext : str = "jpg") -> bool:
    if type(src_dir) != str:
        raise TypeError("src_dir must be str type.")
    if type(output_dir) != str:
        raise TypeError("output_dir must be str type.")
    if type(src_ext) != str:
        raise TypeError("src_ext must be str type.")
    if type(dest_ext) != str:
        raise TypeError("dest_ext must be str type.")
    # files = get_file_list(folder_dir, src_ext)
    files = get_file_list(src_dir, src_ext)

    converted_image_files = []
    try:
        for file_name in files:
            converted_image_file = convert_image_format(file_name, src_ext, dest_ext)
            converted_image_files.append(converted_image_file)
        move_files(converted_image_files, output_dir)
    except Exception as e_img:
        for image_file in converted_image_files:
            if image_file not in files:
                pathlib.Path(image_file).unlink()
        raise e_img
    return True

def exe_convert_image_format_in_folder():
    args = sys.argv
    convert_image_format_in_folder(str(args[1]))
    # convert_image_format_in_folder(str(args[1]), str(args[2]), str(args[3]))
    return True

def main():
    args = sys.argv

    # # test code for select_area()
    # list_of_ext = ["jpg"]
    # select_area(str(args[1]))

    # test code for trim_image()
    # trim_image('jpg')
    # trim_image(str(args[1]), 'jpg')

    # test code for remove_duplication()
    # file_list = get_file_list(decide_now_dir(),'jpg')
    file_list = get_file_list(str(args[1]),'jpg')
    remove_duplication(file_list)

    # test code for extract_image()
    # list_of_ext = ["mp4"]
    # extract_image(str(args[1]))

    # test code for convert_image_format_in_folder()
    # convert_image_format_in_folder(str(args[1]))
    # convert_image_format_in_folder(str(args[1]), 'png', 'jpg')

if __name__ == "__main__":
    main()
