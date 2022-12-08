import os
import socket
import time
import json
from threading import Thread

# import tkinter as tk
# from PIL import ImageTk, Image

# setup udp-server
ip = "raspberrypi.local"  # change to IP to the raspberry or to the pc with slideshow.py
port = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))


# # globals
# current_slide = 1
# current_wav = 4
# current_wav_loop = 1
#
# # create slideshow
# window = tk.Tk()
# window.title("slideshow")
# window.geometry("1920x1080")
# #window.geometry("1280x800")
# window.configure(background='black')
# window.attributes("-fullscreen", True)
# window.config(cursor="none")
#
# # define function to change slide
# panel = tk.Label(window)
# panel.configure(background="black")


def show_slide(current_slide):
    print("hi")


#     try:
#         global panel
#
#         print("showing slide", current_slide)
#         #file = "/media/pi/OLIVER/" + str(current_slide) + ".JPG"
#         file = "/home/pi/slideshow/" + str(current_slide) + ".JPG"
#         print(file)
#         panel.image = ImageTk.PhotoImage(Image.open(file))
#         panel['image'] = panel.image
#         panel.place(x=0, y=0)
#         print("showig slide " + str(current_slide))
#     except:
#         pass
#         print("error in showing slides")
#
#
# # show slide
# show_slide(1)


# def play_sound(curren_wav):
#     try:
#         file = "/home/pi/slideshow/" + str(curren_wav) + ".wav"
#         task = "aplay " + file
#         os.system(task)
#     except:
#         pass

# run udp-server
def udp_rec():
    while True:
        try:
            data, source_address = sock.recvfrom(1024)
            print(data)
            print(source_address)
            # what data does the client send/need?
            if data == "data":
                # reply with bpm and pulse
                response = [63, 432]
                sock.sendto(json.dumps(response), source_address)
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
