import inspect
from datetime import datetime
from pathlib import Path


class _CustomLogger:
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / "latest.log"
    MAX_SIZE = 10 * 1024  # 10kB

    def __init__(self):
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)
        self._rotate_if_needed()
        self._patch_print()

    def _rotate_if_needed(self):
        if not (self.LOG_FILE.exists() and self.LOG_FILE.stat().st_size > self.MAX_SIZE):
            return

        rotated_path = self._generate_rotated_path()
        self._compress_existing_backups()
        self.LOG_FILE.rename(rotated_path)

    def _generate_rotated_path(self) -> Path:
        timestamp = datetime.now().strftime("until_%y%m%d_%Hh_%Mm_%Ss")
        return self.LOG_DIR / f"{timestamp}.log"

    def _compress_existing_backups(self):
        for f in self.LOG_DIR.glob("until_*.log"):
            zip_path = f.with_suffix(".zip")
            if zip_path.exists():
                zip_path.unlink()
            f.rename(zip_path)

    def _patch_print(self):
        builtin_print = print

        def patched_print(*args, **kwargs):
            message = " ".join(str(arg) for arg in args)

            self.info(message)

            builtin_print(*args, **kwargs)

        __builtins__['print'] = patched_print

    def _log(self, level: str, message: str):
        self._rotate_if_needed()

        frame = inspect.stack()[2]
        class_name = frame.frame.f_locals.get('self', type('', (), {})).__class__.__name__
        func_name = frame.function

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        padded_func = f"{class_name}.{func_name}()".ljust(30)
        formatted = f"[{timestamp}] [{level}] {padded_func}: {message}"

        self.LOG_DIR.mkdir(exist_ok=True)

        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")

    def info(self, message: str):
        self._log("INFO ", message)

    def error(self, message: str):
        self._log("ERROR", message)

    def debug(self, message: str):
        self._log("DEBUG", message)


class LoggerSingleton:
    _instance = None

    @classmethod
    def get_logger(cls):
        if cls._instance is None:
            cls._instance = _CustomLogger()
        return cls._instance
