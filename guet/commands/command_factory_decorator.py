from typing import List

from guet.commands.command_factory import CommandFactoryMethod
from guet.settings.settings import Settings


class CommandFactoryDecorator(CommandFactoryMethod):
    def __init__(self, decorated: CommandFactoryMethod):
        self.decorated = decorated

    def short_help_message(self):
        self.decorated.short_help_message()

    def build(self, args: List[str], settings: Settings):
        raise NotImplementedError