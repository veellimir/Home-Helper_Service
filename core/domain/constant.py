import pathlib

from dotenv import dotenv_values

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent

base_env = dotenv_values(BASE_DIR / ".env")
env = base_env.get("ENV", "dev")

env_file = BASE_DIR / f".env.{env}"
