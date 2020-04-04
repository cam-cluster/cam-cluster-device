from aiohttp import web
import asyncio

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

def main():
    print( 'test_http_server' )

    app = web.Application()
    app.router.add_route( 'GET', '/', handle )
    app.router.add_route( 'GET', '/{name}', handle )
    web.run_app( app )

if __name__ == '__main__':
    main()
