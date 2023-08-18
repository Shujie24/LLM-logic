import os
import sys
import openai
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    after_log,
    before_sleep_log,
)  # for exponential backoff
import logging

logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
logger = logging.getLogger(__name__)

# openai.api_key = os.getenv("OPENAI_API_KEY")


def get_model_name(model):
    if model == "codex":
        return "code-davinci-002"
    if model == "chat":
        return "gpt-3.5-turbo"
    return model


@retry(
    wait=wait_random_exponential(min=1, max=60),
    before_sleep=before_sleep_log(logger, logging.ERROR),
)
def get_response(prompt, model, **kwargs):
    if "gpt-3.5-turbo" not in model:
        # original completion model
        res = openai.Completion.create(prompt=prompt, model=model, **kwargs)
    else:
        # chat completion model
        res = openai.ChatCompletion.create(model=model, messages=prompt[0])

    print("usage", res.usage)
    return res