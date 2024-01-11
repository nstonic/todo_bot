from __future__ import annotations

from contextlib import suppress
from typing import TYPE_CHECKING
from pydantic import ValidationError

import httpx


if TYPE_CHECKING:
    from .tg_methods import BaseTgResponse


class TgHttpStatusError(httpx._exceptions.HTTPStatusError):
    # Common HTTPStatusError fields are filled by HTTPStatusError __init__ method:
    request: httpx.Request
    response: httpx.Response

    # Tg specific extra fields:
    tg_response: BaseTgResponse | None

    def __init__(
        self,
        *,
        request: httpx.Request,
        response: httpx.Response,
    ) -> None:
        from .tg_methods import BaseTgResponse

        tg_response = None
        with suppress(ValidationError):
            tg_response = BaseTgResponse.parse_raw(response.content)

        message_template_lines = [
            "{error_type} '{response.status_code} {response.reason_phrase}' for url '{response.url}'",
            'Redirect location: {response.headers[location]!r}' if response.has_redirect_location else None,
            'Details: error_code={tg.error_code!r} description={tg.description!r}' if tg_response else None,
            "For more information check: https://httpstatuses.com/{response.status_code}",
        ]
        message_template = '\n'.join(line for line in message_template_lines if line)

        status_class = response.status_code // 100
        error_types = {
            1: "Informational response",
            3: "Redirect response",
            4: "Client error",
            5: "Server error",
        }
        error_type = error_types.get(status_class, "Invalid status code")
        message = message_template.format(
            response=response,
            error_type=error_type,
            tg=tg_response,
        )

        super().__init__(message, request=request, response=response)
        self.tg_response = tg_response


class TgRuntimeError(RuntimeError):
    # TODO это исключение в номер не надо отлавливать -- оно сигнализирует о непредвиденном сбое в коде
    pass
