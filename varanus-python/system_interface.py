import socket
import websocket

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
        print '+++ Varanus Connection address:', addr
        return self.conn

    def close(self):
        self.conn.close()

class WebSocketInterface(SystemInterface):
    """ Interface to a WebSocket Connection """

    def __init__(self, IP, port=None, event_map = None):
        self.IP = IP
        if port != None:
            self.port = str(port)

        websocket.enableTrace(False)
        if port != None:
            websockets_str = "ws://" + self.IP + ":" + self.port
        else:
            websockets_str = "ws://" + self.IP

        self.ws = websocket.WebSocketApp(
            "ws://127.0.0.1:8080",
            on_message = self.on_message,
            on_error = self.on_error,
            on_close = self.on_close,
            on_open = self.on_open)
        print(self.ws)
        print("+++ WebSocketInterface Initialised +++")

    def send(self, message):
        print("+++ Sending ", message, " +++")
        self.ws.send(message)

    def connect(self):
        self.ws.run_forever()



    def close(self):
        self.ws.close()

    def on_message(ws, message):
        print(message)

        new_traces = eventMapper.new_traces(json.loads(data))
        print new_traces

        results = []
        for new_trace in new_traces:
            print new_trace
            result = self.fdr.check_trace(new_trace)

            print result
            results.append(result)

        num_of_results = len(results)
        num_of_t = 0
        for r in results:
            if r: #is true
                num_of_t = num_of_t + 1

        percentage_true = (float(num_of_t) / num_of_results) * 100

        if percentage_true == 0 :
            print "False (100%)"
        else:
            print "True (" + str(percentage_true) + "%)"

        self.ws.send("Varanus got the message")

    def on_error(ws, error):
        print(error)

    def on_close(ws):
    	print('+++ Varanus websocket closed +++')

    def on_open(ws):
    	print('+++ Varanus websocket is open +++')

if __name__ == '__main__':
    system = WebSocketInterface("127.0.0.1")
    system.connect()
