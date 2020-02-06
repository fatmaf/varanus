import websocket
import sys
try:
    import thread
except ImportError:
    import _thread as thread
import time

""" Reads the json file supplied in FILE and sends this to the monitor """

TCP_IP = '127.0.0.1'
TCP_PORT = "8080"
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
FILE = "mascot-speed-fail-am.json"

def main(argv):
    websocket.enableTrace(True)
    websockets_str =  "ws://" + TCP_IP + ":" + TCP_PORT

    print(websockets_str)
    ws = websocket.WebSocketApp(
        websockets_str,
        on_message = on_message,
        on_error = on_error,
        on_close = on_close,
        on_open = on_open)
    ws.run_forever()

    print("Mid Main")





def on_message(ws, message):
    print(message)

    json_dict = json.loads(message)
    if 'error' in json_dict:
        print('The event ' + message + ' is inconsistent..')
    else:
        print('The event ' + message + ' is fine..')

def on_error(ws, error):
    print(error)

def on_close(ws):
	print('+++ Dummy MASCOT websocket closed +++')

def on_open(ws):
    print('+++ Dummy MASCOT websocket is open +++')
    def run(*args):
        telegram_file = open(FILE, "r")
        for line in telegram_file:
            ws.send(line)
            print("+++ Dummy MASCOT sent data: ", line)
            data = s.recv(BUFFER_SIZE)
            print("+++ Dummy MASCOT received data: ", data)

        telegram_file.close()

        time.sleep(1)
        close(ws)
        print("thread terminating...")
    thread.start_new_thread(run, ())

def close(ws):
    ws.close()

if __name__ == '__main__':
    main(sys.argv)
