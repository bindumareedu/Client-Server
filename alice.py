import argparse
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1993      # The port used by the server




def main(key , value, wait=True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        input = 'STORE '+key+'='+value
        s.sendall(input.encode())
        data = s.recv(4096)
        print('AT CLIENT_ALICE: STORE ', data.decode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--key', default='username', help='Contains value of the key that needs to be stored')
    parser.add_argument('--value',  default='foo', help='Contains value of particular key')
    args = parser.parse_args()
    main(args.key, args.value)