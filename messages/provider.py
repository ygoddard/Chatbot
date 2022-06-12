class MessagesProvider(object):
    def send_text(self, text: str, _from: str, _to: str):
        raise NotImplementedError

    def send_multimedia(self, text: str, media_url: str, _from: str, _to: str):
        raise NotImplementedError
