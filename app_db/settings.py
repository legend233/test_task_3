from dotenv import load_dotenv
import os

# загрузка переменных окружения
load_dotenv()
DB = os.getenv('DB')
