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
from cam_http_server import CamHTTPServer

server_url = environ[ 'SERVER_URL' ]
device_name = environ[ 'DEVICE_NAME' ]
register_interval = int( environ[ 'REGISTER_INTERVAL' ] )
cam_server_port = int( environ[ 'CAM_SERVER_PORT' ] )

print( 'Starting up "', device_name, '"...' )

device_info = DeviceInfo( device_name )

class CamClusterClient( object ):
	def __init__( self, register_interval ):
		self.register_interval = register_interval
		self.api = CamClusterApi( server_url )
		self.last_register = 0
		self.update()

	def update( self ):
		now = time.time()
		if ( self.last_register + self.register_interval <= now ):
			self.api.register( device_info )
			self.last_register = now

client = CamClusterClient( register_interval )

server = CamHTTPServer( cam_server_port, device_info, client )
server.serve_forever()
