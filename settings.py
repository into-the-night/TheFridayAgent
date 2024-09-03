from dotenv import load_dotenv
import os
load_dotenv()

class Settings():
    os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
    pv_access_key = os.getenv("PVPORCUPINE_ACCESS_KEY")
    tvly_api_key = os.getenv("TAVILY_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
