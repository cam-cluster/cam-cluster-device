#!/usr/bin/env python

"""Runs the Pi Cam Device for the Cam Cluster

This runs any Raspberry Pi as a Cam Cluster device using
its built-in camera interface
"""

__author__ = "Kevin Killingsworth"
__copyright__ = "Copyright 2019, Kevin Killingsworth"
__credits__ = [ "Kevin Killingsworth" ]
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Kevin Killingsworth"
__email__ = "kk@redfenix.com"
__status__ = "Pre-alpha"

from os import environ
import time

from camclusterapi import CamClusterApi
from deviceinfo import DeviceInfo

serverUrl = environ[ 'SERVER_URL' ]
deviceName = environ[ 'DEVICE_NAME' ]

print( 'Starting up "', deviceName, '"...' )

deviceInfo = DeviceInfo( deviceName )
camClusterApi = CamClusterApi( serverUrl )

while True:
	camClusterApi.register( deviceInfo )
	time.sleep( 60 );
