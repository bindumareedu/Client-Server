import argparse
import socket
import threading


class ReadWriteLock:
    ''' From :  https://www.oreilly.com/library/view/python-cookbook/0596001673/ch06s04.html
    A lock object that allows many simultaneous "read locks", but only one "write lock." '''

    def __init__(self):
        self._read_ready = threading.Condition(threading.RLock())
        self._readers = 0

    def acquire_read(self):
        """ Acquire a read lock. Blocks only if a thread has
        acquired the write lock. """
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def release_read(self):
        """ Release a read lock. """
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def acquire_write(self):
        """ Acquire a write lock. Blocks until there are no
        acquired read or write locks. """
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def release_write(self):
        """ Release a write lock. """
        self._read_ready.release()

def get(input, lock, addr):
    try:
        lock.acquire_read()
        key = input.split(' ')[1]
        if key in dict:
            value = dict[key]
        else:
            value = 'ERROR'
        print('AT SERVER: Client', addr, ' GET key = ', key)
        print('AT SERVER: Client', addr, 'Sending back value = ',value,' to client')
    finally:
        lock.release_read()
    return value

def store(input, lock, addr):
    try:
        lock.acquire_write()
        keyval = input.split(' ')[1]
        key = keyval.split('=')[0]
        value = keyval.split('=')[1]
        dict[key] = value
        response = 'success'
        print('AT SERVER: Client', addr, ' STORED key = ', key, 'value = ', value)
        print('AT SERVER: Client', addr, 'Sending back response to client')
    finally:
        lock.release_write()
    return response


def server_thread(conn, addr, lock):
            data = conn.recv(1024)
            input = data.decode()
            action = input.partition(' ')[0]
            if action == 'GET':
                print('AT SERVER: Client', addr, ' requested GET')
                response = get(input, lock, addr)
            elif action == 'STORE':
                print('AT SERVER: Client', addr, ' requested STORE')
                response = store(input, lock, addr)
            else:
                print('AT SERVER: Client', addr, ' UNEXPECTED_INPUT')
                response = 'UNEXPECTED_INPUT'
            conn.send(bytes(response, 'utf-8'))

def main(host, port , wait=True):
    global HOST
    global PORT
    global dict
    dict = {}
    HOST = host
    PORT = port
    lock = ReadWriteLock()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print('AT SERVER: Client', addr, ' connected to server')
            t = threading.Thread(target=server_thread, name=addr[0], args=(conn, addr, lock))
            t.start()
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--host', default='127.0.0.1', help='Value of port')
    parser.add_argument('--port', default=1993, help='Value of port')
    args = parser.parse_args()
    main(args.host, args.port)
