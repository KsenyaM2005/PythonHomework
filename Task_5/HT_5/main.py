from log_meneger import LogLevel, LogManager
import functools
import json, os



# Автоматическое использование логов опасных уровней
DEFAULT_LEVEL_MAP = {
    # WARN
    FileNotFoundError:      LogLevel.WARN,
    KeyError:               LogLevel.WARN,

    # ERROR
    ZeroDivisionError:      LogLevel.ERROR,
    ValueError:             LogLevel.ERROR,
    TypeError:              LogLevel.ERROR,
    IndexError:             LogLevel.ERROR,
    AttributeError:         LogLevel.ERROR,
    PermissionError:        LogLevel.ERROR,
    ConnectionError:        LogLevel.ERROR,
    TimeoutError:           LogLevel.ERROR,
    OSError:                LogLevel.ERROR,

    # FATAL
    MemoryError:            LogLevel.FATAL,
    SystemExit:             LogLevel.FATAL,
    RecursionError:         LogLevel.FATAL,
}



def _resolve_level(exc, mapping, default=LogLevel.ERROR):
    for cls in type(exc).__mro__:
        if cls in mapping:
            return mapping[cls]
    return default



# Декоратор для автоматического использования логов опасных уровней
def auto_log(logger, source=None, event_id=None, user=None,
             extra=None, level_map=None,
             reraise=True,              # True — пробросить исключение дальше,
                                        # False — вернуть default и «проглотить»
             default=None               # значение, возвращаемое при reraise=False
             ):


    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                _src = source or func.__qualname__
                level = _resolve_level(exc, level_map or DEFAULT_LEVEL_MAP)
                logger.log(
                    level=level,
                    source=_src,
                    message=f"{type(exc).__name__}: {exc}",
                    event_id=event_id,
                    user=user,
                    extra=extra,
                    exc_info=True,
                )
                if reraise:
                    raise
                return default
        return wrapper
    return decorator



# ПРИМЕРЫ
logger = LogManager(
        filename="Log.txt",
        min_level=LogLevel.DEBUG,
        console_output=True,
        append=False
    )


@auto_log(logger, source="Calculator", event_id="CALC_500",
          user="session_42", reraise=False,)
def divide(a, b):
    return a / b

@auto_log(logger, source="ConfigLoader", event_id="CFG_LOAD",
          reraise=False, default={})
def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

@auto_log(logger, source="EndlessRecursion", event_id="ALG_INF_REC",
          user="worker_01", reraise=False)
def endless_recursion(n: int):
    return endless_recursion(n)


if __name__ == "__main__":

    # INFO
    logger.info(
        source="CityList",
        message="Житель успешно добавлен",
        event_id="AUTH_001",
        user="ivan_petrov"
    )

    # DEBUG
    logger.debug(
        source="DatabaseConnector",
        message="Выполнен SQL-запрос",
        event_id="DB_QUERY",
        extra={"query": "SELECT * FROM users", "duration_ms": 45}
    )


    # WARN
    load_config("unexistence_config.json")

    # ERROR
    divide(10, 0)

    # FATAL
    endless_recursion(10)

