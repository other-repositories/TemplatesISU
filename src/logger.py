import datetime

class CustomLogger:
    # Общие настройки (глобальные для класса)
    _log_to_console = True
    _log_to_file = False
    _log_file = "application.log"
    _levels = {"DEBUG": 1, "INFO": 2, "WARNING": 3, "ERROR": 4, "CRITICAL": 5}
    _current_level = "DEBUG"  # Уровень логирования по умолчанию

    @staticmethod
    def configure(log_to_console=True, log_to_file=False, log_file="application.log", level="DEBUG"):
        """Настраивает параметры логгера."""
        CustomLogger._log_to_console = log_to_console
        CustomLogger._log_to_file = log_to_file
        CustomLogger._log_file = log_file
        if level in CustomLogger._levels:
            CustomLogger._current_level = level
        else:
            raise ValueError(f"Некорректный уровень логирования: {level}")

    @staticmethod
    def _should_log(level):
        """Проверяет, нужно ли логировать сообщение текущего уровня."""
        return CustomLogger._levels[level] >= CustomLogger._levels[CustomLogger._current_level]

    @staticmethod
    def _log_message(level, message):
        """Форматирует и логирует сообщение."""
        if CustomLogger._should_log(level):
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"{timestamp} - {level} - {message}"

            # Логируем в консоль
            if CustomLogger._log_to_console:
                print(formatted_message)

            # Логируем в файл
            if CustomLogger._log_to_file:
                with open(CustomLogger._log_file, "a") as f:
                    f.write(formatted_message + "\n")

    @staticmethod
    def debug(message):
        CustomLogger._log_message("DEBUG", message)

    @staticmethod
    def info(message):
        CustomLogger._log_message("INFO", message)

    @staticmethod
    def warning(message):
        CustomLogger._log_message("WARNING", message)

    @staticmethod
    def error(message):
        CustomLogger._log_message("ERROR", message)

    @staticmethod
    def critical(message):
        CustomLogger._log_message("CRITICAL", message)
