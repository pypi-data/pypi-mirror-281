import enum
import os


class ModelTypes(enum.Enum):
    llama_3_8b_instruct = "llama_3_8b_instruct"
    llama_3_8b_chat = "llama_3_8b_chat"
    llama_3_70b_instruct = "llama_3_70b_instruct"
    gpt_4 = "gpt_4"
    gpt_3_5_turbo = "gpt_3_5_turbo"


"""
If we are running in a mode where each request should provide their own credentials
"""
SAAS_MODE = os.environ.get("OPTIMODEL_SAAS_MODE", None)
