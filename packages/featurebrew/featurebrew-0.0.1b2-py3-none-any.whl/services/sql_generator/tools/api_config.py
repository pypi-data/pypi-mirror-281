import os
# set your OPENAI_API_BASE, OPENAI_API_KEY here!
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")

import openai
openai.api_key = OPENAI_API_KEY

MODEL_NAME = os.getenv("MODEL", 'gpt-4o')
# MODEL_NAME = 'CodeLlama-7b-hf'
# MODEL_NAME = 'gpt-4-32k'
# MODEL_NAME = 'gpt-4'
# MODEL_NAME = 'gpt-35-turbo-16k'