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

from http import server
from os import environ
import socketserver
import time

from camclusterapi import CamClusterApi
from deviceinfo import DeviceInfo

serverUrl = environ[ 'SERVER_URL' ]
deviceName = environ[ 'DEVICE_NAME' ]
registerInterval = int( environ[ 'REGISTER_INTERVAL' ] )
camServerPort = int( environ[ 'CAM_SERVER_PORT' ] )

print( 'Starting up "', deviceName, '"...' )

deviceInfo = DeviceInfo( deviceName )

class CamClusterClient( object ):
	def __init__( self, registerInterval ):
		self.registerInterval = registerInterval
		self.camClusterApi = CamClusterApi( serverUrl )
		self.lastRegister = 0
		self.update()

	def update( self ):
		now = time.time()
		if ( self.lastRegister + self.registerInterval <= now ):
			self.camClusterApi.register( deviceInfo )
			self.lastRegister = now

client = CamClusterClient( registerInterval )

class HTTPHandler( server.BaseHTTPRequestHandler ):
	def do_GET( self ):
		if self.path == '/':
			self.send_response( 301 )
			self.send_header( 'Location', '/index.html' )
			self.end_headers()
		elif self.path == '/index.html':
			text = 'CamServer test page'
			content = text.encode( 'utf-8' )
			self.send_response( 200 )
			self.send_header( 'Content-Type', 'text/html' )
			self.send_header( 'Content-Length', len( content ) )
			self.end_headers()
			self.wfile.write( content )
		else:
			self.send_error( 404 )
			self.end_headers()

class CamServer( socketserver.ThreadingMixIn, server.HTTPServer ):
	allow_reuse_address = True
	daemon_threads = True

	def service_actions( self ):
		client.update()

address = ( '', camServerPort )
server = CamServer( address, HTTPHandler )
server.serve_forever()

#while True:
#	camClusterApi.register( deviceInfo )
#	#time.sleep( registerInterval );
