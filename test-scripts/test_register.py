from getmac import get_mac_address
from requests import post
from os import environ
import sys
import time

serverUrl = environ['SERVER_URL']
deviceName = environ['DEVICE_NAME']

print( "Starting up..." )

info = {
  'mac': get_mac_address(),
  'name': deviceName,
}

print( "Camera info: ", info )

if len(sys.argv) > 1:
  serverUrl = sys.argv[1]

# Continue to execute just so the container doesn't restart
while True:
  url = serverUrl + "/api/cameras"
  print( "Registering via url: ", url )

  r = post( url, data = info )

  print( r.status_code, r.reason )
  print( r.text )

  time.sleep(60)
