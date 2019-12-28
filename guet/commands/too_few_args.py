from typing import List

from guet.settings.settings import Settings
from guet.commands.strategy import CommandStrategy


class TooFewArgsStrategy(CommandStrategy):
    def __init__(self, help_message):
        super().__init__()
        self._help_message = help_message

    def apply(self, args: List[str], settings: Settings):
        print('Not enough arguments.')
        print('')
        print(self._help_message)
