import logging
from rich.logging import RichHandler
from src.config import DEBUG

CONSOLE_LEVEL = logging.DEBUG if DEBUG else logging.INFO

# logger
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

# handler
console_handler = RichHandler(rich_tracebacks=True)
console_handler.setLevel(CONSOLE_LEVEL)

# formatting
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)

# add handler
logger.addHandler(console_handler)