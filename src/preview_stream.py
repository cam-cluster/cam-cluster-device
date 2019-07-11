import io
from threading import Condition

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

def serve_preview_stream( httpHandler, info, stream_out ):
	httpHandler.send_response( 200 )
	httpHandler.send_header( 'Age', 0 )
	httpHandler.send_header( 'Cache-Control', 'no-cache, private' )
	httpHandler.send_header( 'Pragma', 'no-cache' )
	httpHandler.send_header( 'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME' )
	httpHandler.end_headers()
	try:
		while True:
			with stream_out.condition:
				stream_out.condition.wait()
				frame = stream_out.frame
			httpHandler.wfile.write( b'--FRAME\r\n' )
			httpHandler.send_header( 'Content-Type', 'image/jpeg' )
			httpHandler.send_header( 'Content-Length', len( frame ) )
			httpHandler.end_headers()
			httpHandler.wfile.write( frame )
			httpHandler.wfile.write( b'\r\n' )
	except Exception as e:
		print(
			'Removed streaming client %s: %s',
			httpHandler.client_address, str( e )
		)
