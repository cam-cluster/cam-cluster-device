"""Handles HTTP Requests"""

from http import server
import json
import socketserver

def generate_info_page( info ):
	text = '<h1>' + info[ 'name' ] + '</h1>\n' 
	text += '<table>\n'
	text += '  <tr><th>mac:</th><td>' + info[ 'mac' ] + '</td></tr>\n'
	text += '  <tr><th>ip:</th><td>' + info[ 'ip' ] + '</td></tr>\n'
	text += '</table>\n'
	return text.encode( 'utf-8' )

def create_handler( device_info ):
	class HTTPHandler( server.BaseHTTPRequestHandler ):
		dev_info = device_info

		def do_GET( self ):
			if self.path == '/':
				self.send_response( 301 )
				self.send_header( 'Location', '/index.html' )
				self.end_headers()
			elif self.path == '/index.html':
				content = generate_info_page( self.dev_info.getInfo() )
				self.send_response( 200 )
				self.send_header( 'Content-Type', 'text/html' )
				self.send_header( 'Content-Length', len( content ) )
				self.end_headers()
				self.wfile.write( content )
			else:
				self.send_error( 404 )
				self.end_headers()

	return HTTPHandler

class CamHTTPServer( socketserver.ThreadingMixIn, server.HTTPServer ):
	allow_reuse_address = True
	daemon_threads = True

	def __init__( self, port, device_info, client ):
		self.device_info = device_info
		self.client = client
		self.allow_reuse_address = True

		address = ( '', port )
		super().__init__( address, create_handler( device_info ) )

	def service_actions( self ):
		self.client.update()
