from dotenv import load_dotenv
import os
from pathlib import Path
import tomllib

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("環境変数 GOOGLE_API_KEY が設定されていません。")

MODEL_NAME = "gemini-3.5-flash"

BASE_DIR = Path(__file__).resolve().parent
INSTRUCTION_PROMPT_PATH = BASE_DIR / "instruction_prompt.toml"


def load_instruction_prompt(path: Path = INSTRUCTION_PROMPT_PATH) -> str:
    if not path.exists():
        raise RuntimeError(f"指示プロンプト設定ファイルが見つかりません: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    prompt = data.get("instruction", {}).get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        raise RuntimeError(
            "指示プロンプト設定ファイルに instruction.prompt を設定してください。"
        )

    return prompt


SYSTEM_INSTRUCTION = load_instruction_prompt()
