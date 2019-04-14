import logging
from aiohttp import web

from src.decorators.auth import login_required
from src.integrations.google_stt import GoogleSpeechToTextAPI

logger = logging.getLogger(__name__)

FILE_MAX_SIZE = 1024 * 1024 * 10


@login_required
async def recognize_speech(request):
    request_data = await request.post()

    # todo: reimplement validation
    # serializer = SpeechSerializer(data=request.POST)
    # if not serializer.is_valid():
    #     return web.json_response(
    #         {'error': serializer.errors},
    #         status=400
    #     )

    audiofile = request_data.get('file').file

    encoding = request_data.get('encoding')
    sample_rate_hertz = request_data.get('sampleRateHertz')
    language_code = request_data.get('languageCode')

    if not audiofile:
        return web.json_response(
            {'error': 'Audio file was not specified.'},
            status=400
        )

    audio_content = audiofile.read()

    if len(audio_content) > FILE_MAX_SIZE:
        return web.json_response(
            {'error': "Audio file size exceeds the maximum size limit of 10 MB."},
            status=400
        )

    API = GoogleSpeechToTextAPI(request)
    response = await API.recognize(audio_content, encoding, sample_rate_hertz, language_code)

    if not response:
        return web.json_response(
            {'error': 'Something went wrong. Please try again later.'},
            status=500
        )

    error = response.get('error')
    if error:
        return web.json_response(
            {'error': error.get('message')},
            status=400
        )

    results = response.get('results')

    return web.json_response(dict(
        transcript='\n'.join([result['alternatives'][0]['transcript'] for result in results])),
        status=200
    )
