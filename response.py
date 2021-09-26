import requests
import sys


port = sys.argv[1:]
while True:
    for i in range(5000, 10000):
        p = 'http://' + port[0] + ':' + str(i) + '/'
        print(p)
        try:
            response = requests.get(p)
        except:
            pass