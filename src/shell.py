from interface import SomeThing


def main():
    handler = SomeThing()

    while True:
        try:
            user_input = input("Shell> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            command = parts[0]
            args = parts[1:]

            if command == "exit":
                break

            if not hasattr(handler, command):
                print(f"[{command}] INVALID COMMAND")
                continue

            method = getattr(handler, command)
            result = method(*args)
            print(f"[{command}] {result}")

        except Exception as e:
            print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    main()
