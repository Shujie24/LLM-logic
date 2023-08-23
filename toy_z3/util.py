import openai 


def make_message(content, role):
    if role == "user":
        return {"role": "user", "content": content}
    if role == "system":
        return {"role": "system", "content": content}
    if role == "assistant":
        return {"role": "assistant", "content": content}
    if role == "":
        return 

def prepare_prompt(sys_message, conversation):
    messages = [make_message(sys_message, "system")]
    for i, msg in enumerate(conversation):
        if i % 2 == 0:
            messages.append(make_message(msg, "user"))
        else:
            messages.append(make_message(msg, "assistant"))
    return messages

def call_openai_api(messages, model="gpt-3.5-turbo", temperature=0) -> str:
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature = temperature)
    token_used = response["usage"]["total_tokens"]
    return response["choices"][0]["message"]["content"], token_used
