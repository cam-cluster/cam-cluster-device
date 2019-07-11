"""Handles HTTP Requests"""

from http import server
import json
import socketserver
from preview_stream import StreamingOutput, serve_preview_stream

def error_not_found( handler ):
	handler.send_error( 404 )
	handler.end_headers()

def redirect_to_index( handler, info, stream_out ):
	handler.send_response( 301 )
	handler.send_header( 'Location', '/index.html' )
	handler.end_headers()

def serve_info_page( handler, info, stream_out ):
	text = '<h1>' + info[ 'name' ] + '</h1>\r\n' 
	text += '<table>\r\n'
	text += '  <tr><th>mac:</th><td>' + info[ 'mac' ] + '</td></tr>\r\n'
	text += '  <tr><th>ip:</th><td>' + info[ 'ip' ] + '</td></tr>\r\n'
	text += '  <tr><th>status:</th><td>' + info[ 'status' ] + '</td></tr>\r\n'

	if stream_out:
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

get_paths = {
	'/': redirect_to_index,
	'/index.html': serve_info_page,
	'/stream.mjpg': serve_preview_stream,
}

def create_handler( cam_http_server ):
	class HTTPHandler( server.BaseHTTPRequestHandler ):
		def do_GET( self ):
			if ( self.path in get_paths ):
				path = get_paths[ self.path ]
				path( self, cam_http_server.device_info.getInfo(), cam_http_server.stream_out )
			else:
				error_not_found( self )

	return HTTPHandler

class CamHTTPServer( socketserver.ThreadingMixIn, server.HTTPServer ):
	allow_reuse_address = True
	daemon_threads = True

	def __init__( self, port, device_info, client, camera ):
		self.device_info = device_info
		self.client = client
		self.camera = camera
		self.stream_out = None

		address = ( '', port )
		super().__init__( address, create_handler( self ) )

	def start_preview( self ):
		if self.stream_out:
			# We already had a preview running, so stop it and restart
			self.stop_preview()

		self.camera.resolution = (640, 480)
		self.camera.framerate = 24

		self.stream_out = StreamingOutput()
		self.camera.start_recording( self.stream_out, format='mjpeg' )

	def stop_preview( self ):
		if self.stream_out:
			self.stream_out = None
			self.camera.stop_recording()

	def service_actions( self ):
		self.client.update()
