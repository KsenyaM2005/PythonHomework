import os
import json
import traceback
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
import threading



class LogLevel(Enum):
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    FATAL = 50



class LogManager:

    def __init__(self,
                 filename: str = "Log.txt",            # Путь к лог-файлу
                 min_level: LogLevel = LogLevel.DEBUG, # Минимальный уровень для записи
                 console_output: bool = True,          # Дублировать ли записи в консоль
                 append: bool = True                   # True — дописывать в файл, False — перезаписывать
                 ):

        self.filename = filename
        self.min_level = min_level
        self.console_output = console_output
        self._write_lock = threading.Lock()

        # Создаём файл, если его нет, или перезаписываем при append=False
        mode = 'a' if append else 'w'
        with open(self.filename, mode, encoding='utf-8') as f:
            if not append or os.path.getsize(self.filename) == 0:
                f.write(f"# Лог-файл создан: {datetime.now().isoformat()}\n")




    def _format_record(self, level: LogLevel, source: str, message: str,
                       event_id: Optional[str] = None,
                       user: Optional[str] = None,
                       extra: Optional[Dict[str, Any]] = None) -> str:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        record = (
            f"[{timestamp}] "
            f"[{level}] "
            f"[{source}] "
            f"[ID:{event_id or '-'}] "
            f"[User:{user or '-'}] "
            f"{message}"
        )

        if extra:
            try:
                extra_str = json.dumps(extra, ensure_ascii=False, default=str)
                record += f" | EXTRA: {extra_str}"
            except (TypeError, ValueError):
                record += f" | EXTRA: {str(extra)}"

        return record




    def _write(self, record: str) -> None:
        with self._write_lock:
            try:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write(record + '\n')
            except IOError as e:
                print(f"Ошибка записи в лог-файл: {e}")

            if self.console_output:
                print(record)



    def log(self,
            level: LogLevel,                            # Уровень серьёзности
            source: str,                                # Источник события
            message: str,                               # Сообщение
            event_id: Optional[str] = None,             # Уникальный идентификатор события
            user: Optional[str] = None,                 # Пользователь или сессия
            extra: Optional[Dict[str, Any]] = None,     # Дополнительная информация (dict)
            exc_info: bool = False                      # Добавить стек вызовов текущего исключения
            ) -> None:

        if level.value < self.min_level.value:
            return

        if exc_info:
            extra = extra.copy() if extra else {}
            try:
                tb = traceback.format_exc(limit=20)
                if len(tb) > 8000:
                    tb = tb[:4000] + "\n...[обрезано]...\n" + tb[-4000:]
                extra['traceback'] = tb
            except Exception as tb_err:
                extra['traceback'] = f"<не удалось получить traceback: {tb_err}>"


        record = self._format_record(level, source, message, event_id, user, extra)
        self._write(record)



    # методы-обёртки

    def debug(self, source: str, message: str, **kwargs) -> None:
        self.log(LogLevel.DEBUG, source, message, **kwargs)

    def info(self, source: str, message: str, **kwargs) -> None:
        self.log(LogLevel.INFO, source, message, **kwargs)

    def warn(self, source: str, message: str, **kwargs) -> None:
        self.log(LogLevel.WARN, source, message, **kwargs)

    def error(self, source: str, message: str, **kwargs) -> None:
        self.log(LogLevel.ERROR, source, message, **kwargs)

    def fatal(self, source: str, message: str, **kwargs) -> None:
        self.log(LogLevel.FATAL, source, message, **kwargs)