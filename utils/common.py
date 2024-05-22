import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_execution(func):
    def wrapper(*args, **kwargs):
        logging.info(f"Starting {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Completed {func.__name__}")
        return result
    return wrapper
