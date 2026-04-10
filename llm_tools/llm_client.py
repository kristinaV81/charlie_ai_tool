import os
from groq import Groq


MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_charlie_message(system_prompt: str, messages: list[dict]) -> str:
    """

    :param system_prompt: prompt from prompts.py
    :param messages: message from Charlie
    :return:
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            *messages,
        ],
        temperature=0.4,
        max_tokens=80,
    )

    content = response.choices[0].message.content or ""
    return content.strip()


def generate_raw_completion(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2,
    max_tokens: int = 120,
) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    content = response.choices[0].message.content or ""
    return content.strip()
