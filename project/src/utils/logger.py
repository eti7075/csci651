import logging

def get_logger(name="P2P"):
    """Returns a configured logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(ch)

    return logger

# Example usage
logger = get_logger()
logger.info("Logger initialized.")
