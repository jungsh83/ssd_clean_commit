# src/decorators.py
import inspect
from functools import wraps
from src.logger import LoggerSingleton


def log_call(level="INFO"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggerSingleton.get_logger()

            # 클래스명.함수명() 구성
            bound_func = inspect.signature(func).bind(*args, **kwargs)
            bound_func.apply_defaults()
            arg_str = ", ".join(f"{k}={v!r}" for k, v in bound_func.arguments.items())

            logger_method = getattr(logger, level.lower(), logger.info)

            try:
                logger_method(f"[CALL] {func.__qualname__}({arg_str})")
                result = func(*args, **kwargs)
                logger_method(f"[RETURN] {func.__qualname__} → {result!r}")
                return result
            except Exception as e:
                logger.error(f"[EXCEPTION] {func.__qualname__} raised {e!r}")
                raise

        return wrapper

    return decorator
