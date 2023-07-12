class DataClient():
    def __init__(self, logger, behaviorAbsolutePath, virtual, data_port, arg_port):
        self.logger = logger
        if virtual:
            self.ip = "127.0.0.1"
        else:
            #self.ip = "192.168.1.102" # server is on local computer
            #self.ip = "192.168.1.100"  # server is on local computer - tp link pep wifi
            self.ip = "raspberrypi.local" # server is on raspberry pi

        self.data_port = data_port
        self.arg_port = arg_port

        self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.arg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.arg_sock.setblocking(False) # Prevent socket from waiting for input

    def call_for(self, msg):
        self.logger.info("asking for " + msg)
        try:
            self.arg_sock.sendto(msg, (self.ip, self.arg_port))
            response = self.arg_sock.recv(1024)
            self.logger.info(response)
        except:
            self.logger.info("connection to raspi not available")

        return response

    def call_with_data(self, topic, data=None):
        #self.logger.info("asking for " + topic + " with data: " + str(data))

        msg = json.dumps([topic, data])
        try:
            self.arg_sock.sendto(msg.encode(), (self.ip, self.arg_port))
            #response = self.arg_sock.recv(1024)
            self.logger.info("sent " + topic + " with data: " + str(data))
        except:
            self.logger.info("connection to raspi not available")

    def call_for_data(self):
        # self.logger.info("asking for data")
        try:
            self.data_sock.sendto("data", (self.ip, self.data_port))
            response = self.data_sock.recv(1024)
            # self.logger.info(response)

            bpm, pulse = json.loads(response)
            #data_msg = "BPM: " + str(bpm) + "  ---  pulse signal: " + str(pulse)
            #self.logger.info(data_msg)
            return bpm, pulse
        except:
            self.logger.info("connection to raspi not available")
            return [0, 0]