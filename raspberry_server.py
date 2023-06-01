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
print("Hostname: " + hostname)
# ip = socket.gethostbyname(hostname)  # does not work like this
# printing the hostname and ip_address

if hostname == "raspberrypi":
    print("I'm running from /home/pi/.config/autostart/pepper_therapex_study.desktop")
    ip = "raspberrypi.local"  # on raspi
else:
    ip = "127.0.0.1"  # server on laptop, virtual robot
    # ip = "192.168.1.102"  # server on laptop, real robot
print("IP Address: " + ip)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data_sock.bind((ip, data_port))

exercise_manager = ExerciseManager(arduino=False)


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
                    # print(response)
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
                # msg = bmsg.decode()
                msg, data = json.loads(bmsg)
                if msg == "start":
                    # save session
                    exercise_manager.start_new_experiment_cycle()
                    # response = "RASPI: started exercise cycle!"
                    # sock.sendto(response.encode(), source_address)
                    print("\n got request: START EXPERIMENT")

                elif msg == "done":
                    # save session
                    exercise_manager.save_session_data()
                    # response = "RASPI: stopped exercise cycle!"
                    # sock.sendto(response.encode(), source_address)
                    print("\n got request: STOP exercise cycle")

                    # start new session, if requested
                    if not data:  # if this session was not the last
                        exercise_manager.start_new_session()
                    else:
                        print("\n STOPPED experiment!")
                        print("\n ------------------------------------------------------")

                # elif "resting_bpm" in msg:
                elif "resting_bpm" == msg:
                    # print(data)
                    # get resting bpm value (assume double digits)
                    # 3 digit resting bpm should not occur
                    resting_bpm = float(data)  # this might not be an int e.g. 55.5
                    # response = "RASPI: set resting BPM!"
                    # sock.sendto(response.encode(), source_address)
                    print("\n CALIBRATION done!")
                    print("got data: resting_bpm = " + str(resting_bpm))
                    exercise_manager.resting_bpm = resting_bpm

                elif "intensity" == msg:
                    # get current exercise intensity
                    current_intensity = int(data)
                    # response = "RASPI: set intensity trend!"
                    # sock.sendto(response.encode(), source_address)
                    print("\n FINISHED EXERCISE! setting new exercise intensity")
                    print("got data: intensity trend = " + str(current_intensity))
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
