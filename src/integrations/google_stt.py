import base64
import logging
from aiohttp.client_exceptions import ClientConnectionError

from settings import GOOGLE_STT_API_URL

logger = logging.getLogger(__name__)


class GoogleSpeechToTextAPI:
    def __init__(self, request):
        self.API_KEY = GOOGLE_STT_API_URL
        self.http_client =  http_client = request.app['external_api']

    async def send_request(self, data):
        try:
            response = await self.http_client.post(GOOGLE_STT_API_URL, json=data)
            return await response.json()

        except ClientConnectionError as e:
            logger.error(e)

    async def encode_audio(self, audio_content):
        return base64.b64encode(audio_content)

    async def recognize(self, audio_content, encoding, sample_rate_hertz, language_code):
        speech_content = await self.encode_audio(audio_content)

        data = {
            'audio': {
                'content': speech_content.decode('UTF-8')
            },
            'config': {
                'encoding': encoding,
                'sampleRateHertz': sample_rate_hertz,
                'languageCode': language_code
            }
        }

        return await self.send_request(data)
