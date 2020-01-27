import argparse
import subprocess
import time



def main(key , value, wait=True):
    serverprocess = subprocess.Popen(['python3', 'server.py'])
    time.sleep(.50)
    subprocess.call(['python3','alice.py','--key', key, '--value', value])
    subprocess.call(['python3','bob.py','--key', key])
    serverprocess.kill()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--key', default='username', help='Contains value of the key that needs to be stored')
    parser.add_argument('--value',  default='foo', help='Contains value of particular key')
    args = parser.parse_args()
    main(args.key, args.value)