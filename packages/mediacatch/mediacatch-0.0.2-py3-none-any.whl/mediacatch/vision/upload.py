import json
import logging
from typing import Any, Literal

import requests

from mediacatch import mediacatch_api_key

logger = logging.getLogger('mediacatch.vision.upload')

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'X-API-KEY': f'{mediacatch_api_key}',
}


def upload(
    fpath: str,
    type: Literal['ocr', 'face'],
    url: str = 'https://api.mediacatch.io/vision',
    extra: dict[str, Any] = {},
) -> str:
    """Upload a file to MediaCatch Vision API.

    Args:
        fpath (str): File path.
        type (Literal['ocr', 'face']): Type of inference to run on the file.
        url (str, optional): URL to the vision API. Defaults to 'https://api.mediacatch.io/vision'.
        extra (dict[str, Any], optional): Dictonary with extra parameters. Defaults to {}.

    Returns:
        str: File ID.
    """
    logger.info(f'Uploading file {fpath} to MediaCatch Vision API')

    # Get presigned URL
    data = {'filename': fpath, 'type': type, 'extra': extra}
    response = requests.post(f'{url}/upload/', headers=headers, data=json.dumps(data))
    assert (
        response.status_code == 201
    ), f'Failed to upload file {fpath} to MediaCatch Vision API: {response.text}'
    response_data = response.json()
    file_id = response_data['file_id']

    # Upload file to storage
    with open(fpath, 'rb') as f:
        files = {'file': (response_data['fields']['key'], f)}
        response = requests.post(response_data['url'], data=response_data['fields'], files=files)

    # Mark file as uploaded
    data = {'file_id': file_id}
    response = requests.post(f'{url}/upload/complete/', headers=headers, data=json.dumps(data))
    assert response.status_code == 200, f'Failed to mark file {fpath} as uploaded: {response}'

    logger.info(f'File {fpath} uploaded with ID {file_id}')
    return file_id
