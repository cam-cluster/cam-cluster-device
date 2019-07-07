"""Holds identifying information about this device"""

from getmac import get_mac_address

class DeviceInfo( object ):

	def __init__( self, deviceName ):
		self.mac = get_mac_address()
		self.deviceName = deviceName

	def getInfo( self ):
		return {
			'mac': self.mac,
			'name': self.deviceName,
		}
