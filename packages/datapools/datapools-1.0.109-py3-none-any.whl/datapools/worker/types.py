from typing import NamedTuple, Optional
from enum import Enum

# from ..common.storage import FileStorage
from ..common.types import DatapoolContentType
from pydantic import AnyUrl
from ..common.session_manager import Session


class YieldResult(Enum):
    NoResult = 0
    ContentDownloadSuccess = 1
    ContentDownloadFailure = 2
    ContentIgnored = 3


class WorkerContext:
    session: Session
    yield_result: YieldResult
    # storage: FileStorage


class WorkerTask(NamedTuple):
    url: AnyUrl
    content_type: Optional[DatapoolContentType] = None
