from src.logger import LogLevel
from src.shell_commands.shell_command import ShellCommand, InvalidArgumentException
from src.decorators import log_call


class HelpShellCommand(ShellCommand):
    command_name: str = 'help'
    _description = 'Show list of available shell_commands.'
    _usage = 'help'
    _author = 'Songju Na'
    _alias: list[str] = ['h']

    @log_call(level=LogLevel.INFO)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @log_call(level=LogLevel.INFO)
    def execute(self):
        if not self.validate():
            raise InvalidArgumentException(self._get_exception_string())

        for name, cls in sorted(ShellCommand.registry.items()):
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

    def _get_exception_string(self):
        return f"{self.__class__.command_name} takes no arguments, but got {self._arguments}"