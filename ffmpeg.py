import subprocess
import os
import time
import shlex
import json


def Main():
    print(("""
    
___  ___          _       ______         _____          _____ 
|  \/  |         | |      | ___ \       |  _  |        |  _  |
| .  . | __ _  __| | ___  | |_/ /_   _  | | | |_      _| | | |
| |\/| |/ _` |/ _` |/ _ \ | ___ \ | | | | | | \ \ /\ / / | | |
| |  | | (_| | (_| |  __/ | |_/ / |_| | \ \_/ /\ V  V /\ \_/ /
\_|  |_/\__,_|\__,_|\___| \____/ \__, |  \___/  \_/\_/  \___/  
                                  __/ |                                              
                                 |___/                                               
    """))
    print('1. Rotate Video')
    print('2. to webm (4chan)')
    print('3. video to 60fps')
    print('4. batch convert')
    option_select = input('Please Select an Option: ')
    if option_select == '1':
        Rotate_video()
    elif option_select == '2':
        to_4chan_webm()
    elif option_select == '3':
        to_60_fps()
    elif option_select == '4':
        batch_convert_option_select = input(
            '1. batch convert 60 fps\n2. batch convert filetype\n')
        if batch_convert_option_select[0] == '1':
            batch_convert_60fps()
        elif batch_convert_option_select[0] == '2':
            batch_convert_webm()
        else:
            print('\nPlease select a valid option next time!\n')
    else:
        print('\nPlease select a valid option next time!\n')
        time.sleep(1)
        Main()


def Rotate_video():
    drive_var_input = input(
        str('Please enter the directory you are in (Example: X:\\tik-tok-master\\uhyuhck)\n'
            ))
    os.chdir(drive_var_input)
    Repeat_var = True
    while Repeat_var == True:
        video_id = input(str('Please enter the video name or ID: '))
        transpose_var_input = input(
            'Please enter your transpose var\n0. 90CounterCLockwise and Vertical Flip\n1. 90Clockwise\n2. 90CounterClockwise\n3. 90Clockwise and Vertical Flip\n4. 180 Degrees\n5. Horizontal Flip (mirror)\n'
        )
        if transpose_var_input == '1':
            transpose_var = 'transpose=1'
        elif transpose_var_input == '2':
            transpose_var = 'transpose=2'
        elif transpose_var_input == '3':
            transpose_var = 'transpose=3'
        elif transpose_var_input == '4':
            transpose_var = 'transpose=2,transpose=2'
        elif transpose_var_input == '5':
            transpose_var = 'hflip'
        else:
            print('Please enter a valid option next time!')
        if ".mp4" not in video_id or ".webm" not in video_id:
            video_id = Find_video_from_id(video_id, drive_var_input)
        video_id_input, video_file_extension = Split_video_parts(video_id)
        video_bitrate = Find_video_bitrate(
            str(drive_var_input) + "\\" + str(video_id))
        rotate_process = subprocess.Popen([
            "ffmpeg", "-i", video_id, "-b:v", video_bitrate + "M", "-vf", transpose_var, video_id_input + "_rot" + video_file_extension
        ])
        rotate_process.wait()
        print('\nffmpeg process complete!')
        convert_another = input('Would you like to convert another? (y/n) ')
        if convert_another[0] == 'y':
            pass
        else:
            Repeat_var = False


def to_60_fps():
    drive_var_input = input(
        'Please enter the directory you are in (Example: X:\\tik-tok-master\\uhyuhck)\n'
    )
    os.chdir(drive_var_input)
    Repeat_var = True
    while Repeat_var == True:
        video_id = input('Please enter the video name or ID: ')
        if ".mp4" not in video_id or ".webm" not in video_id:
            video_id = Find_video_from_id(video_id, drive_var_input)
        video_id_input, video_file_extension = Split_video_parts(video_id)
        video_bitrate = Find_video_bitrate(
            str(drive_var_input) + "\\" + str(video_id))
        fps_60_process = subprocess.Popen([
            "ffmpeg", "-i", video_id_input + video_file_extension, "-b:v",
            video_bitrate + "M", "-filter:v",
            "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
            video_id_input + "_60fps" + video_file_extension
        ])
        fps_60_process.wait()
        print('\nffmpeg process complete!')
        convert_another = input('Would you like to convert another? (y/n) ')
        if convert_another[0] == 'y':
            pass
        else:
            Repeat_var = False


