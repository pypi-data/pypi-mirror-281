import os
from thinkup_cli.utils.singleton import singleton


@singleton
class App:
    version: str = "1.0.2"

    def init(self):
        os.system('printf "\033c"')
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def close():
        os.system('printf "\033c"')
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()