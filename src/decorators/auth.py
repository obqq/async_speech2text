from aiohttp import web

def login_required(func):
    def wrapper(request):
        if not request.authenticated:
            return web.json_response({'error': 'Auth required'}, status=401)
        return func(request)
    return wrapper