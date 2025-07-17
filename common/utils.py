# SPDX-FileCopyrightText: 2025 Taras Paruta (partarstu@gmail.com)
#
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import mimetypes
import os.path
from pathlib import Path
from pydantic_ai import BinaryContent

import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_logger(name):
    log_level = config.LOG_LEVEL
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger


def fetch_media_file_content(remote_file_path: str, attachments_local_folder_path: str) -> BinaryContent:
    file_name = Path(remote_file_path).name
    local_file_path = Path(os.path.join(attachments_local_folder_path, file_name)).resolve()
    if not local_file_path.is_file():
        raise RuntimeError(f"File {local_file_path} does not exist.")
    mime_type, _ = mimetypes.guess_type(local_file_path)
    if mime_type and mime_type.startswith(("audio", "video", "image")):
        return BinaryContent(
            data=Path(local_file_path).read_bytes(),
            media_type=mime_type or "application/octet-stream",
        )
    else:
        raise RuntimeError(f"File {local_file_path} is not a media file or mime type could not be determined.")
