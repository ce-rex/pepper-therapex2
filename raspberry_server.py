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

exercise_manager = ExerciseManager(arduino=False)

print("I'm running from /home/pi/.config/autostart/pepper_therapex_study.desktop")


def send_data():
    ready = True

    while True:
        try:
            # ready = select.select([sock], [], [], timeout)
            if ready:
                msg, source_address = data_sock.recvfrom(1024)

                if msg == b'data':
                    data = exercise_manager.update_data()
                    response = json.dumps(data)
                    print(response)
                    data_sock.sendto(response.encode(), source_address)

                else:
                    print("unknown request for data")
        except:
            print("something went wrong with data call")


# run udp-server
def udp_rec():
    ready = True

    print("starting to listen")
    while True:
        try:
            # ready = select.select([sock], [], [], timeout)
            if ready:
                bmsg, source_address = sock.recvfrom(1024)
                msg = bmsg.decode()
                if msg == "start":
                    # save session
                    exercise_manager.start_new_experiment_cycle()
                    response = "started exercise cycle!"
                    sock.sendto(response.encode(), source_address)

                elif msg == "done":
                    # save session
                    exercise_manager.save_session_data()
                    response = "stopped exercise cycle!"
                    sock.sendto(response.encode(), source_address)

                elif "resting_bpm" in msg:
                    # get resting bpm value (assume double digits)
                    # 3 digit resting bpm should not occur
                    resting_bpm = int(msg[-2:])
                    print("resting_bpm: " + str(resting_bpm))
                    exercise_manager.resting_bpm = resting_bpm

                elif "intensity" in msg:
                    # get current exercise intensity
                    current_intensity = int(msg[-1:])
                    print("current_intensity: " + str(current_intensity))
                    exercise_manager.exercise_intensity = current_intensity

                else:
                    print("unknown request")

        except:
            print("something went wrong")

        # time.sleep(0.1)


thread_upd_rec = Thread(target=udp_rec)
thread_upd_rec.start()

thread_data = Thread(target=send_data)
thread_data.start()
