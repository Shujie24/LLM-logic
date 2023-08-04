from backend import get_response


class Generator:
    def __init__(self, model: str):
        self.model = model
        self.history = []

    def clear_history(self):
        self.history = []

    def gen(self, prompt, **kwargs):
        num_bs = len(prompt)
        num_gen = kwargs.get("n", 1)  # number of generations
        generated = [["" for _ in range(num_gen)] for _ in range(num_bs)]

        response = get_response(prompt=prompt, model=self.model, **kwargs)

        self.history.append(response)
        for choice in response.choices:
            idx_bs = choice.index // num_gen
            idx_gen = choice.index % num_gen
            if "gpt-3.5-turbo" not in self.model:
                generated[idx_bs][idx_gen] = choice.text
            else:
                generated[idx_bs][idx_gen] = choice.message.content
        return generated