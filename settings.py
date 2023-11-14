import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

API_ID = os.getenv('API_ID')

API_HASH = os.getenv('API_HASH')

REFRESH_TIME = 60  # Как часто проверять новые посты, время в секундах

ADMIN_CHANEL = 'https://t.me/+nGpqukMqWKlkMDVi'

CHANNELS_DONOR = ['https://t.me/+QidF0v6evBE4MjYy', 'https://t.me/+syj8zVecWCtlZTRi',
                  'https://t.me/+6vE4vMJ4lb8xOWVi', 'https://t.me/+zvA5AOweoepmMjky',
                  'https://t.me/+OmtYNpv7JtgzYjYy', 'https://t.me/+Z3Cf7YaFvB5hNGQx',
                  'https://t.me/+DBivdVcjRpZmNGYx', 'https://t.me/+7QA5pwsrLrpiNmU6',
                  'https://t.me/+G3k-d_lRLR81YWQy', 'https://t.me/+KMQmRFPSP4E3NjJi',
                  'https://t.me/+ASMTgmSIInM4Yjdi', 'https://t.me/+yFssC13043xhODgy']
