import json
import logging
import time
from typing import Any

import requests

logger = logging.getLogger('mediacatch.vision.result')


def wait_for_result(
    file_id: str,
    url: str = 'https://api.mediacatch.io/vision',
    timeout: int = 3600,
    delay: int = 30,
) -> dict[str, Any] | None:
    """Wait for result from a URL.

    Args:
        file_id (str): The file ID to get the result from.
        url (str): The URL to get the result from.
        timeout (int, optional): Timeout for waiting in seconds. Defaults to 3600.
        delay (int, optional): Delay between each request. Defaults to 5.

    Returns:
        dict[str, Any] | None: Dictionary with the result from the URL or None if failed.
    """
    result_url = f'{url}/result/{file_id}'
    logger.info(f'Waiting for result from {result_url}')
    start_time = time.time()
    end_time = start_time + timeout
    while time.time() < end_time:
        try:
            response = requests.get(result_url)
            response.raise_for_status()
            result = response.json()
            elapsed_time = time.time() - start_time
            logger.info(f'Got result from {result_url} in {elapsed_time:.2f} seconds')
            return result

        except (requests.RequestException, json.JSONDecodeError):
            time.sleep(delay)

        except Exception as e:
            logger.error(f'Failed to get result from {result_url}: {e}')
            return None

    logger.error(f'Timeout waiting for result from {result_url}, give up')
    return None
