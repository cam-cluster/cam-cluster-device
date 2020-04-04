import aiohttp
from aiohttp import web
import asyncio
import os


WS_SERVER_HOST = os.getenv( 'WS_SERVER_HOST', '0.0.0.0' )
WS_SERVER_PORT = int( os.getenv( 'WS_SERVER_PORT', 8080 ) )

WS_URL = f'http://{WS_SERVER_HOST}:{WS_SERVER_PORT}/ws'

async def handle(request):
	name = request.match_info.get('name', "Anonymous")
	text = "Hello, " + name
	return web.Response(text=text)

async def start_http_server():
	print( 'starting http server...' )

	app = web.Application()
	app.router.add_route( 'GET', '/', handle )
	app.router.add_route( 'GET', '/{name}', handle )

	runner = web.AppRunner( app )
	await runner.setup()
	site = web.TCPSite( runner, 'localhost', 8080 )
	await site.start()
	print( 'http server ready' )
	return runner

async def run_ws_client():
	print( 'starting ws client' )
	session = aiohttp.ClientSession()
	async with session.ws_connect( WS_URL ) as ws:
		await ws_schedule_send( ws, 0 )
		async for msg in ws:
			print( 'WS Message received from server:', msg )
			await ws_schedule_send( ws, 10 )

			if msg.type in ( aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR ):
				break
	print( 'Exiting ws client' )

async def ws_schedule_send( ws, seconds ):
	await asyncio.sleep( seconds )
	await ws.send_str( 'websocket test message' )

async def main():
	print( 'test_server_with_wsclient' )
	runner = await start_http_server()
	await run_ws_client()
	await runner.cleanup()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete( main() )
