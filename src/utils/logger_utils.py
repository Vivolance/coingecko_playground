import logging


def logger_setup(logger: logging.Logger) -> None:
    """
    For this function, setup the logger with a stream handler and log formatter
    """
    handler: logging.Handler = logging.StreamHandler()
    formatter: logging.Formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)