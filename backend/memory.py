class ChatMemory:
    def __init__(self):
        self.history = []

    def add_user(self, text):
        self.history.append({"role": "user", "content": text})

    def add_bot(self, text):
        self.history.append({"role": "assistant", "content": text})

    def get_history(self):
        return self.history