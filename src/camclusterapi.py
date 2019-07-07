"""Sends and receives API calls from the Cam Cluster Server"""

import json
from requests import post

class CamClusterApi( object ):

	def __init__( self, serverUrl ):
		self.serverUrl = serverUrl

	def register( self, deviceInfo ):
		url = self.serverUrl + '/api/cameras'
		print( 'Registering via url: ', url )

		r = post( url, data = deviceInfo.getInfo() )

		# TODO: Add handling for response
		print( 'Response: ', r.status_code, r.reason )
		print( r.text )
