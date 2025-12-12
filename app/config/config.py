from dotenv import load_dotenv
import os 
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("環境変数 GOOGLE_API_KEY が設定されていません。")

MODEL_NAME = "gemini-2.5-flash"
