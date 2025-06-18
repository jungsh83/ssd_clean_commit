from src.commands.command_action import CommandAction
from src.ssd import VirtualSSD
from src.ssd_driver import SSDDriver

def resolve_command(name):
    handler = CommandAction.registry.get(name)
    if handler:
        return handler, name

    for cls in CommandAction.registry.values():
        if name in getattr(cls, '_alias', []):
            return cls, cls.command_name
    return None, name


def main(ssd_driver = SSDDriver()):
    while True:
        try:
            user_input = input("Shell> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            handler, command = resolve_command(command)

            if not handler:
                print(f"[{command.upper()}] INVALID COMMAND")
                continue

            handler_instance = handler(ssd_driver, *args)
            result = handler_instance.run()

            if result:
                print(f"[{command.upper()}] {result}")

            if command == 'exit':
                break

        except Exception as e:
            print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    main(SSDDriver())
