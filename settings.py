import os

from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN2")

STATUS_TELEGRAM_TOKEN = os.getenv('STATUS_TELEGRAM_TOKEN')

MY_ID=os.getenv('MY_ID')
WIFE_ID=os.getenv('WIFE_ID')


WHITE_USERS = [
    int(MY_ID),
    int(WIFE_ID)
]