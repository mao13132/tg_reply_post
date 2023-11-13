import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

ADMIN = ['']

API_ID = os.getenv('API_ID')

API_HASH = os.getenv('API_HASH')

START_MESSAGE = 'Стартовое сообщение'

CHANNELS_DONOR = ['-1002017070550', 'https://t.me/chahhanelsB']

ADMIN_CHANEL = '-1001769946855'

