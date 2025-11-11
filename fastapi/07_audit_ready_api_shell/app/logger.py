from pythonjsonlogger import jsonlogger
import logging

def setup_logger():
    api_logger = logging.getLogger("api_logger")
    api_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    handler.setFormatter(formatter)
    api_logger.addHandler(handler)
    return api_logger

logger = setup_logger()