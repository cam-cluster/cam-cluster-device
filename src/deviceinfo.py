"""Holds identifying information about this device"""

from getmac import get_mac_address
import socket

DEVICE_STATUS = {
	'idle': 'Idle',
	'preview': 'Preview Mode',
	'preparing': 'Preparing to record...',
	'recording': 'Recording',
	'uploading': 'Uploading',
}

class DeviceInfo( object ):

	def __init__( self, deviceName ):
		self.mac = get_mac_address()
		self.deviceName = deviceName
		self.status = DEVICE_STATUS[ 'idle' ]

	def getInfo( self ):
		return {
			'mac': self.mac,
			'name': self.deviceName,
			'ip': self.getIp(),
			'status': self.status,
		}

	def getIp( self ):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			# doesn't even have to be reachable
			s.connect(('10.255.255.255', 1))
			IP = s.getsockname()[0]
		except:
			IP = '127.0.0.1'
		finally:
			s.close()
		return IP
