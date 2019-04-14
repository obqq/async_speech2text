import jwt
import logging
from aiohttp import web
from aiohttp.client_exceptions import ClientConnectionError

from settings import PUBLIC_KEY_URL

logger = logging.getLogger(__name__)

async def get_public_key(request):
    http_client = request.app['external_api']
    try:
        response = await http_client.get(PUBLIC_KEY_URL)
    except ClientConnectionError as e:
        logger.error(e)
        return web.json_response({'error': 'Cannot connect to the server. Please, try again later'}, status=500)
    json_response = await response.json()

    return json_response.get('public_key')


async def decode_token(request, token):
    public_key = await get_public_key(request)
    data = jwt.decode(token, public_key, algorithms=['RS256'])

    return data
