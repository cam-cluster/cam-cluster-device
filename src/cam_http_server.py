"""Handles HTTP Requests"""

from http import server
import json
import socketserver

def error_not_found( handler ):
	handler.send_error( 404 )
	handler.end_headers()

def redirect_to_index( handler ):
	handler.send_response( 301 )
	handler.send_header( 'Location', '/index.html' )
	handler.end_headers()

def serve_info_page( handler, info ):
	text = '<h1>' + info[ 'name' ] + '</h1>\n' 
	text += '<table>\n'
	text += '  <tr><th>mac:</th><td>' + info[ 'mac' ] + '</td></tr>\n'
	text += '  <tr><th>ip:</th><td>' + info[ 'ip' ] + '</td></tr>\n'
	text += '</table>\n'
	content = text.encode( 'utf-8' )

	handler.send_response( 200 )
	handler.send_header( 'Content-Type', 'text/html' )
	handler.send_header( 'Content-Length', len( content ) )
	handler.end_headers()
	handler.wfile.write( content )

get_paths = {
	'/': redirect_to_index,
	'/index.html': serve_info_page,
}

def create_handler( device_info, get_paths ):
	class HTTPHandler( server.BaseHTTPRequestHandler ):
		dev_info = device_info

		def do_GET( self ):
			handle_get = get_paths[ self.path ]

			if handle_get:
				handle_get( self, self.dev_info.getInfo() )
			else:
				error_not_found( self )

	return HTTPHandler

class CamHTTPServer( socketserver.ThreadingMixIn, server.HTTPServer ):
	allow_reuse_address = True
	daemon_threads = True

	def __init__( self, port, device_info, client ):
		self.device_info = device_info
		self.client = client
		self.allow_reuse_address = True

		address = ( '', port )
		super().__init__( address, create_handler( device_info, get_paths ) )

	def service_actions( self ):
		self.client.update()
