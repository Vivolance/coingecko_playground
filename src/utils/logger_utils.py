import logging


def logger_setup(logger: logging.Logger) -> None:
    handler: logging.Handler = logging.StreamHandler()
    formatter: logging.Formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)