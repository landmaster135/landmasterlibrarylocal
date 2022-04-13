# input_controller.py
# code in shift-jis

import os, sys
import re # regular expression

def check_whether_sjis_exists(target_str_list : list, callingfilename_with_ext : str) -> bool:
    '''
    target_str_list          : String List target for check.
    callingfilename_with_ext : String absolutely name of calling file with extension
    checkStr                 : String filter for check.
    isSjisContained          : Boolean.
    basefilename_without_ext : String name of calling file without extension.
    '''
    check_str = re.compile('[\\a-zA-Z0-9\-\_\.\-\s\:\~\^\=]+')
    is_sjis_contained = False
    for i in target_str_list:
        if check_str.fullmatch(i) == None:
            is_sjis_contained = True
        print('\nCheckWhetherSjisExists : targetStr is "{}" ・・・・・・ isSjisContained == {}'.format(i, is_sjis_contained))

    basefilename_without_ext = os.path.splitext(os.path.basename(callingfilename_with_ext))[0]
    if is_sjis_contained == True:
        print('\n\n{} exits because of the directory containing shift-jis character.'.format(basefilename_without_ext))
        return True
    return False

def repeat_input_with_multi_choices(first_message : str, choice_list : list = []) -> str:
    '''
    first_message    : String message for the first input.
    choice_list      : List of String choice.
    is_input_correct : Boolean input is correct or not.
    is_first_input   : Boolean this input is the first time or not.
    input_message    : String message for input.
    input_chr        : String input character.
    '''
    is_input_correct = False
    is_first_input   = True
    input_message   = ''
    input_chr       = ''
    while is_input_correct == False:
        if is_first_input == True:
            # Create message for the first input.
            input_message = first_message
        else:
            # Create message.
            input_message = 'Retry.'
            if choice_list == []:
                pass
            else:
                input_message += ' [ "'
                for i in range(0, len(choice_list)):
                    if i == 0:
                        input_message += '{choice}"'.format(choice=choice_list[i])
                    else:
                        input_message += ' or "{choice}"'.format(choice=choice_list[i])
                input_message += ' ]: '
        input_chr = input(input_message)
        # Check by message.
        if input_chr == '':
            pass
        else:
            if type(choice_list[0]) is int:
                if int(input_chr) >= 0 and int(input_chr) <= 100:
                    is_input_correct = True
                    input_chr = int(input_chr)
                else:
                    pass
            elif type(choice_list[0]) is str:
                if choice_list == []:
                    is_input_correct = True
                else:
                    for choice in choice_list:
                        if input_chr == choice:
                            is_input_correct = True
                            break
        is_first_input = False
    return input_chr

def main():
    # test code for RepeatInputWithMultiChoices()
    repeat_input_with_multi_choices()

if __name__ == "__main__":
    main()