def to_4chan_webm():
    drive_var_input = input(
        'Please enter the directory you are in (Example: X:\\tik-tok-master\\uhyuhck)\n'
    )
    os.chdir(drive_var_input)
    Repeat_var = True
    conversion_size_boolean = True
    ask_for_original_bitrate_boolean = True
    while Repeat_var == True:
        video_id = input('Please enter the video name or ID: ')
        if ".mp4" not in video_id or ".webm" not in video_id:
            video_id = Find_video_from_id(video_id, drive_var_input)
        video_id_input, video_file_extension = Split_video_parts(video_id)
        custom_name_input_option = input(
            'Would you like to set a custom output file name?\n1. yes\n2. no\n'
        )
        if custom_name_input_option == '1':
            custom_name_input = input(
                'What would you like the filename to be (without the extension) '
            )
            video_id_output = custom_name_input
        else:
            video_id_output = video_id_input
        while ask_for_original_bitrate_boolean == True:
            ask_for_original_bitrate = input(
                'Would you like to try to use the original bitrate?\n1. yes\n2. no\n'
            )
            if ask_for_original_bitrate[0] == '1' or ask_for_original_bitrate[
                    0] == 'y':
                video_bitrate = Find_video_bitrate(drive_var_input + "\\" +
                                                   video_id_input +
                                                   video_file_extension)
                to_webm_process = subprocess.Popen([
                    "ffmpeg", "-i", video_id_input + video_file_extension,
                    "-b:v", video_bitrate + "M", "-c:v", "libvpx", "-c:a",
                    "libvorbis", video_id_output + ".webm", "-y"
                ])
                to_webm_process.wait()
                try_again_input = input(
                    'did you file come out to the desired filesize?\n1. yes\n2. no\n'
                )
                if try_again_input[0] == '1' or try_again_input[0] == 'y':
                    conversion_size_boolean = False
                    break
                else:
                    break
            else:
                ask_for_original_bitrate_boolean = False
                break
        while conversion_size_boolean == True:
            bitrate_input = input(
                'Please insert your bitrate (without the M) (example: 1.5) ')
            to_webm_process = subprocess.Popen([
                "ffmpeg", "-i", video_id_input + video_file_extension, "-b:v",
                bitrate_input + "M", "-c:v", "libvpx", "-c:a", "libvorbis",
                video_id_output + ".webm", "-y"
            ])
            to_webm_process.wait()
            try_again_input = input(
                'did you file come out to the desired filesize?\n1. yes\n2. no\n'
            )
            if try_again_input[0] == '1' or try_again_input[0] == 'y':
                conversion_size_boolean == False
                break
            else:
                pass
        print('\nffmpeg process complete!')
        convert_another = input('Would you like to convert another? (y/n) ')
        if convert_another[0] == 'y':
            pass
        else:
            Repeat_var = False


def batch_convert_60fps():
    drive_var_input = input(
        'Please enter the directory you are in (Example: X:\\tik-tok-master\\uhyuhck)\n'
    )
    os.chdir(drive_var_input)
    names_list = os.listdir(drive_var_input)
    for video_id in names_list:
        video_bitrate = Find_video_bitrate(drive_var_input + "\\" + video_id)
        video_name_without_extension, video_file_extension = Split_video_parts(
            video_id)
        if "_60fps" in video_name_without_extension or check_60fps_video_exists(drive_var_input, video_name_without_extension, video_file_extension) == True:
            print('This video already has a 60fps tag! (not converting)')
        else:
            batch_convert_subprocess = subprocess.Popen([
                "ffmpeg", "-i",
                video_name_without_extension + video_file_extension,
                "-filter:v",
                "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1",
                "-b:v", video_bitrate + "M",
                video_name_without_extension + "_60fps" + video_file_extension
            ])
            batch_convert_subprocess.wait()
    print('\nConversions Complete!')


def batch_convert_webm():
    drive_var_input = input(
        'Please enter the directory you are in (Example: X:\\tik-tok-master\\uhyuhck)\n'
    )
    os.chdir(drive_var_input)
    names_list = os.listdir(drive_var_input)
    desired_file_extension_input = input(
        'Please input your desired file extension(output): ')
    if "." in desired_file_extension_input:
        desired_file_extension = desired_file_extension_input
    else:
        desired_file_extension = "." + desired_file_extension_input
    for video_id in names_list:
        video_bitrate = Find_video_bitrate(drive_var_input + "\\" + video_id)
        video_name_without_extension, video_file_extension = Split_video_parts(
            video_id)
        batch_convert_subprocess = subprocess.Popen([
            "ffmpeg", "-i",
            video_name_without_extension + video_file_extension, "-c:v",
            "libvpx", "-b:v", video_bitrate + "M", "-c:a", "libvorbis",
            video_name_without_extension + desired_file_extension
        ])
        batch_convert_subprocess.wait()
    print('\nConversions Complete!')


def Find_video_bitrate(pathToInputVideo):
    temp_bitrate_list = []
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)
    video_bitrate_1 = ffprobeOutput['streams'][0]['bit_rate']
    video_bitrate_2 = ffprobeOutput['streams'][-1]['bit_rate']
    temp_bitrate_list.append(float(video_bitrate_1))
    temp_bitrate_list.append(float(video_bitrate_2))
    video_bitrate = max(temp_bitrate_list)
    video_bitrate = float(video_bitrate) / 1000000
    return str(video_bitrate)


def Find_video_from_id(video_id, folder_directory):
    file_list = os.listdir(folder_directory)
    print("You did not include the file extension. Searching...")
    for file_names in file_list:
        if video_id in file_names:
            video_id_final = file_names
            print('File was found! [' + video_id_final + ']')
	
    return str(video_id_final)


def Split_video_parts(video_id):
    video_file_extension = "." + (video_id.split('.')[-1])
    video_id_input = ('.').join(video_id.split('.')[:-1])
    return video_id_input, video_file_extension

def check_60fps_video_exists(folder_directory, video_name_without_extension, video_file_extension):
	file_list = os.listdir(folder_directory)
	video_id_60 = video_name_without_extension + "_60fps" + video_file_extension
	if video_id_60 in file_list:
		print('This video already has a 60fps tag! (not converting)')
		return True
	else:
		return False
Main()
