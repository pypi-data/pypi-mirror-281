import asyncio
import logging
import pytest
from pytest import fixture

from datapools.common.session_manager import Session, SessionManager, SessionStatus, POSTPONED_SESSIONS_KEY, URLState
from datapools.common.types import WorkerSettings, CrawlerHintURLStatus
from datapools.common.logger import setup_logger


# @pytest.fixture(scope="session")
# async def asyncio_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield
#     loop.close()


# TODO: move to some common lib to share among all tests
@fixture()
def setup():
    logging.info("SETUP")
    setup_logger()


@fixture()
def worker_settings(setup):
    return WorkerSettings()


@fixture()
async def session_manager(worker_settings) -> SessionManager:
    res = SessionManager(worker_settings.REDIS_HOST)
    yield res
    await res.r.delete(POSTPONED_SESSIONS_KEY)
    await res.stop()


@fixture()
async def session(session_manager) -> Session:
    res = await session_manager.create(1)
    yield res
    await session_manager.remove(res.id)


@pytest.mark.anyio
async def test_session_status(session):
    assert await session.get_last_reported_status() is None

    await session.set_last_reported_status(CrawlerHintURLStatus.Success)
    assert await session.get_last_reported_status() == CrawlerHintURLStatus.Success


@pytest.mark.anyio
async def test_postponed(session_manager):
    # no limits
    assert await session_manager.list_postponed() == []
    await session_manager.push_postponed("ses1")
    assert await session_manager.list_postponed() == ["ses1"]
    await session_manager.pop_postponed("ses1")
    assert await session_manager.list_postponed() == []

    # with limits
    assert await session_manager.list_postponed(10) == []
    await session_manager.push_postponed("ses1")
    assert await session_manager.list_postponed(10) == ["ses1"]
    await session_manager.pop_postponed("ses1")
    assert await session_manager.list_postponed(10) == []


@pytest.mark.anyio
async def test_url_state(session):
    assert await session.has_url("url1") is False
    assert await session.get_url_state("url1") is None

    # add url
    await session.add_url("url1")
    assert await session.has_url("url1") is True
    state = await session.get_url_state("url1")
    assert isinstance(state, URLState)
    assert state.worker_id == ""
    assert state.status == CrawlerHintURLStatus.Unprocessed

    # set worker
    await session.set_url_worker("url1", "worker1")
    state = await session.get_url_state("url1")
    assert isinstance(state, URLState)
    assert state.worker_id == "worker1"
    assert state.status == CrawlerHintURLStatus.Unprocessed

    # set status
    await session.set_url_status("url1", CrawlerHintURLStatus.Success)
    state = await session.get_url_state("url1")
    assert isinstance(state, URLState)
    assert state.worker_id == "worker1"
    assert state.status == CrawlerHintURLStatus.Success
