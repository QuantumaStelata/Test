import logging


FILE_LOG = logging.FileHandler('log/logging.log', mode = 'w', encoding= 'utf-8')
CONSOLE_LOG = logging.StreamHandler()
SETTINGS = "%(asctime)s | %(filename)-13s | %(levelname)-8s | %(message)s"
DATE_SETTINGS = '%d.%m.%Y %H:%M:%S'

logging.basicConfig(handlers=(FILE_LOG, CONSOLE_LOG), format = SETTINGS, datefmt = DATE_SETTINGS, level = logging.INFO)