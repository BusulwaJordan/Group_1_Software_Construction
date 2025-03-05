from strategies.share_strategy import ShareStrategy

class NoteSharingContext:
    def __init__(self, strategy: ShareStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ShareStrategy):
        self._strategy = strategy

    def share_note(self, title, content):
        self._strategy.share(title, content)