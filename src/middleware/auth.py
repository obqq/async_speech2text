import jwt
from aiohttp import web

from src.utils.access_token import decode_token


@web.middleware
async def auth_middleware(request, handler):
    request.authenticated = False
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return web.json_response({'error': 'Invalid token type specified'}, status=400)

    if not auth_header.startswith('Bearer '):
        return web.json_response({'error': 'Access token is not specified'}, status=400)

    access_token = auth_header[7:]

    try:
        await decode_token(request, access_token)
    except jwt.DecodeError:
        return web.json_response({'error': 'Invalid access token'}, status=400)
    except jwt.ExpiredSignatureError:
        return web.json_response({'error': 'Access token expired'}, status=400)

    request.authenticated = True
    return await handler(request)

