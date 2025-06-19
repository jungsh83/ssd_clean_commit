from src.shell_commands.command_action import CommandAction
from src.ssd_file_manager import SSDFileManager
from src.ssd_driver import SSDDriver
import sys
import re
from pathlib import Path

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def resolve_command(name):
    handler = CommandAction.registry.get(name)
    if handler:
        return handler, name

    for cls in CommandAction.registry.values():
        if name in getattr(cls, '_alias', []):
            return cls, cls.command_name
    return None, name


def execute_command(command: str, args: list[str], ssd_driver):
    handler, resolved_name = resolve_command(command)

    if not handler:
        raise Exception(f"[{command.upper()}] INVALID COMMAND")

    handler_instance = handler(ssd_driver, *args)
    result = handler_instance.run()
    return resolved_name, result


def shell_mode(ssd_driver=SSDDriver()):
    while True:
        try:
            user_input = input("Shell> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            resolved_command, result = execute_command(command, args, ssd_driver)

            if result:
                print(f"[{resolved_command.upper()}] {result}")

            if resolved_command == 'exit':
                break

        except Exception as e:
            print(f"[ERROR] {str(e)}")


def runner_mode(file_path: str, ssd_driver=SSDDriver()):
    path = Path(file_path)
    if not path.exists():
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(EXIT_FAILURE)

    failed = False

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if not re.fullmatch(r"\d+_[^\s]*", line):
                print(f"[{line.upper()}] INVALID COMMAND")
                failed = True
                break

            command = line
            handler, resolved_name = resolve_command(command)

            if not handler:
                print(f"[{command.upper()}] INVALID COMMAND")
                failed = True
                break

            label = f"{resolved_name.upper():<20}"
            print(f"{label} ___   RUN...", end="")

            try:
                _, result = execute_command(command, [], ssd_driver)

                if result not in {"PASS", "FAIL"}:
                    failed = True
                    raise Exception(f"Test Scenario Returned {result}. Return should be in {{'PASS', 'FAIL'}}")

                print(f"  {result}")
                if result == "FAIL":
                    failed = True
                    break

            except Exception as e:
                print(f"FAIL WITH ERROR. {str(e)}")
                failed = True
                break

    sys.exit(EXIT_FAILURE if failed else EXIT_SUCCESS)


if __name__ == "__main__":
    ssd_driver = SSDDriver()
    if len(sys.argv) == 2 and sys.argv[1].endswith(".txt"):
        runner_mode(sys.argv[1], ssd_driver)
    else:
        shell_mode(ssd_driver)
