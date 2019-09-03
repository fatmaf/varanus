import socket

class EventAbstractor(object):

    def __init__(self, event_map):
        self.event_map = event_map



class SystemInterface(object):

    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass


class OfflineInterface(SystemInterface):

    def __init__(self, trace_file_path, event_map = None):
        self.trace_file_path = trace_file_path
        if event_map != None:
            self.EventAbs = EventAbstractor(event_map)

    def connect(self):
        self.trace_file = open(self.trace_file_path)
        return self.trace_file

    def close(self):
        self.trace_file.close()



class TCPInterface(SystemInterface):

    def __init__(self, IP, port, event_map = None):
        self.IP = IP
        self.port = port

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.IP, self.port))
        s.listen(1)

        self.conn, addr = s.accept()
        print 'Connection address:', addr
        return self.conn

    def close(self):
        self.conn.close()
