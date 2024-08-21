import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")