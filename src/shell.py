from src.command_action import CommandAction
from src.ssd import VirtualSSD

def resolve_command(name):
    handler = CommandAction.registry.get(name)
    if handler:
        return handler
    # alias 탐색
    for cls in CommandAction.registry.values():
        if name in getattr(cls, 'alias', []):
            return cls
    return None

def main():
    ssd_driver = VirtualSSD()
    while True:
        try:
            user_input = input("Shell> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                print(f"[{command.upper()}]")
                break

            handler = resolve_command(command)

            if not handler:

                print(f"[{command.upper()}] INVALID COMMAND")
                continue

            handler_instance = handler(ssd_driver)

            result = handler_instance.run(*args)

            if result:
                print(f"[{command.upper()}] {result}")

        except Exception as e:
            print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    main()
