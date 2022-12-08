import os
import socket
import time
import json
import select
from threading import Thread

# import tkinter as tk
# from PIL import ImageTk, Image

# setup udp-server
ip = "raspberrypi.local"  # change to IP to the raspberry or to the pc with slideshow.py
port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

sensor = PulseSensor(filepath="data_log/" + session_timestamp + "arduino_log.csv")

print("I'm running from /home/pi/.config/autostart/pepper_therapex_study.desktop")

# run udp-server
def udp_rec():
    timeout = 5
    ready = True
    test_data = [[63, 435, 62, 64], [61, 378, 62, 63]]
    counter = 0
    
    print("starting to listen")
    while True:
        try:
            # ready = select.select([sock], [], [], timeout)
            if ready:
                msg, source_address = sock.recvfrom(1024)
                #print(msg)
                #print(source_address)
                # what data does the client send/need?
                if msg == b'newsession':
                    # create new recording file
                    print(msg)
                
                if msg == b'data':
                    print(msg)
                    # reply with bpm, pulse, resting_bpm, last20_bpm?
                    counter = counter % 2
                    response = json.dumps(test_data[counter])
                    print(response)
                    sock.sendto(response.encode(), source_address)
                    counter += 1
                    
                if msg == b'calibration':
                    print(msg)
                    # reply with bpm, pulse, resting_bpm, last20_bpm?
                    counter = counter % 2
                    response = json.dumps(test_data[counter])
                    print(response)
                    sock.sendto(response.encode(), source_address)
                    counter += 1
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


thread_upd_rec = Thread(target=udp_rec)
thread_upd_rec.start()

# # ability to exit
# window.bind("<Escape>", lambda event
# :window.destroy())
#
# # run
# window.mainloop()
