import logging
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

class CustomFormatter (logging.Formatter):
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
        level_color = self.COLORS.get(record.levelno, "")
        time_str = Style.BRIGHT + self.GRAY + datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        levelname = f"{level_color}{record.levelname:<8}{Style.RESET_ALL}"
        message = f"{record.getMessage()}"
        return f"{time_str} {levelname}\t{self.PURPLE}{record.name}{Style.RESET_ALL} {message}"

def get_logger(name: str = "BOT", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)

    return logger