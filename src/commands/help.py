from src.commands.command_action import CommandAction, InvalidArgumentException
from src.decorators import log_call

class HelpCommand(CommandAction):
    command_name: str = 'help'
    _description = 'Show list of available commands.'
    _usage = 'help'
    _author = 'Songju Na'
    _alias: list[str] = ['h']

    @log_call(level="INFO")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @log_call(level="INFO")
    def run(self):
        if not self.validate():
            raise InvalidArgumentException(
                f"{self.__class__.command_name} takes no arguments, but got {self._arguments}")

        for name, cls in sorted(CommandAction.registry.items()):
            print(f"\n▶ {name}")
            print(f"  - Description : {getattr(cls, '_description', 'No description')}")
            print(f"  - Usage       : {getattr(cls, '_usage', 'No usage')}")
            team_name = getattr(cls, '_team_name', "")
            print(f"  - Author      : [{team_name}] {getattr(cls, '_author', 'Unknown')}")

            aliases = getattr(cls, '_alias', [])
            if aliases:
                print(f"  - Alias       : {', '.join(aliases)}")

    def validate(self) -> bool:
        return self._arguments == ()
