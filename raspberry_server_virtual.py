import os
import socket
import time
import json
from threading import Thread
from exercise_manager import ExerciseManager

# copy to raspi
# scp -r /Users/clara/TUMaster/8_WS2021/ProjektMedInf/pepper-therapex2 pi@raspberrypi.local:/home/pi/Desktop/

# setup udp-server
# ip = "raspberrypi.local"  # change to IP to the raspberry or to the pc with slideshow.py
port = 5005
data_port = 5006

# getting the IP address using socket.gethostbyname() method
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
# printing the hostname and ip_address
print("Hostname: " + hostname)
print("IP Address: " + ip)
ip = "127.0.0.1"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data_sock.bind((ip, data_port))

# exercise_manager = ExerciseManager()

print("I'm running from /home/pi/.config/autostart/pepper_therapex_study.desktop")


def send_data():
    test_data = [[63, 435], [61, 378]]
    headers = ['time', 'BPM', 'pulse_data', 'resting_BPM', 'exercise_intensity']
    ready = True
    counter = 0

    while True:
        try:
            # ready = select.select([sock], [], [], timeout)
            if ready:
                msg, source_address = data_sock.recvfrom(1024)

                if msg == b'data':
                    # reply with bpm, pulse, resting_bpm, last20_bpm?
                    counter = counter % 2
                    response = json.dumps(test_data[counter])
                    print(response)
                    data_sock.sendto(response.encode(), source_address)
                    counter += 1

                else:
                    print("unknown request")
        except:
            print("something went wrong with data call")


# run udp-server
def udp_rec():
    timeout = 5
    ready = True
    test_data = [[63, 435, 62, 64], [61, 378, 62, 63]]
    headers = ['time', 'BPM', 'pulse_data', 'resting_BPM', 'exercise_intensity']
    data_saver = None
    session_num = 1

    counter = 0

    print("starting to listen")
    while True:
        try:
            # ready = select.select([sock], [], [], timeout)
            if ready:
                bmsg, source_address = sock.recvfrom(1024)
                msg = bmsg.decode()
                if msg == "start":
                    # save session
                    # exercise_manager.start_new_experiment_cycle()

                    response = "started exercise cycle!"
                    sock.sendto(response.encode(), source_address)

                elif msg == "done":
                    # save session
                    # exercise_manager.save_session_data()

                    response = "stopped exercise cycle!"
                    sock.sendto(response.encode(), source_address)

                elif "resting_bpm" in msg:
                    # get resting bpm value (assume double digits)
                    # 3 digit resting bpm should not occur
                    resting_bpm = int(msg[-2:])




                else:
                    print("unknown request")

        except:
            print("something went wrong")

        # time.sleep(0.1)


thread_upd_rec = Thread(target=udp_rec)
thread_upd_rec.start()

thread_data = Thread(target=send_data)
thread_data.start()
