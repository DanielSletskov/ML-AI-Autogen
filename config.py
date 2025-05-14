from dotenv import load_dotenv
import os

load_dotenv()

LLM_CONFIG = {
    "config_list": [
        {
            "model": os.getenv("MISTRAL_MODEL", "open-mistral-nemo"),
            "api_key": os.getenv("MISTRAL_API_KEY"),
            # Other parameters (hard‑coded defaults or override via .env as needed)
            "api_type": os.getenv("MISTRAL_API_TYPE", "mistral"),
            #"api_rate_limit": float(os.getenv("MISTRAL_API_RATE_LIMIT", 0.25)),
            #"repeat_penalty": float(os.getenv("MISTRAL_REPEAT_PENALTY", 1.1)),
            "temperature": float(os.getenv("MISTRAL_TEMPERATURE", 0.0)),
            #"seed": int(os.getenv("MISTRAL_SEED", 42)),
            "stream": os.getenv("MISTRAL_STREAM", "False").lower() in ("true", "1"),
            #"native_tool_calls": os.getenv("MISTRAL_NATIVE_TOOL_CALLS", "False").lower() in ("true", "1"),
            #"cache_seed": None,
        }
    ]
}