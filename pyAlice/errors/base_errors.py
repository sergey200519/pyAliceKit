from pyAlice.messages.errors_message import EMBEDDED_ERRORS_MESSAGE


class BaseErrors(Exception):
    def __init__(self, text, context=None, language="en", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg = text
        self.context = context
        self.language = language

    def get_dialog(self, key):
        return EMBEDDED_ERRORS_MESSAGE.get(f"{key}-{self.language}")

    def __str__(self):
        return f"Base Error: {self.get_dialog(self.msg)}"


class SettingsEroors(BaseErrors):
    def __str__(self):
        return f"Settings Error: {self.get_dialog(self.msg)}"


class KeyWordsErrors(BaseErrors):
    def __str__(self):
        return f"Key words Error: {self.get_dialog(self.msg)}"


class IntentsErrors(BaseErrors):
    def __str__(self):
        return f"Intents Error: {self.get_dialog(self.msg)}"


class MessageErrors(BaseErrors):
    def __str__(self):
        return f"Dialogs Error: {self.get_dialog(self.msg).format(self.context)}"


class PyAliceErrors(BaseErrors):
    def __str__(self):
        return f"PyAlice Error: {self.get_dialog(self.msg)}"
