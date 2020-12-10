from aiohttp import web
import asyncio


routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
	return web.Response(text='ok')

def start_server(loop, background_task, client):
	global app
	asyncio.set_event_loop(loop)
	app = web.Application(
	)
	app.discord = client
	app.add_routes(routes)
	asyncio.ensure_future(
		background_task,
		loop=loop
	)
	web.run_app(
		app,
		port=8081
	)