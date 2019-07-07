"""Sends and receives API calls from the Cam Cluster Server"""

import json

class CamClusterApi( object ):

	def __init__( self, serverUrl ):
		self.serverUrl = serverUrl

	def register( self, deviceInfo ):
		# TODO: Send an API fetch call
		print( 'info: ', json.dumps( deviceInfo.getInfo() ) )
