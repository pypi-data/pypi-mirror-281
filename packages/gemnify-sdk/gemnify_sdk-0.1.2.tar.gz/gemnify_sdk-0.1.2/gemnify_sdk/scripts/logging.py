import logging

def getLogger(config):
    switcher = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
        "fatal": logging.FATAL
    }
    logger = logging.getLogger("gemnify_logger")
    logger.setLevel(switcher.get(config.logger_level.lower(), "info"))

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger