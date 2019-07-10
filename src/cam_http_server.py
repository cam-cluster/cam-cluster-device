"""Handles HTTP Requests"""

from http import server
import json
import socketserver

def error_not_found( handler ):
	handler.send_error( 404 )
	handler.end_headers()

def redirect_to_index( handler, info, output ):
	handler.send_response( 301 )
	handler.send_header( 'Location', '/index.html' )
	handler.end_headers()

def serve_info_page( handler, info, output ):
	text = '<h1>' + info[ 'name' ] + '</h1>\r\n' 
	text += '<table>\r\n'
	text += '  <tr><th>mac:</th><td>' + info[ 'mac' ] + '</td></tr>\r\n'
	text += '  <tr><th>ip:</th><td>' + info[ 'ip' ] + '</td></tr>\r\n'
	text += '  <tr><th>status:</th><td>' + info[ 'status' ] + '</td></tr>\r\n'
	text += '  <tr>\r\n'
	text += '    <th>preview:</th>\r\n'
	text += '    <td><img src="stream.mjpg" width="640" height="480"</td>\r\n'
	text += '  </tr>\r\n'
	text += '</table>\r\n'
	content = text.encode( 'utf-8' )

	handler.send_response( 200 )
	handler.send_header( 'Content-Type', 'text/html' )
	handler.send_header( 'Content-Length', len( content ) )
	handler.end_headers()
	handler.wfile.write( content )

def serve_camera_stream( handler, info, output ):
	handler.send_response( 200 )
	handler.send_header( 'Age', 0 )
	handler.send_header( 'Cache-Control', 'no-cache, private' )
	handler.send_header( 'Pragma', 'no-cache' )
	handler.send_header( 'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME' )
	handler.end_headers()
	try:
		while True:
			with output.condition:
				output.condition.wait()
				frame = output.frame
			handler.wfile.write( b'--FRAME\r\n' )
			handler.send_header( 'Content-Type', 'image/jpeg' )
			handler.send_header( 'Content-Length', len( frame ) )
			handler.end_headers()
			handler.wfile.write( frame )
			handler.wfile.write( b'\r\n' )
	except Exception as e:
		print(
			'Removed streaming client %s: %s',
			handler.client_address, str( e )
		)

get_paths = {
	'/': redirect_to_index,
	'/index.html': serve_info_page,
	'/stream.mjpg': serve_camera_stream,
}

def create_handler( device_info, output, get_paths ):
	class HTTPHandler( server.BaseHTTPRequestHandler ):
		dev_info = device_info

		def do_GET( self ):
			if ( self.path in get_paths ):
				get_paths[ self.path ]( self, self.dev_info.getInfo(), output )
			else:
				error_not_found( self )

	return HTTPHandler

class CamHTTPServer( socketserver.ThreadingMixIn, server.HTTPServer ):
	allow_reuse_address = True
	daemon_threads = True

	def __init__( self, port, device_info, client, output ):
		self.client = client

		address = ( '', port )
		super().__init__( address, create_handler( device_info, output, get_paths ) )

	def service_actions( self ):
		self.client.update()
