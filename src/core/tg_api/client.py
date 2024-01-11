from contextlib import asynccontextmanager, contextmanager, AsyncExitStack
from contextvars import ContextVar, Token
from dataclasses import dataclass, KW_ONLY, field
from urllib.parse import urljoin
from typing import AsyncGenerator, ClassVar, Generator, Type, TypeVar

import httpx

from .exceptions import TgHttpStatusError, TgRuntimeError

DEFAULT_TG_SERVER_URL = 'https://api.telegram.org'

AsyncTgClientType = TypeVar('AsyncTgClientType', bound='AsyncTgClient')
SyncTgClientType = TypeVar('SyncTgClientType', bound='SyncTgClient')


@dataclass(frozen=True)
class AsyncTgClient:
    token: str
    _: KW_ONLY
    session: httpx.AsyncClient
    tg_server_url: str = DEFAULT_TG_SERVER_URL

    api_root: str = field(init=False)

    default_client: ClassVar[ContextVar['AsyncTgClient']] = ContextVar('default_client')

    def __post_init__(self) -> None:
        api_root = urljoin(self.tg_server_url, f'./bot{self.token}/')
        object.__setattr__(self, 'api_root', api_root)

    @classmethod
    @asynccontextmanager
    async def setup(
        cls: Type[AsyncTgClientType],
        token: str,
        *,
        session: httpx.AsyncClient | None = None,
        tg_server_url: str = DEFAULT_TG_SERVER_URL,
    ) -> AsyncGenerator[AsyncTgClientType, None]:
        if not token:
            # Safety check for empty string or None to avoid confusing HTTP 404 error
            raise ValueError(f'Telegram token is empty: {token!r}')

        async with AsyncExitStack() as stack:
            if not session:
                session = await stack.enter_async_context(httpx.AsyncClient())

            client = cls(token=token, session=session, tg_server_url=tg_server_url)
            with client.set_as_default():
                yield client

    @contextmanager
    def set_as_default(self) -> Generator[None, None, None]:
        default_client_token: Token = self.default_client.set(self)
        try:
            yield
        finally:
            self.default_client.reset(default_client_token)


@dataclass(frozen=True)
class SyncTgClient:
    token: str
    _: KW_ONLY
    session: httpx.Client
    tg_server_url: str = DEFAULT_TG_SERVER_URL

    api_root: str = field(init=False)

    default_client: ClassVar[ContextVar['SyncTgClient']] = ContextVar('default_client')

    def __post_init__(self) -> None:
        api_root = urljoin(self.tg_server_url, f'./bot{self.token}/')
        object.__setattr__(self, 'api_root', api_root)

    @classmethod
    @contextmanager
    def setup(
        cls: Type[SyncTgClientType],
        token: str,
        *,
        session: httpx.Client = None,
        tg_server_url: str = DEFAULT_TG_SERVER_URL,
    ) -> Generator[SyncTgClientType, None, None]:
        if not token:
            # Safety check for empty string or None to avoid confusing HTTP 404 error
            raise ValueError(f'Telegram token is empty: {token!r}')

        if not session:
            session = httpx.Client()

        client = cls(token=token, session=session, tg_server_url=tg_server_url)
        with client.set_as_default():
            yield client

    @contextmanager
    def set_as_default(self) -> Generator[None, None, None]:
        default_client_token: Token = self.default_client.set(self)
        try:
            yield
        finally:
            self.default_client.reset(default_client_token)


def raise_for_tg_response_status(response: httpx.Response) -> None:
    """Raise the `TgHttpStatusError` if one occurred."""
    request = response._request

    if request is None:
        raise TgRuntimeError(
            "Cannot call `raise_for_status` as the request instance has not been set on this response.",
        )

    if response.is_success:
        return

    raise TgHttpStatusError(request=request, response=response)
