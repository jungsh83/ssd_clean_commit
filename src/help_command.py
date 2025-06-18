from src.command_action import CommandAction


class HelpCommand(CommandAction):
    command_name: list[str] = 'help'
    Description = 'Show list of available commands.'
    Usage = 'help'
    Author = 'Songju Na'
    alias = ['h']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        if not self.validate():
            raise Exception(f"help command takes no arguments, but got {self._arguments}")

        for name, cls in sorted(CommandAction.registry.items()):
            print(f"\n▶ {name}")
            print(f"  - Description : {getattr(cls, 'description', 'No description')}")
            print(f"  - Usage       : {getattr(cls, 'usage', 'No usage')}")
            print(f"  - Author      : {getattr(cls, 'author', 'Unknown')}")

            aliases = getattr(cls, 'alias', [])
            if aliases:
                print(f"  - Alias       : {', '.join(aliases)}")

    def validate(self) -> bool:
        return len(self._arguments) == 0