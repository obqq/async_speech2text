import os

DEBUG: bool = bool(int(os.environ['DEBUG']))

# Authentication service
PUBLIC_KEY_URL = 'http://localhost:8000/api/auth/public_key'

# Third-party API's keys

# Google Speech-To_Text

GOOGLE_STT_API_KEY = os.environ.get('GOOGLE_STT_API_KEY')
GOOGLE_STT_API_URL = f'https://speech.googleapis.com/v1/speech:recognize?key={GOOGLE_STT_API_KEY}'