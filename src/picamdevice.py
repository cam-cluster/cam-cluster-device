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

import io
from os import environ
import picamera
from threading import Condition
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

# TODO: Move this to a proper location
class StreamingOutput( object ):
	def __init__( self ):
		self.frame = None
		self.buffer = io.BytesIO()
		self.condition = Condition()

	def write( self, buf ):
		if buf.startswith( b'\xff\xd8'):
			# New frame, copy the existing buffer's content and notify all
			# clients it's available
			self.buffer.truncate()
			with self.condition:
				self.frame = self.buffer.getvalue()
				self.condition.notify_all()
			self.buffer.seek(0)
		return self.buffer.write( buf )

with picamera.PiCamera( resolution='640x480', framerate=24 ) as camera:
	output = StreamingOutput()
	camera.start_recording( output, format='mjpeg' )

	try:
		client = CamClusterClient( register_interval )
		server = CamHTTPServer( cam_server_port, device_info, client, output )
		server.serve_forever()
	finally:
		camera.stop_recording()
