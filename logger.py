import logging
from logging import Logger
from os import remove
class Log:
    log: Logger
    def __init__(self):
        remove("execution.log")
        self.log = logging.getLogger(__name__)
        logging.basicConfig(filename='execution.log', format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.INFO)

    def loginfo(self, caller: str,  message: str):
        self.log.info(f"Admin {caller.upper()}: {message}")
