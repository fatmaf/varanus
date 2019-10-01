import socket

"""Communicates with the system being monitored and passes back its handle.
This should provide a common interface to the Monitor class, regardless of the
system's underlying connection  """


class SystemInterface(object):
    """Interface for all system interfaces"""

    def __init__(self):
        pass

    def connect(self):
        pass

    def close(self):
        pass


class OfflineInterface(SystemInterface):
    """ Interface to a file of traces."""

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
    """Interface to a TCP connection."""

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
