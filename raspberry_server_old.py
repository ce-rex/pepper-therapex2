import os
import socket
import time
import json
from threading import Thread
from exercise_manager import ExerciseManager

# import tkinter as tk
# from PIL import ImageTk, Image

# copy to raspi
# scp -r /Users/clara/TUMaster/8_WS2021/ProjektMedInf/pepper-therapex2 pi@raspberrypi.local:/home/pi/Desktop/

# setup udp-server
ip = "raspberrypi.local"  # change to IP to the raspberry or to the pc with slideshow.py
port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

exercise_manager = ExerciseManager()

print("I'm running from /home/pi/.config/autostart/pepper_therapex_study.desktop")


# run udp-server
def udp_rec(ex_man):
    timeout = 5
    ready = True
    # test_data = [[63, 435, 62, 64], [61, 378, 62, 63]]
    test_data = [[63, 435], [61, 378]]
    headers = ['time', 'BPM', 'pulse_data', 'resting_BPM', 'exercise_intensity']
    data_saver = None
    session_num = 1

    counter = 0

    print("starting to listen")
    while True:
        try:
            # ready = select.select([sock], [], [], timeout)
            if ready:
                msg, source_address = sock.recvfrom(1024)
                # print(msg)
                # print(source_address)
                # what data does the client send/need?

                if msg == b'newsession':
                    # create new recording file
                    exercise_manager.start_new_session()
                    print(msg)

                elif msg == b'data':
                    print(msg)
                    # reply with bpm, pulse, resting_bpm, last20_bpm?
                    exercise_manager.update_data()
                    response = json.dumps(test_data[counter])
                    print(response)
                    sock.sendto(response.encode(), source_address)

                elif msg == b'calibration':
                    exercise_manager.start_calibration()

                    response = "started calibration process!"
                    sock.sendto(response.encode(), source_address)

                elif msg == b'exercise':
                    response = exercise_manager.get_exercise_intensity()
                    sock.sendto(response.encode(), source_address)

                elif msg == b'start':
                    # save session
                    exercise_manager.start_new_experiment_cycle()

                    response = "started exercise cycle!"
                    sock.sendto(response.encode(), source_address)

                elif msg == b'done':
                    # save session
                    exercise_manager.save_session_data()

                    response = "stopped exercise cycle!"
                    sock.sendto(response.encode(), source_address)

                else:
                    print("unknown request")
                # print("received message:", data, "from:", addr)

                # # set max slides and wav
                # if current_slide >= 18:
                #     current_slide = 18
                #
                # if current_wav >= 22:
                #     current_wav = 22
                #
                # if current_wav_loop >= 3:
                #     current_wav_loop = 3
                #
                # # play certain wav
                # if data[-4:] == b".wav":
                #     wav_number = data[:-4]
                #     print(data)
                #     print(data[:-4])
                #     print(wav_number)
                #     thread_play_sound = Thread(target=play_sound, args=[int(wav_number)])
                #     thread_play_sound.start()
                #
                # # show certain slide
                # if data[-4:] == b".jpg" or data[-4:] == b".JPG":
                #     jpg_number = data[:-4]
                #     print(data)
                #     print(data[:-4])
                #     print(jpg_number)
                #     show_slide(int(jpg_number))

                # run slides
                # if data == b"next_slide":
                #    current_slide = current_slide +1
                #    show_slide(current_slide)

                # if data == b"restart_slideshow":
                #    current_slide = 1
                #    show_slide(current_slide)

                # run wav interaction
                # if data == b"next_wav":
                #    current_wav = current_wav +1
                #   #play_sound(current_wav)
                #    thread_play_sound = Thread(target=play_sound, args=[current_wav])
                #    thread_play_sound.start()

                # if data == b"restart_wav":
                #    current_wav = 4
                #    thread_play_sound = Thread(target=play_sound, args=[current_wav])
                #    thread_play_sound.start()

                # run wav loop
                # if data == b"next_wav_loop":
                #    current_wav_loop = current_wav_loop +1
                #    #play_sound(current_wav)
                #    thread_play_sound = Thread(target=play_sound, args=[current_wav_loop])
                #    thread_play_sound.start()

                # if data == b"restart_wav_loop":
                #    current_wav_loop = 1
                #    thread_play_sound = Thread(target=play_sound, args=[current_wav_loop])
                #    thread_play_sound.start()



        except:
            print("something went wrong")
        #     current_slide = 1
        #     show_slide(current_slide)
        #
        #     current_wav = 4
        #     current_wav_loop = 1

        # time.sleep(0.1)


thread_upd_rec = Thread(target=udp_rec, args=(exercise_manager,))
thread_upd_rec.start()

# # ability to exit
# window.bind("<Escape>", lambda event
# :window.destroy())
#
# # run
# window.mainloop()