import logging
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

class CustomFormatter (logging.Formatter):
    """
    Un formato de logging personalizado que incluye colores y formato de tiempo.
    """
    COLORS = {
        logging.DEBUG: Fore.CYAN + Style.BRIGHT,
        logging.INFO: Fore.BLUE + Style.BRIGHT,
        logging.WARNING: Fore.YELLOW + Style.BRIGHT,
        logging.ERROR: Fore.RED + Style.BRIGHT,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT
    }

    GRAY = Fore.LIGHTBLACK_EX

    PURPLE = Fore.MAGENTA

    def format(self, record):
        """
        Formatea el registro de logging con colores y un formato de tiempo específico.
        Args:
            record (logging.LogRecord): El registro de logging a formatear.
        Returns:
            str: El registro formateado como una cadena de texto.
        """
        level_color = self.COLORS.get(record.levelno, "")
        time_str = Style.BRIGHT + self.GRAY + datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        levelname = f"{level_color}{record.levelname:<8}{Style.RESET_ALL}"
        message = f"{record.getMessage()}"
        return f"{time_str} {levelname}\t{self.PURPLE}{record.name}{Style.RESET_ALL} {message}"

def get_logger(name: str = "BOT", level: int = logging.INFO) -> logging.Logger:
    """
    Crea y configura un logger con un formato personalizado.
    Args:
        name (str): El nombre del logger. Por defecto es "BOT".
        level (int): El nivel de logging. Por defecto es logging.INFO.
    Returns:
        logging.Logger: Un logger configurado con el formato personalizado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

    return logger