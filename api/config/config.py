from dotenv import load_dotenv
import os
from pathlib import Path
import tomllib

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("環境変数 GOOGLE_API_KEY が設定されていません。")

BASE_DIR = Path(__file__).resolve().parent
SETTING_PATH = BASE_DIR / "setting.toml"


def load_setting() -> dict:
    if not SETTING_PATH.exists():
        raise RuntimeError(f"設定ファイルが見つかりません: {SETTING_PATH}")

    with SETTING_PATH.open("rb") as f:
        return tomllib.load(f)


def load_prompt(data: dict) -> str:
    instruction = data.get("instruction")
    prompt = instruction.get("prompt") if isinstance(instruction, dict) else None
    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError("設定ファイルに instruction.prompt を設定してください。")

    return prompt


def load_model(data: dict) -> str:
    model = data.get("model")
    name = model.get("name") if isinstance(model, dict) else None
    if not isinstance(name, str) or not name.strip():
        raise RuntimeError("設定ファイルに model.name を設定してください。")

    return name


data = load_setting()

SYSTEM_INSTRUCTION = load_prompt(data)
MODEL_NAME = load_model(data)
