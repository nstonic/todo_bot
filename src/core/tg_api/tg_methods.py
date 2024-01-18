import asyncio
import io
import json
from collections.abc import AsyncGenerator, Generator
from itertools import chain, repeat
from textwrap import dedent
from time import sleep
from typing import Any, Union, NoReturn

import httpx
from pydantic import BaseModel, Field

from . import tg_types
from .client import (AsyncTgClient, SyncTgClient, TgRuntimeError,
                     raise_for_tg_response_status)


class BaseTgRequest(BaseModel, tg_types.ValidableMixin):
    """Base class representing a request to the Telegram Bot API.

    Provides utility methods for making both asynchronous and synchronous requests to the API.

    Typically used as a parent class for specific request types which include their data fields and
    possibly override or extend the base methods to customize behavior.
    """

    class Config:
        extra = 'forbid'
        validate_assignment = True
        anystr_strip_whitespace = True

    async def apost_as_json(self, api_method: str) -> bytes:
        """Send a request to the Telegram Bot API asynchronously using a JSON payload.

        :param api_method: The Telegram Bot API method to call.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = AsyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires AsyncTgClient to be specified before call.')

        http_response = await client.session.post(
            f'{client.api_root}{api_method}',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            content=self.json(exclude_none=True).encode('utf-8'),
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    def post_as_json(self, api_method: str) -> bytes:
        """Send a request to the Telegram Bot API synchronously using a JSON payload.

        :param api_method: The Telegram Bot API method to call.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = SyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires SyncTgClient to be specified before call.')

        http_response = client.session.post(
            f'{client.api_root}{api_method}',
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            content=self.json(exclude_none=True).encode('utf-8'),
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    async def apost_multipart_form_data(self, api_method: str, content: dict, files: dict) -> bytes:
        """Send a request to the Telegram Bot API asynchronously using the "multipart/form-data" format.

        :param api_method: The Telegram Bot API method to call.
        :param content: A dictionary containing the content to be sent.
        :param files: A dictionary containing files to be sent.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = AsyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires AsyncTgClient to be specified before call.')

        if content.get('caption_entities'):
            content['caption_entities'] = json.dumps(content['caption_entities'])

        if content.get('entities'):
            content['entities'] = json.dumps(content['entities'])

        if content.get('reply_markup'):
            content['reply_markup'] = json.dumps(content['reply_markup'])

        if content.get('media'):
            content['media'] = json.dumps(content['media'])

        http_response = await client.session.post(
            f'{client.api_root}{api_method}',
            files=files,
            data=content,
        )
        raise_for_tg_response_status(http_response)
        return http_response.content

    def post_multipart_form_data(self, api_method: str, content: dict, files: dict) -> bytes:
        """Send a request to the Telegram Bot API synchronously using the "multipart/form-data" format.

        :param api_method: The Telegram Bot API method name.
        :param content: A dictionary containing the content to be sent.
        :param files: A dictionary containing files to be sent.
        :return: The response from the Telegram Bot API as a byte string.
        """
        client = SyncTgClient.default_client.get(None)

        if not client:
            raise TgRuntimeError('Requires SyncTgClient to be specified before call.')

        if content.get('caption_entities'):
            content['caption_entities'] = json.dumps(content['caption_entities'])

        if content.get('entities'):
            content['entities'] = json.dumps(content['entities'])

        if content.get('reply_markup'):
            content['reply_markup'] = json.dumps(content['reply_markup'])

        if content.get('media'):
            content['media'] = json.dumps(content['media'])

        http_response = client.session.post(
            f'{client.api_root}{api_method}',
            files=files,
            data=content,
        )
        raise_for_tg_response_status(http_response)
        return http_response.content


class BaseTgResponse(BaseModel):
    """Represents the base structure of a response from the Telegram Bot API.

    Every response from the Telegram Bot API contains certain common attributes, which are captured
    in this base model. Specific response types might extend this base structure.
    """

    ok: bool = Field(
        description="A Boolean value indicating the success of the operation.",
    )
    error_code: int | None = Field(
        default=None,
        description=dedent("""\
            An integer or `None` value that contains the error code if the operation fails.
            If the operation was successful, the value will be `None`.
        """),
    )
    description: str = Field(
        default="",
        description=dedent("""\
            A string value that can contain additional description of the result of the operation or the cause of
            the error. If the operation was successful, the value will be empty.
        """),
    )
    result: Any = Field(
        default=None,
        description=dedent("""\
            Any value that represents the specific result of an operation. The value type may depend on
            the specific Telegram Bot API response type.
        """),
    )
    parameters: tg_types.ResponseParameters | None = Field(
        default=None,
        description="An optional field that represents additional parameters associated with the response.",
    )

    class Config:
        extra = 'ignore'
        allow_mutation = False


class SendMessageResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message = Field(
        description="Result of sending a message.",
    )


class SendMessageRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendMessage`.

    See here https://core.telegram.org/bots/api#sendmessage
    """

    text: str = Field(
        min_length=1,
        max_length=4096,
        description="Text of the message to be sent, 1-4096 characters after entities parsing.",
    )
    chat_id: int = Field(
        description=dedent("""\
            Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """),
    )
    parse_mode: tg_types.ParseMode | None = Field(
        default=None,
        description="Mode for parsing entities in the message text. See formatting options for more details.",
    )
    entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of special entities that appear in message text,
            which can be specified instead of parse_mode.
        """),
    )
    disable_web_page_preview: bool | None = Field(
        default=None,
        description="Disables link previews for links in this message.",
    )
    disable_notification: bool | None = Field(
        default=None,
        description="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content: bool | None = Field(
        default=None,
        description="Protects the contents of the sent message from forwarding and saving.",
    )
    message_thread_id: bool | None = Field(
        default=None,
        description=dedent("""\
            Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
        """),
    )
    allow_sending_without_reply: bool | None = Field(
        default=None,
        description="Pass True if the message should be sent even if the specified replied-to message is not found.",
    )
    reply_markup: Union[
                      tg_types.InlineKeyboardMarkup,
                      tg_types.ReplyKeyboardMarkup,
                      tg_types.ReplyKeyboardRemove,
                      tg_types.ForceReply,
                  ] | None = Field(
        default=None,
        description=dedent("""\
            Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.
        """),
    )

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super().__init__(text=args[0], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    class Config:
        anystr_strip_whitespace = True

    async def asend(self) -> SendMessageResponse:
        """Send HTTP request to `sendMessage` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('sendMessage')
        response = SendMessageResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendMessageResponse:
        """Send HTTP request to `sendMessage` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('sendMessage')
        response = SendMessageResponse.parse_raw(json_payload)
        return response


class SendPhotoResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message = Field(
        description="Result of sending a photo.",
    )


class SendBytesPhotoRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendPhoto`.

    See here https://core.telegram.org/bots/api#sendphoto
    """

    photo: bytes = Field(
        description=dedent("""\
            Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended),
            pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo using
            multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height must not exceed
            10000 in total. Width and height ratio must be at most 20.
        """),
    )
    chat_id: int = Field(
        description=dedent("""\
            Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """),
    )
    filename: str | None = Field(
        default=None,
        description="",
    )
    message_thread_id: int | None = Field(
        default=None,
        description=dedent("""\
            Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
        """),
    )
    caption: str | None = Field(
        default=None,
        max_length=1024,
        description=dedent("""\
            Photo caption (may also be used when resending photos by file_id),
            0-1024 characters after entities parsing.
        """),
    )
    parse_mode: str | None = Field(
        default=None,
        description="Mode for parsing entities in the photo caption. See formatting options for more details.",
    )
    caption_entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    has_spoiler: bool | None = Field(
        default=None,
        description="Pass True if the photo needs to be covered with a spoiler animation.",
    )
    disable_notification: bool | None = Field(
        default=None,
        description="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content: bool | None = Field(
        default=None,
        description="Protects the contents of the sent message from forwarding and saving.",
    )
    reply_to_message_id: int | None = Field(
        default=None,
        description="If the message is a reply, ID of the original message.",
    )
    allow_sending_without_reply: bool | None = Field(
        default=None,
        description="Pass True if the message should be sent even if the specified replied-to message is not found.",
    )
    reply_markup: Union[
                      tg_types.InlineKeyboardMarkup,
                      tg_types.ReplyKeyboardMarkup,
                      tg_types.ReplyKeyboardRemove,
                      tg_types.ForceReply,
                  ] | None = Field(
        default=None,
        description=dedent("""\
            Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.
        """),
    )

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super().__init__(photo=args[0], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    async def asend(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint asynchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'photo'})
        photo_bytes_io = io.BytesIO(self.photo)
        photo_bytes_io.name = self.filename
        files = {'photo': photo_bytes_io}
        json_payload = await self.apost_multipart_form_data('sendPhoto', content, files)
        response = SendPhotoResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint synchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'photo'})
        photo_bytes_io = io.BytesIO(self.photo)
        photo_bytes_io.name = self.filename
        files = {'photo': photo_bytes_io}
        json_payload = self.post_multipart_form_data('sendPhoto', content, files)
        response = SendPhotoResponse.parse_raw(json_payload)
        return response


class SendUrlPhotoRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendPhoto`.

    See here https://core.telegram.org/bots/api#sendphoto
    """

    photo: str = Field(
        description=dedent("""\
            Photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended),
            pass an HTTP URL as a String for Telegram to get a photo from the Internet, or upload a new photo
            using multipart/form-data. The photo must be at most 10 MB in size. The photo's width and height
            must not exceed 10000 in total. Width and height ratio must be at most 20.
        """),
    )
    chat_id: int = Field(
        description=dedent("""\
            Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """),
    )
    filename: str | None = Field(
        default=None,
        description="",
    )
    message_thread_id: int | None = Field(
        default=None,
        description=dedent("""\
            Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
        """),
    )
    caption: str | None = Field(
        default=None,
        max_length=1024,
        description=dedent("""\
            Photo caption (may also be used when resending photos by file_id),
            0-1024 characters after entities parsing.
        """),
    )
    parse_mode: str | None = Field(
        default=None,
        description="Mode for parsing entities in the photo caption. See formatting options for more details.",
    )
    caption_entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    has_spoiler: bool | None = Field(
        default=None,
        description="Pass True if the photo needs to be covered with a spoiler animation.",
    )
    disable_notification: bool | None = Field(
        default=None,
        description="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content: bool | None = Field(
        default=None,
        description="Protects the contents of the sent message from forwarding and saving.",
    )
    reply_to_message_id: int | None = Field(
        default=None,
        description="If the message is a reply, ID of the original message.",
    )
    allow_sending_without_reply: bool | None = Field(
        default=None,
        description="Pass True if the message should be sent even if the specified replied-to message is not found.",
    )
    reply_markup: Union[
                      tg_types.InlineKeyboardMarkup,
                      tg_types.ReplyKeyboardMarkup,
                      tg_types.ReplyKeyboardRemove,
                      tg_types.ForceReply,
                  ] | None = Field(
        default=None,
        description=dedent("""\
            Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.
        """),
    )

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super().__init__(photo=args[0], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    async def asend(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('sendPhoto')
        response = SendPhotoResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendPhotoResponse:
        """Send HTTP request to `sendPhoto` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('sendPhoto')
        response = SendPhotoResponse.parse_raw(json_payload)
        return response


class SendDocumentResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message = Field(
        description="Result of sending a document.",
    )


class SendBytesDocumentRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendDocument`.

    See here https://core.telegram.org/bots/api#senddocument
    """

    document: bytes = Field(
        description=dedent("""\
            File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended),
            pass an HTTP URL as a String for Telegram to get a file from the Internet,
            or upload a new one using multipart/form-data.
        """),
    )
    chat_id: int = Field(
        description=dedent("""\
            Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """),
    )
    filename: str | None = Field(
        default=None,
        description="",
    )
    message_thread_id: int | None = Field(
        default=None,
        description=dedent("""\
            Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
        """),
    )
    thumbnail: bytes | str | None = Field(
        default=None,
        description=dedent("""\
            Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side.
            The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should
            not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused
            and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the thumbnail was
            uploaded using multipart/form-data under <file_attach_name>.
        """),
    )
    caption: str | None = Field(
        default=None,
        max_length=1024,
        description=dedent("""\
            Document caption (may also be used when resending documents by file_id),
            0-1024 characters after entities parsing.
        """),
    )
    parse_mode: str | None = Field(
        default=None,
        description="Mode for parsing entities in the document caption. See formatting options for more details.",
    )
    caption_entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    disable_content_type_detection: bool | None = Field(
        default=None,
        description=dedent("""\
            Disables automatic server-side content type detection for files uploaded using multipart/form-data.
        """),
    )
    disable_notification: bool | None = Field(
        default=None,
        description="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content: bool | None = Field(
        default=None,
        description="Protects the contents of the sent message from forwarding and saving.",
    )
    reply_to_message_id: int | None = Field(
        default=None,
        description="If the message is a reply, ID of the original message.",
    )
    allow_sending_without_reply: bool | None = Field(
        default=None,
        description="Pass True if the message should be sent even if the specified replied-to message is not found.",
    )
    reply_markup: Union[
                      tg_types.InlineKeyboardMarkup,
                      tg_types.ReplyKeyboardMarkup,
                      tg_types.ReplyKeyboardRemove,
                      tg_types.ForceReply,
                  ] | None = Field(
        default=None,
        description=dedent("""\
            Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.
        """),
    )

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super().__init__(document=args[0], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    async def asend(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint asynchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'document'})
        document_bytes = io.BytesIO(self.document)
        document_bytes.name = self.filename
        files = {'document': document_bytes}
        json_payload = await self.apost_multipart_form_data('sendDocument', content, files)
        response = SendDocumentResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint synchronously and parse response."""
        content = self.dict(exclude_none=True, exclude={'document'})
        document_bytes = io.BytesIO(self.document)
        document_bytes.name = self.filename
        files = {'document': document_bytes}
        json_payload = self.post_multipart_form_data('sendDocument', content, files)
        response = SendDocumentResponse.parse_raw(json_payload)
        return response


class SendUrlDocumentRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `sendDocument`.

    See here https://core.telegram.org/bots/api#senddocument
    """

    document: str = Field(
        description=dedent("""\
            File to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended),
            pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload
            a new one using multipart/form-data.
        """),
    )
    chat_id: int = Field(
        description=dedent("""\
            Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """),
    )
    filename: str | None = Field(
        default=None,
        description="",
    )
    message_thread_id: int | None = Field(
        default=None,
        description=dedent("""\
            Unique identifier for the target message thread (topic) of the forum; for forum supergroups only.
        """),
    )
    thumbnail: bytes | str | None = Field(
        default=None,
        description=dedent("""\
            Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side.
            The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height
            should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't
            be reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>” if the
            thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        """),
    )
    caption: str | None = Field(
        default=None,
        max_length=1024,
        description=dedent("""\
            Document caption (may also be used when resending documents by file_id),
            0-1024 characters after entities parsing.
        """),
    )
    parse_mode: str | None = Field(
        default=None,
        description="Mode for parsing entities in the document caption. See formatting options for more details.",
    )
    caption_entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    disable_content_type_detection: bool | None = Field(
        default=None,
        description=dedent("""\
            Disables automatic server-side content type detection for files uploaded using multipart/form-data.
        """),
    )
    disable_notification: bool | None = Field(
        default=None,
        description="Sends the message silently. Users will receive a notification with no sound.",
    )
    protect_content: bool | None = Field(
        default=None,
        description="Protects the contents of the sent message from forwarding and saving.",
    )
    reply_to_message_id: int | None = Field(
        default=None,
        description="If the message is a reply, ID of the original message.",
    )
    allow_sending_without_reply: bool | None = Field(
        default=None,
        description="Pass True if the message should be sent even if the specified replied-to message is not found.",
    )
    reply_markup: Union[
                      tg_types.InlineKeyboardMarkup,
                      tg_types.ReplyKeyboardMarkup,
                      tg_types.ReplyKeyboardRemove,
                      tg_types.ForceReply,
                  ] | None = Field(
        default=None,
        description=dedent("""\
            Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard,
            instructions to remove reply keyboard or to force a reply from the user.
        """),
    )

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            super().__init__(document=args[0], **kwargs)
        else:
            super().__init__(*args, **kwargs)

    async def asend(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('sendDocument')
        response = SendDocumentResponse.parse_raw(json_payload)
        return response

    def send(self) -> SendDocumentResponse:
        """Send HTTP request to `sendDocument` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('sendDocument')
        response = SendDocumentResponse.parse_raw(json_payload)
        return response


class DeleteMessageResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: bool = Field(
        description="Message deletion result.",
    )


class DeleteMessageRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `deleteMessage`.

    See here https://core.telegram.org/bots/api#deletemessage
    """

    chat_id: int = Field(
        description=dedent("""\
            Unique identifier for the target chat or username of the target channel (in the format @channelusername).
        """),
    )
    message_id: int = Field(
        description="Identifier of the message to delete.",
    )

    async def asend(self) -> DeleteMessageResponse:
        """Send HTTP request to `deleteMessage` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('deleteMessage')
        response = DeleteMessageResponse.parse_raw(json_payload)
        return response

    def send(self) -> DeleteMessageResponse:
        """Send HTTP request to `deleteMessage` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('deleteMessage')
        response = DeleteMessageResponse.parse_raw(json_payload)
        return response


class EditMessageTextResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message | bool = Field(
        description="Message editing result.",
    )


class EditMessageTextRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editMessageText`.

    See here https://core.telegram.org/bots/api#editmessagetext
    """

    chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Required if inline_message_id is not specified. Unique identifier for the target chat or
            username of the target channel (in the format @channelusername).
        """),
    )
    message_id: int | None = Field(
        default=None,
        description="Required if inline_message_id is not specified. Identifier of the message to edit.",
    )
    inline_message_id: str | None = Field(
        default=None,
        description="Required if chat_id and message_id are not specified. Identifier of the inline message.",
    )
    text: str = Field(
        min_length=1,
        max_length=4096,
        description="New text of the message, 1-4096 characters after entities parsing.",
    )
    parse_mode: str | None = Field(
        default=None,
        description="Mode for parsing entities in the message text. See formatting options for more details.",
    )
    entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""
            A JSON-serialized list of special entities that appear in message text,
            which can be specified instead of parse_mode.
        """),
    )
    disable_web_page_preview: bool | None = Field(
        default=None,
        description="Disables link previews for links in this message.",
    )
    reply_markup: tg_types.InlineKeyboardMarkup | None = Field(
        default=None,
        description="A JSON-serialized object for an inline keyboard.",
    )

    async def asend(self) -> EditMessageTextResponse:
        """Send HTTP request to `editmessagetext` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagetext')
        response = EditMessageTextResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageTextResponse:
        """Send HTTP request to `editmessagetext` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagetext')
        response = EditMessageTextResponse.parse_raw(json_payload)
        return response


class EditMessageReplyMarkupResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message | bool = Field(
        description="The result of editing a ReplyMarkup message.",
    )


class EditMessageReplyMarkupRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editMessageReplyMarkup`.

    See here https://core.telegram.org/bots/api#editmessagereplymarkup
    """

    chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Required if inline_message_id is not specified. Unique identifier for the target chat or username
            of the target channel (in the format @channelusername).
        """),
    )
    message_id: int | None = Field(
        default=None,
        description="Required if inline_message_id is not specified. Identifier of the message to edit.",
    )
    inline_message_id: str | None = Field(
        default=None,
        description="Required if chat_id and message_id are not specified. Identifier of the inline message.",
    )
    reply_markup: tg_types.InlineKeyboardMarkup | None = Field(
        default=None,
        description="A JSON-serialized object for an inline keyboard.",
    )

    async def asend(self) -> EditMessageReplyMarkupResponse:
        """Send HTTP request to `editmessagereplymarkup` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagereplymarkup')
        response = EditMessageReplyMarkupResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageReplyMarkupResponse:
        """Send HTTP request to `editmessagereplymarkup` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagereplymarkup')
        response = EditMessageReplyMarkupResponse.parse_raw(json_payload)
        return response


class EditMessageCaptionResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message | bool = Field(
        description="The result of editing a caption.",
    )


class EditMessageCaptionRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editMessageCaption`.

    See here https://core.telegram.org/bots/api#editmessagecaption
    """

    chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Required if inline_message_id is not specified. Unique identifier for the target chat or username
            of the target channel (in the format @channelusername).
        """),
    )
    message_id: int | None = Field(
        default=None,
        description="Required if inline_message_id is not specified. Identifier of the message to edit.",
    )
    inline_message_id: str | None = Field(
        default=None,
        description="Required if chat_id and message_id are not specified. Identifier of the inline message.",
    )
    caption: str | None = Field(
        default=None,
        max_length=1024,
        description="New caption of the message, 0-1024 characters after entities parsing.",
    )
    parse_mode: str | None = Field(
        default=None,
        description="Mode for parsing entities in the message caption. See formatting options for more details.",
    )
    caption_entities: list[tg_types.MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    reply_markup: tg_types.InlineKeyboardMarkup | None = Field(
        default=None,
        description="A JSON-serialized object for an inline keyboard.",
    )

    async def asend(self) -> EditMessageCaptionResponse:
        """Send HTTP request to `editmessagecaption` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagecaption')
        response = EditMessageCaptionResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageCaptionResponse:
        """Send HTTP request to `editmessagecaption` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagecaption')
        response = EditMessageCaptionResponse.parse_raw(json_payload)
        return response


class EditMessageMediaResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.Message | bool = Field(
        description="The result of editing a media message.",
    )


class EditBytesMessageMediaRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editmessagemedia`.

    See here https://core.telegram.org/bots/api#editmessagemedia
    """

    chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Required if inline_message_id is not specified. Unique identifier for the target chat or username
            of the target channel (in the format @channelusername).
        """),
    )
    message_id: int | None = Field(
        default=None,
        description="Required if inline_message_id is not specified. Identifier of the message to edit.",
    )
    inline_message_id: str | None = Field(
        default=None,
        description="Required if chat_id and message_id are not specified. Identifier of the inline message.",
    )
    media: Union[tg_types.InputMediaBytesDocument, tg_types.InputMediaBytesPhoto] = Field(
        description="A JSON-serialized object for a new media content of the message.",
    )
    reply_markup: tg_types.InlineKeyboardMarkup | None = Field(
        default=None,
        description="A JSON-serialized object for a new inline keyboard.",
    )

    async def asend(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint asynchronously and parse response."""
        content = self.dict(exclude_none=True)

        content['media'].pop('media_content')
        media_bytes = io.BytesIO(self.media.media_content)
        files = {self.media.media: media_bytes}

        if not self.media.media.startswith('attach://'):
            content['media']['media'] = f"attach://{content['media']['media']}"

        if content['media'].get('thumbnail') and content['media'].get('thumbnail_content'):
            thumbnail = content['media']['thumbnail']
            thumbnail_content = content['media'].pop('thumbnail_content')
            thumbnail_bytes = io.BytesIO(thumbnail_content)
            files[thumbnail] = thumbnail_bytes

            if not thumbnail.startswith('attach://'):
                content['media']['thumbnail'] = f"attach://{thumbnail}"

        json_payload = await self.apost_multipart_form_data('editmessagemedia', content, files)
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint synchronously and parse response."""
        content = self.dict(exclude_none=True)

        content['media'].pop('media_content')
        media_bytes = io.BytesIO(self.media.media_content)
        files = {self.media.media: media_bytes}

        if not self.media.media.startswith('attach://'):
            content['media']['media'] = f"attach://{content['media']['media']}"

        if content['media'].get('thumbnail') and content['media'].get('thumbnail_content'):
            thumbnail = content['media']['thumbnail']
            thumbnail_content = content['media'].pop('thumbnail_content')
            thumbnail_bytes = io.BytesIO(thumbnail_content)
            files[thumbnail] = thumbnail_bytes

            if not thumbnail.startswith('attach://'):
                content['media']['thumbnail'] = f"attach://{thumbnail}"

        json_payload = self.post_multipart_form_data('editmessagemedia', content, files)
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response


class EditUrlMessageMediaRequest(BaseTgRequest):
    """Object encapsulates data for calling Telegram Bot API endpoint `editmessagemedia`.

    See here https://core.telegram.org/bots/api#editmessagemedia
    """

    chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Required if inline_message_id is not specified. Unique identifier for the target chat or
            username of the target channel (in the format @channelusername).
        """),
    )
    message_id: int | None = Field(
        default=None,
        description="Required if inline_message_id is not specified. Identifier of the message to edit.",
    )
    inline_message_id: str | None = Field(
        default=None,
        description="Required if chat_id and message_id are not specified. Identifier of the inline message.",
    )
    media: Union[tg_types.InputMediaUrlDocument, tg_types.InputMediaUrlPhoto] = Field(
        description="A JSON-serialized object for a new media content of the message.",
    )
    reply_markup: tg_types.InlineKeyboardMarkup | None = Field(
        default=None,
        description="A JSON-serialized object for a new inline keyboard.",
    )

    async def asend(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint asynchronously and parse response."""
        json_payload = await self.apost_as_json('editmessagemedia')
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response

    def send(self) -> EditMessageMediaResponse:
        """Send HTTP request to `editmessagemedia` Telegram Bot API endpoint synchronously and parse response."""
        json_payload = self.post_as_json('editmessagemedia')
        response = EditMessageMediaResponse.parse_raw(json_payload)
        return response


class WebhookInfoResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: tg_types.WebhookInfo = Field(
        description="Webhook info.",
    )


class WebhookInfoRequest(BaseTgRequest):
    """Get current webhook status.

    See https://core.telegram.org/bots/api#getwebhookinfo
    """

    async def asend(self) -> WebhookInfoResponse:
        """Get the webhook info (async)."""
        response = await self.apost_as_json('getWebhookInfo')
        return WebhookInfoResponse.parse_raw(response)

    def send(self) -> WebhookInfoResponse:
        """Get the webhook info (sync)."""
        response = self.post_as_json('getWebhookInfo')
        return WebhookInfoResponse.parse_raw(response)


class SetWebhookResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: bool = Field(
        description="Set webhook result.",
    )


class SetWebhookRequest(BaseTgRequest):
    """Specify a URL for receiving updates via an outgoing webhook.

    See https://core.telegram.org/bots/api#setwebhook
    """

    url: str = Field(
        description=dedent("""\
            HTTPS URL to send updates to.
            Use an empty string to remove webhook integration
        """),
    )
    certificate: bytes | None = Field(
        default=None,
        description=dedent("""\
            Upload your public key certificate so that the root certificate
            in use can be checked. See the self-signed guide for details:
            https://core.telegram.org/bots/self-signed
        """),
    )
    ip_address: str | None = Field(
        default=None,
        description=dedent("""\
            The fixed IP address which will be used to send webhook requests
            instead of the IP address resolved through DNS
        """),
    )

    max_connections: int | None = Field(
        default=None,
        description=dedent("""\
            The maximum allowed number of simultaneous HTTPS connections
            to the webhook for update delivery, 1-100. Defaults to 40.
            Use lower values to limit the load on your bot's server,
            and higher values to increase your bot's throughput.
        """),
    )

    allowed_updates: list[str] | None = Field(
        default=None,
        description=dedent("""\
            A JSON-serialized list of the update types you want your bot
            to receive. For example, specify
            ["message", "edited_channel_post", "callback_query"]
            to only receive updates of these types.
        """),
    )
    drop_pending_updates: bool | None = Field(
        default=None,
        description="Pass True to drop all pending updates",
    )
    secret_token: str | None = Field(
        default=None,
        description=dedent("""\
            A secret token to be sent in a header
            “X-Telegram-Bot-Api-Secret-Token” in every webhook request,
            1-256 characters.
            Only characters A-Z, a-z, 0-9, _ and - are allowed. The header is
            useful to ensure that the request comes from a webhook set by you.
        """),
    )

    async def asend(self) -> SetWebhookResponse:
        """Set a webhook (async)."""
        response = await self.apost_as_json('setWebhook')
        return SetWebhookResponse.parse_raw(response)

    def send(self) -> SetWebhookResponse:
        """Set the webhook (sync)."""
        response = self.post_as_json('setWebhook')
        return SetWebhookResponse.parse_raw(response)


class DeleteWebhookResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: bool = Field(
        description="Delete webhook result.",
    )


class DeleteWebhookRequest(BaseTgRequest):
    """Remove webhook integration.

    See https://core.telegram.org/bots/api#deletewebhook
    """

    drop_pending_updates: bool | None = Field(
        default=None,
        description="Pass True to drop all pending updates",
    )

    async def asend(self) -> DeleteWebhookResponse:
        """Delete a webhook (async)."""
        response = await self.apost_as_json('deleteWebhook')
        return DeleteWebhookResponse.parse_raw(response)

    def send(self) -> DeleteWebhookResponse:
        """Delete a webhook (sync)."""
        response = self.post_as_json('deleteWebhook')
        return DeleteWebhookResponse.parse_raw(response)


class GetUpdatesResponse(BaseTgResponse):
    """Represents an extended response structure from the Telegram Bot API."""

    result: list[tg_types.Update] = Field(
        description="Get updates result.",
    )


class GetUpdatesRequest(BaseTgRequest):
    """Get updates.

    Object encapsulates data for calling Telegram Bot API endpoint
    `getUpdates`.

    See here https://core.telegram.org/bots/api#getupdates
    """

    offset: int | None = Field(
        default=1,
        description="Identifier of the first update to be returned.",
    )
    limit: int | None = Field(
        default=100,
        description="Limits the number of updates to be retrieved.",
    )
    timeout: int | None = Field(
        default=30,
        description="Timeout in seconds for long polling.",
    )
    allowed_updates: list[str] | None = Field(
        default=None,
        description=dedent("""\
            Specify a list of the update types to be received.
            Specify an empty list to receive all update types except
            chat_member (default).
            If not specified, the previous setting will be used.
        """),
    )

    async def asend(self) -> AsyncGenerator[tg_types.Update, None]:
        """Get Telegram updates (async)."""
        response = await self.apost_as_json('getUpdates')
        get_updates_response = GetUpdatesResponse.parse_raw(response)
        for update in get_updates_response.result:
            yield update

    def send(self) -> Generator[tg_types.Update, None, None]:
        """Get Telegram updates (sync)."""
        response = self.post_as_json('getUpdates')
        yield from GetUpdatesResponse.parse_raw(response).result

    async def alisten_updates(self) -> Generator[tg_types.Update, None, NoReturn]:
        max_pause = 10
        pauses = chain(
            [0, 1, 3],
            repeat(max_pause),
        )

        while True:
            try:
                updates = self.asend()
                async for update in updates:
                    yield update
                    self.offset = update.update_id + 1
            except httpx.ReadTimeout:
                continue
            except (httpx.ConnectError, httpx.RemoteProtocolError, httpx.ConnectTimeout):
                pause = next(pauses)
                await asyncio.sleep(pause)

            pauses = chain(
                [0, 1, 3],
                repeat(max_pause),
            )

    def listen_updates(self) -> Generator[tg_types.Update, None, NoReturn]:
        max_pause = 10
        pauses = chain(
            [0, 1, 3],
            repeat(max_pause),
        )
        while True:
            try:
                updates = self.send()
                for update in updates:
                    yield update
                    self.offset = update.update_id + 1
            except httpx.ReadTimeout:
                continue
            except (httpx.ConnectError, httpx.RemoteProtocolError, httpx.ConnectTimeout):
                pause = next(pauses)
                sleep(pause)

            pauses = chain(
                [0, 1, 3],
                repeat(max_pause),
            )
