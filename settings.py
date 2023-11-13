import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

API_ID = os.getenv('API_ID')

API_HASH = os.getenv('API_HASH')

REFRESH_TIME = 60  # Как часто проверять новые посты, время в секундах

ADMIN_CHANEL = '-1001769946855'

CHANNELS_DONOR = ['https://t.me/CahanellslsA', 'https://t.me/chahhanelsB']
