# used for fault tolerance

from firebase_functions import logger
from collections.abc import Callable
import time

def retry_wrapper(func: Callable, max_retries:int =3, base_delay:int = 1, max_delay: int =60) -> None:
    """
    Wrapper function to add retry logic around a given function. uses exponential backoff
    """
    delay = base_delay
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            logger.error(f"Attempt {i+1} failed: {e}")
            if i < max_retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay = min(delay * 2, max_delay)
    logger.error("Max retries reached. Operation failed.")
    raise Exception("Max retries reached. Operation failed.")