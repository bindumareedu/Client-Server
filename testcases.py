import argparse
import subprocess
import time



serverprocess = subprocess.Popen(['python3', 'server.py'])
time.sleep(.50)
print('\n***TEST CASE 1***')
subprocess.call(['python3','alice.py','--key', 'color', '--value', 'red'])
subprocess.call(['python3','alice.py','--key', 'day', '--value', 'monday'])
subprocess.call(['python3','alice.py','--key', 'thing', '--value', 'bowl'])
print('\n***TEST CASE 2***')
subprocess.call(['python3','bob.py','--key', 'thing'])
subprocess.call(['python3','bob.py','--key', 'day'])
subprocess.call(['python3','bob.py','--key', 'color'])
print('\n***TEST CASE 3***')
subprocess.call(['python3','bob.py','--key', 'time'])
print('\n***TEST CASE 4***')
subprocess.call(['python3','alice.py','--key', 'pen', '--value', 'paper'])
subprocess.call(['python3','bob.py','--key', 'pen'])
subprocess.call(['python3','alice.py','--key', 'pencil', '--value', 'lid'])
subprocess.call(['python3','bob.py','--key', 'pencil'])


serverprocess.kill()


