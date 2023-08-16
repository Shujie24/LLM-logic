import openai 

def prepare_prompt(system, user, assistant) -> list:
    messages = [
        {"role": "user", "content": user},
        {"role": "system", "content": system},
        {"role": "assistant", "content": assistant}
    ]
    return messages


def call_openai_api(prompt_messages, model="gpt-3.5-turbo", temperature=0) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature = temperature)
    return response["choices"][0]["message"]["content"]