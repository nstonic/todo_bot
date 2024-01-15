from __future__ import annotations

from textwrap import dedent
from enum import Enum
from typing import Any, Union, Optional

from pydantic import BaseModel, AnyHttpUrl, Field, root_validator


class ParseMode(str, Enum):
    MarkdownV2 = 'MarkdownV2'  # https://core.telegram.org/bots/api#markdownv2-style
    HTML = 'HTML'  # https://core.telegram.org/bots/api#html-style
    Markdown = 'Markdown'  # legacy mode https://core.telegram.org/bots/api#markdown-style


class ValidableMixin:
    """This mixin sets validation for all fields."""

    class Config:
        validate_all = True


class User(BaseModel, ValidableMixin):
    """This model represents a Telegram user or bot.

    See here: https://core.telegram.org/bots/api#user
    """

    id: int = Field(  # noqa A003
        description=dedent("""\
            Unique identifier for this user or bot. This number may have more than 32 significant bits and
            some programming languages may have difficulty/silent defects in interpreting it.
            But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are
            safe for storing this identifier.
        """),
    )
    is_bot: bool = Field(
        description="True, if this user is a bot.",
    )
    first_name: str = Field(
        description="User's or bot's first name.",
    )
    last_name: str | None = Field(
        default=None,
        description="Optional. User's or bot's last name.",
    )
    username: str | None = Field(
        default=None,
        description="Optional. User's or bot's username.",
    )
    language_code: str | None = Field(
        default=None,
        description="Optional. IETF language tag of the user's language.",
    )
    is_premium: bool | None = Field(
        default=None,
        description="Optional. True, if this user is a Telegram Premium user.",
    )
    added_to_attachment_menu: bool | None = Field(
        default=None,
        description="Optional. True, if this user added the bot to the attachment menu.",
    )
    can_join_groups: bool | None = Field(
        default=None,
        description="Optional. True, if the bot can be invited to groups. Returned only in getMe.",
    )
    can_read_all_group_messages: bool | None = Field(
        default=None,
        description="Optional. True, if privacy mode is disabled for the bot. Returned only in getMe.",
    )
    supports_inline_queries: bool | None = Field(
        default=None,
        description="Optional. True, if the bot supports inline queries. Returned only in getMe.",
    )


class Chat(BaseModel, ValidableMixin):
    """This model represents a chat.

    See here: https://core.telegram.org/bots/api#chat
    """

    id: int = Field(  # noqa A003
        description=dedent("""\
            Unique identifier for this chat. This number may have more than 32 significant bits and some programming
            languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits,
            so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        """),
    )
    type: str = Field(  # noqa A003
        description="Type of chat, can be either “private”, “group”, “supergroup” or “channel”.",
    )
    title: str | None = Field(
        default=None,
        description="Optional. Title, for supergroups, channels and group chats.",
    )
    username: str | None = Field(
        default=None,
        description="Optional. Username, for private chats, supergroups and channels if available.",
    )
    first_name: str | None = Field(
        default=None,
        description="Optional. First name of the other party in a private chat.",
    )
    last_name: str | None = Field(
        default=None,
        description="Optional. Last name of the other party in a private chat.",
    )
    is_forum: bool | None = Field(
        default=None,
        description="Optional. True, if the supergroup chat is a forum (has topics enabled).",
    )
    photo: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Chat photo. Returned only in getChat.",
    )
    active_usernames: list[str] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If non-empty, the list of all active chat usernames;
            for private chats, supergroups and channels. Returned only in getChat.
        """),
    )
    emoji_status_custom_emoji_id: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Custom emoji identifier of emoji status of the other party in a private chat.
            Returned only in getChat.
        """),
    )
    bio: str | None = Field(
        default=None,
        description="Optional. Bio of the other party in a private chat. Returned only in getChat.",
    )
    has_private_forwards: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if privacy settings of the other party in the private chat allows
            to use tg://user?id=<user_id> links only in chats with the user. Returned only in getChat.
        """),
    )
    has_restricted_voice_and_video_messages: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if the privacy settings of the other party restrict sending
            voice and video note messages in the private chat. Returned only in getChat.
        """),
    )
    join_to_send_messages: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if users need to join the supergroup before they can send messages.
            Returned only in getChat.
        """),
    )
    join_by_request: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if all users directly joining the supergroup need
            to be approved by supergroup administrators. Returned only in getChat.
        """),
    )
    description: str | None = Field(
        default=None,
        description="Optional. Description, for groups, supergroups and channel chats. Returned only in getChat.",
    )
    invite_link: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Primary invite link, for groups, supergroups and channel chats. Returned only in getChat.
        """),
    )
    pinned_message: Message | None = Field(
        default=None,
        description="Optional. The most recent pinned message (by sending date). Returned only in getChat.",
    )
    permissions: dict[str, Any] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Default chat member permissions, for groups and supergroups. Returned only in getChat.
        """),
    )
    slow_mode_delay: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. For supergroups, the minimum allowed delay between consecutive messages sent
            by each unpriviledged user; in seconds. Returned only in getChat.
        """),
    )
    message_auto_delete_time: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The time after which all messages sent to the chat will be automatically deleted; in seconds.
            Returned only in getChat.
        """),
    )
    has_aggressive_anti_spam_enabled: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if aggressive anti-spam checks are enabled in the supergroup.
            The field is only available to chat administrators. Returned only in getChat.
        """),
    )
    has_hidden_members: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if non-administrators can only get the list of bots and administrators in the chat.
            Returned only in getChat.
        """),
    )
    has_protected_content: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if messages from the chat can't be forwarded to other chats. Returned only in getChat.
        """),
    )
    sticker_set_name: str | None = Field(
        default=None,
        description="Optional. For supergroups, name of group sticker set. Returned only in getChat.",
    )
    can_set_sticker_set: bool | None = Field(
        default=None,
        description="Optional. True, if the bot can change the group sticker set. Returned only in getChat.",
    )
    linked_chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. Unique identifier for the linked chat, i.e. the discussion group identifier for
            a channel and vice versa;for supergroups and channel chats. This identifier may be greater
            than 32 bits and some programming languages may have difficulty/silent defects in interpreting it.
            But it is smaller than 52 bits, so a signed 64 bit integer or double-precision float type are safe
            for storing this identifier. Returned only in getChat.
        """),
    )


class KeyboardButton(BaseModel, ValidableMixin):
    """This model represents one button of the reply keyboard.

    For simple text buttons, String can be used instead of this object to specify the button text.
    The optional fields web_app, request_user, request_chat, request_contact,
    request_location, and request_poll are mutually exclusive.

    See here: https://core.telegram.org/bots/api#keyboardbutton
    """

    text: str = Field(
        description=dedent("""\
            Text of the button. If none of the optional fields are used, it will be sent
            as a message when the button is pressed.
        """),
    )
    request_user: dict[str, Union[int, bool]] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, pressing the button will open a list of suitable users.
            Tapping on any user will send their identifier to the bot in a “user_shared” service message.
            Available in private chats only.
        """),
    )
    request_chat: dict[str, Union[int, bool, dict[str, bool]]] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, pressing the button will open a list of suitable chats.
            Tapping on a chat will send its identifier to the bot in a “chat_shared” service message.
            Available in private chats only.
        """),
    )
    request_contact: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.
        """),
    )
    request_location: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.
        """),
    )
    request_poll: dict[str, str] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, the user will be asked to create a poll and send it to the bot when
            the button is pressed. Available in private chats only.
        """),
    )
    web_app: dict[str, AnyHttpUrl] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If specified, the described Web App will be launched when the button is pressed.
            The Web App will be able to send a “web_app_data” service message. Available in private chats only.
        """),
    )


class ReplyKeyboardMarkup(BaseModel, ValidableMixin):
    """This model represents a custom keyboard with reply options.

    See here: https://core.telegram.org/bots/api#replykeyboardmarkup
    """

    keyboard: list[list[KeyboardButton]] = Field(
        description="Array of button rows, each represented by an Array of KeyboardButton objects",
    )
    is_persistent: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Requests clients to always show the keyboard when the regular keyboard is hidden.
            Defaults to false, in which case the custom keyboard can be hidden and opened with a keyboard icon.
        """),
    )
    resize_keyboard: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Requests clients to resize the keyboard vertically for optimal
            fit (e.g., make the keyboard smaller if there are just two rows of buttons).
            Defaults to false, in which case the custom keyboard is always
            of the same height as the app's standard keyboard.
        """),
    )
    one_time_keyboard: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Requests clients to hide the keyboard as soon as it's been used.
            The keyboard will still be available, but clients will automatically display
            the usual letter-keyboard in the chat - the user can press a special button
            in the input field to see the custom keyboard again. Defaults to false.
        """),
    )
    input_field_placeholder: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. The placeholder to be shown in the input field when the keyboard is active; 1-64 characters.
        """),
    )
    selective: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Use this parameter if you want to show the keyboard to specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example:
            A user requests to change the bot's language, bot replies to the request with a keyboard to
            select the new language. Other users in the group don't see the keyboard.
        """),
    )


class ReplyKeyboardRemove(BaseModel, ValidableMixin):
    """Upon receiving a message with this object, Telegram clients will remove the current.

    custom keyboard and display the default letter-keyboard. By default, custom keyboards
    are displayed until a new keyboard is sent by a bot. An exception is made for one-time
    keyboards that are hidden immediately after the user presses a button

    See here: https://core.telegram.org/bots/api#replykeyboardremove
    """

    remove_keyboard: bool = Field(
        description=dedent("""\
            Requests clients to remove the custom keyboard (user will not be able to summon this keyboard;
            if you want to hide the keyboard from sight but keep it accessible,
            use one_time_keyboard in ReplyKeyboardMarkup).
        """),
    )
    selective: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Use this parameter if you want to remove the keyboard for specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example:
            A user votes in a poll, bot returns confirmation message in reply to the vote and removes
            the keyboard for that user, while still showing the keyboard with poll
            options to users who haven't voted yet.
        """),
    )


class ForceReply(BaseModel, ValidableMixin):
    """Upon receiving a message with this object, Telegram clients will display a reply.

    interface to the user (act as if the user has selected the bot's message and tapped 'Reply').
    This can be extremely useful if you want to create user-friendly step-by-step interfaces
    without having to sacrifice privacy mode.

    See here: https://core.telegram.org/bots/api#forcereply
    """

    force_reply: bool = Field(
        description=dedent("""\
            Shows reply interface to the user, as if they manually selected the bot's message and tapped 'Reply'.
        """),
    )
    input_field_placeholder: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. The placeholder to be shown in the input field when the reply is active; 1-64 characters.
        """),
    )
    selective: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Use this parameter if you want to force reply from specific users only.
            Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
        """),
    )


class InlineKeyboardButton(BaseModel, ValidableMixin):
    """This model represents one button of an inline keyboard.

    See here: https://core.telegram.org/bots/api#inlinekeyboardbutton
    """

    text: str = Field(
        description="Label text on the button",
    )
    url: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. HTTP or tg:// URL to be opened when the button is pressed.
            Links tg://user?id=<user_id> can be used to mention a user by their ID without using a username,
            if this is allowed by their privacy settings.
        """),
    )
    callback_data: str | None = Field(
        default=None,
        description="Optional. Data to be sent in a callback query to the bot when button is pressed, 1-64 bytes",
    )
    web_app: dict[str, AnyHttpUrl] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Description of the Web App that will be launched when the user presses the button.
            The Web App will be able to send an arbitrary message on behalf of the user using the method
            answerWebAppQuery. Available only in private chats between a user and the bot.
        """),
    )
    login_url: dict[str, Union[str, bool]] | None = Field(
        default=None,
        description=dedent("""\
            Optional. An HTTPS URL used to automatically authorize the user.
            Can be used as a replacement for the Telegram Login Widget.
        """),
    )
    switch_inline_query: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. If set, pressing the button will prompt the user to select one of their chats,
            open that chat and insert the bot's username and the specified inline query in the input field.
            May be empty, in which case just the bot's username will be inserted.
        """),
    )
    switch_inline_query_current_chat: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. If set, pressing the button will insert the bot's username and the specified inline query
            in the current chat's input field. May be empty, in which case only the bot's username will be inserted.
            This offers a quick way for the user to open your bot in inline mode
            in the same chat - good for selecting something from multiple options.
        """),
    )
    switch_inline_query_chosen_chat: dict[str, Union[str, bool]] | None = Field(
        default=None,
        description=dedent("""\
            Optional. If set, pressing the button will prompt the user to select one of their chats of
            the specified type, open that chat and insert the bot's username and the specified
            inline query in the input field.
        """),
    )
    callback_game: Any | None = Field(
        default=None,
        description=dedent("""\
            Optional. Description of the game that will be launched when the user presses the button.
            NOTE: This type of button must always be the first button in the first row.
        """),
    )
    pay: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Specify True, to send a Pay button.
            NOTE: This type of button must always be the first
            button in the first row and can only be used in invoice messages.
        """),
    )


class InlineKeyboardMarkup(BaseModel, ValidableMixin):
    """This model represents an inline keyboard that appears right next to the message it belongs to.

    See here: https://core.telegram.org/bots/api#inlinekeyboardmarkup
    """

    inline_keyboard: list[list[InlineKeyboardButton]] = Field(
        description="Array of button rows, each represented by an Array of InlineKeyboardButton objects.",
    )


class Invoice(BaseModel, ValidableMixin):
    """This model contains basic information about an invoice.

    See here: https://core.telegram.org/bots/api#invoice
    """

    title: str = Field(
        description="Product name.",
    )
    description: str = Field(
        description="Product description",
    )
    start_parameter: str = Field(
        description="Unique bot deep-linking parameter that can be used to generate this invoice.",
    )
    currency: str = Field(
        description="Three-letter ISO 4217 currency code.",
    )
    total_amount: int = Field(
        description=dedent("""\
            Total price in the smallest units of the currency (integer, not float/double).
            For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json,
            it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        """),
    )


class ShippingAddress(BaseModel, ValidableMixin):
    """This object represents a shipping address.

    See here: https://core.telegram.org/bots/api#shippingaddress
    """

    country_code: str = Field(
        description="Two-letter ISO 3166-1 alpha-2 country code.",
    )
    state: str = Field(
        description="State, if applicable.",
    )
    city: str = Field(
        description="City.",
    )
    street_line1: str = Field(
        description="First line for the address.",
    )
    street_line2: str = Field(
        description="Second line for the address.",
    )
    post_code: str = Field(
        description="Address post code.",
    )


class OrderInfo(BaseModel, ValidableMixin):
    """This object represents information about an order.

    See here: https://core.telegram.org/bots/api#orderinfo
    """

    name: str | None = Field(
        default=None,
        description="Optional. User name.",
    )
    phone_number: str | None = Field(
        default=None,
        description="Optional. User's phone number.",
    )
    email: str | None = Field(
        default=None,
        description="Optional. User email.",
    )
    shipping_address: ShippingAddress | None = Field(
        default=None,
        description="Optional. User shipping address.",
    )


class SuccessfulPayment(BaseModel, ValidableMixin):
    """This object contains basic information about a successful payment.

    See here: https://core.telegram.org/bots/api#successfulpayment
    """

    currency: str = Field(
        description="Three-letter ISO 4217 currency code.",
    )
    total_amount: int = Field(
        description=dedent("""\
            Total price in the smallest units of the currency (integer, not float/double).
            For example, for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json,
            it shows the number of digits past the decimal point for each currency (2 for the majority of currencies).
        """),
    )
    invoice_payload: str = Field(
        description="Bot specified invoice payload.",
    )
    shipping_option_id: str | None = Field(
        default=None,
        description="Optional. Identifier of the shipping option chosen by the user.",
    )
    order_info: OrderInfo | None = Field(
        default=None,
        description="Optional. Order information provided by the user.",
    )
    telegram_payment_charge_id: str | None = Field(
        default=None,
        description="Telegram payment identifier.",
    )
    provider_payment_charge_id: str | None = Field(
        default=None,
        description="Provider payment identifier.",
    )


class MessageEntity(BaseModel, ValidableMixin):
    """This model represents one special entity in a text message.

    For example, hashtags, usernames, URLs, etc.

    See here: https://core.telegram.org/bots/api#messageentity
    """

    type: str = Field(  # noqa A003
        description=dedent("""\
            Type of the entity. Currently, can be “mention” (@username), “hashtag” (#hashtag),
            “cashtag” ($USD), “bot_command” (/start@jobs_bot), “url” (https://telegram.org),
            “email” (do-not-reply@telegram.org), “phone_number” (+1-212-555-0123), “bold” (bold text),
            “italic” (italic text), “underline” (underlined text), “strikethrough” (strikethrough text),
            “spoiler” (spoiler message), “code” (monowidth string), “pre” (monowidth block),
            “text_link” (for clickable text URLs), “text_mention” (for users without usernames),
            “custom_emoji” (for inline custom emoji stickers).
        """),
    )
    offset: int = Field(
        description="Offset in UTF-16 code units to the start of the entity.",
    )
    length: int = Field(
        description="Length of the entity in UTF-16 code units.",
    )
    url: str | None = Field(
        default=None,
        description="Optional. For “text_link” only, URL that will be opened after user taps on the text.",
    )
    user: User | None = Field(
        default=None,
        description="Optional. For “text_mention” only, the mentioned user.",
    )
    language: str | None = Field(
        default=None,
        description="Optional. For “pre” only, the programming language of the entity text.",
    )
    custom_emoji_id: str | None = Field(
        default=None,
        description="Optional. For “custom_emoji” only, unique identifier of the custom emoji.",
    )


class Message(BaseModel, ValidableMixin):
    """This model represents a message.

    See here: https://core.telegram.org/bots/api#message
    """

    message_id: int = Field(
        description="Unique message identifier inside this chat.",
    )
    message_thread_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. Unique identifier of a message thread to which the message belongs; for supergroups only.
        """),
    )
    from_: User | None = Field(
        default=None,
        alias="from",
        description=dedent("""\
            Optional. Sender of the message; empty for messages sent to channels. For backward compatibility,
            the field contains a fake sender user in non-channel chats, if the message was sent on behalf of a chat.
        """),
    )
    sender_chat: Chat | None = Field(
        default=None,
        description=dedent("""\
            Optional. Sender of the message, sent on behalf of a chat. For example,
            the channel itself for channel posts,the supergroup itself for messages
            from anonymous group administrators, the linked channel for messages
            automatically forwarded to the discussion group. For backward compatibility,
            the field from contains a fake sender user in non-channel chats,
            if the message was sent on behalf of a chat.
        """),
    )
    date: int = Field(
        description="Date the message was sent in Unix time.",
    )
    chat: Chat = Field(
        description="Conversation the message belongs to.",
    )
    forward_from: User | None = Field(
        default=None,
        description="Optional. For forwarded messages, sender of the original message.",
    )
    forward_from_chat: Chat | None = Field(
        default=None,
        description=dedent("""\
            Optional. For messages forwarded from channels or from anonymous administrators,
            information about the original sender chat.
        """),
    )
    forward_from_message_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. For messages forwarded from channels, identifier of the original message in the channel.
        """),
    )
    forward_signature: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. For forwarded messages that were originally sent in channels or
            by an anonymous chat administrator, signature of the message sender if present.
        """),
    )
    forward_sender_name: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Sender's name for messages forwarded from users who disallow
            adding a link to their account in forwarded messages.
        """),
    )
    forward_date: int | None = Field(
        default=None,
        description="Optional. For forwarded messages, date the original message was sent in Unix time.",
    )
    is_topic_message: dict[str, Any] | None = Field(
        default=None,
        description="Optional. True, if the message is sent to a forum topic.",
    )
    is_automatic_forward: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. True, if the message is a channel post that was automatically
            forwarded to the connected discussion group.
        """),
    )
    reply_to_message: Optional['Message'] = Field(
        default=None,
        description=dedent("""\
            Optional. For replies, the original message. Note that the Message object
            in this field will not contain further reply_to_message fields even if it itself is a reply.
        """),
    )
    via_bot: User | None = Field(
        default=None,
        description="Optional. Bot through which the message was sent.",
    )
    edit_date: int | None = Field(
        default=None,
        description="Optional. Date the message was last edited in Unix time.",
    )
    has_protected_content: bool | None = Field(
        default=None,
        description="Optional. True, if the message can't be forwarded.",
    )
    media_group_id: str | None = Field(
        default=None,
        description="Optional. The unique identifier of a media message group this message belongs to.",
    )
    author_signature: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Signature of the post author for messages in channels,
            or the custom title of an anonymous group administrator.
        """),
    )
    text: str | None = Field(
        default=None,
        description="Optional. For text messages, the actual UTF-8 text of the message.",
    )
    entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. For text messages, special entities like usernames,
            URLs, bot commands, etc. that appear in the text.
        """),
    )
    animation: dict[str, Any] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Message is an animation, information about the animation.
            For backward compatibility, when this field is set, the document field will also be set.
        """),
    )
    audio: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is an audio file, information about the file.",
    )
    document: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a general file, information about the file.",
    )
    photo: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional. Message is a photo, available sizes of the photo.",
    )
    sticker: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a sticker, information about the sticker.",
    )
    video: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a video, information about the video.",
    )
    video_note: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a video note, information about the video message.",
    )
    voice: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a voice message, information about the file.",
    )
    caption: str | None = Field(
        default=None,
        description="Optional. Caption for the animation, audio, document, photo, video or voice.",
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. For messages with a caption, special entities like usernames,
            URLs, bot commands, etc. that appear in the caption.
        """),
    )
    has_media_spoiler: bool | None = Field(
        default=None,
        description="Optional. True, if the message media is covered by a spoiler animation.",
    )
    contact: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a shared contact, information about the contact.",
    )
    dice: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a dice with random value.",
    )
    game: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a game, information about the game.",
    )
    poll: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a native poll, information about the poll.",
    )
    venue: dict[str, Any] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Message is a venue, information about the venue. For backward compatibility,
            when this field is set, the location field will also be set.
        """),
    )
    location: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Message is a shared location, information about the location.",
    )
    new_chat_members: list[User] | None = Field(
        default=None,
        description=dedent("""\
            Optional. New members that were added to the group
            or supergroup and information about them (the bot itself may be one of these members).
        """),
    )
    left_chat_member: User | None = Field(
        default=None,
        description=dedent("""\
            Optional. A member was removed from the group, information about them (this member may be the bot itself).
        """),
    )
    new_chat_title: str | None = Field(
        default=None,
        description="Optional. A chat title was changed to this value.",
    )
    new_chat_photo: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional. A chat photo was change to this value.",
    )
    delete_chat_photo: bool | None = Field(
        default=None,
        description="Optional. Service message: the chat photo was deleted.",
    )
    group_chat_created: bool | None = Field(
        default=None,
        description="Optional. Service message: the group has been created.",
    )
    supergroup_chat_created: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Service message: the supergroup has been created. This field can't be received in a message
            coming through updates, because bot can't be a member of a supergroup when it is created. It can only
            be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
        """),
    )
    channel_chat_created: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Service message: the channel has been created. This field can't be received in a message
            coming through updates, because bot can't be a member of a channel when it is created. It can only
            be found in reply_to_message if someone replies to a very first message in a channel.
        """),
    )
    message_auto_delete_timer_changed: list[dict[str, Any]] | None = Field(
        default=None,
        description="Optional. Service message: auto-delete timer settings changed in the chat.",
    )
    migrate_to_chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The group has been migrated to a supergroup with the specified identifier.
            This number may have more than 32 significant bits and some programming languages may
            have difficulty/silent defects in interpreting it. But it has at most 52 significant bits,
            so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        """),
    )
    migrate_from_chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The supergroup has been migrated from a group with the specified identifier.
            This number may have more than 32 significant bits and some programming languages may
            have difficulty/silent defects in interpreting it. But it has at most 52 significant bits,
            so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
        """),
    )
    pinned_message: Optional['Message'] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Specified message was pinned. Note that the Message object in this field
            will not contain further reply_to_message fields even if it is itself a reply.
        """),
    )
    invoice: Invoice | None = Field(
        default=None,
        description="Optional. Message is an invoice for a payment, information about the invoice.",
    )
    successful_payment: SuccessfulPayment | None = Field(
        default=None,
        description=dedent("""\
            Optional. Message is a service message about a successful payment, information about the payment.
        """),
    )
    user_shared: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: a user was shared with the bot.",
    )
    chat_shared: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: a chat was shared with the bot.",
    )
    connected_website: str | None = Field(
        default=None,
        description="Optional. The domain name of the website on which the user has logged in.",
    )
    write_access_allowed: dict[str, Any] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Service message: the user allowed the bot to write messages after adding
            it to the attachment or side menu, launching a Web App from a link, or accepting an
            explicit request from a Web App sent by the method requestWriteAccess.
        """),
    )
    passport_data: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Telegram Passport data.",
    )
    proximity_alert_triggered: dict[str, Any] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Service message. A user in the chat triggered another user's proximity
            alert while sharing Live Location.
        """),
    )
    forum_topic_created: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: forum topic created.",
    )
    forum_topic_edited: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: forum topic edited.",
    )
    forum_topic_closed: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: forum topic closed.",
    )
    forum_topic_reopened: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: forum topic reopened.",
    )
    general_forum_topic_hidden: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: the 'General' forum topic hidden.",
    )
    general_forum_topic_unhidden: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: the 'General' forum topic unhidden.",
    )
    video_chat_scheduled: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: video chat scheduled.",
    )
    video_chat_started: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: video chat started.",
    )
    video_chat_ended: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: video chat ended.",
    )
    video_chat_participants_invited: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: new participants invited to a video chat.",
    )
    web_app_data: dict[str, Any] | None = Field(
        default=None,
        description="Optional. Service message: data sent by a Web App.",
    )
    reply_markup: InlineKeyboardMarkup | None = Field(
        default=None,
        description=dedent("""\
            Optional. Inline keyboard attached to the message.
            login_url buttons are represented as ordinary url buttons.
    """),
    )


class MessageReplyMarkup(BaseModel, ValidableMixin):
    message_reply_markup: Union[Message, bool] = Field(
        description="",
    )


class InputMediaUrlPhoto(BaseModel, ValidableMixin):
    """This model represents a photo with url or file id.

    See here: https://core.telegram.org/bots/api#inputmediaphoto
    """

    type: str = Field(  # noqa A003
        default="photo",
        description="Type of the result, must be photo.",
    )
    media: str = Field(
        description=dedent("""\
            File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended),
            pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>”
            to upload a new one using multipart/form-data under <file_attach_name> name.
        """),
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing.",
    )
    parse_mode: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
        """),
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. List of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    has_spoiler: bool | None = Field(
        default=None,
        description="Optional. Pass True if the photo needs to be covered with a spoiler animation.",
    )


class InputMediaBytesPhoto(BaseModel, ValidableMixin):
    """This model represents a photo with file.

    See here: https://core.telegram.org/bots/api#inputmediaphoto
    """

    type: str = Field(  # noqa A003
        default="photo",
        description="Type of the result, must be photo.",
    )
    media: str = Field(
        description=dedent("""\
            File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended),
            pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>”
            to upload a new one using multipart/form-data under <file_attach_name> name.
        """),
    )
    media_content: bytes = Field(
        description="File to send in bytes.",
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="Optional. Caption of the photo to be sent, 0-1024 characters after entities parsing.",
    )
    parse_mode: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Mode for parsing entities in the photo caption. See formatting options for more details.
        """),
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. List of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    has_spoiler: bool | None = Field(
        default=None,
        description="Optional. Pass True if the photo needs to be covered with a spoiler animation.",
    )


class InputMediaUrlDocument(BaseModel, ValidableMixin):
    """This model represents a document with url or file id.

    See here: https://core.telegram.org/bots/api#inputmediadocument
    """

    type: str = Field(  # noqa A003
        default="document",
        description="Type of the result, must be document",
    )
    media: str = Field(
        description=dedent("""\
            File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended),
            pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>”
            to upload a new one using multipart/form-data under <file_attach_name> name.
        """),
    )
    thumbnail: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Thumbnail of the file sent; can be ignored if thumbnail generation
            for the file is supported server-side. The thumbnail should be in JPEG format
            and less than 200 kB in size. A thumbnail's width and height should not exceed 320.
            Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be
            reused and can be only uploaded as a new file, so you can pass “attach://<file_attach_name>”
            if the thumbnail was uploaded using multipart/form-data under <file_attach_name>.
        """),
    )
    thumbnail_content: bytes | None = Field(
        default=None,
        description="Thumbnail of the sent file in bytes.",
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="Optional. Caption of the document to be sent, 0-1024 characters after entities parsing.",
    )
    parse_mode: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Mode for parsing entities in the document caption. See formatting options for more details.
        """),
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. List of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    disable_content_type_detection: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Disables automatic server-side content type detectionfor filesuploaded using
            multipart/form-data. Always True, if the document is sent as part of an album.
        """),
    )


class InputMediaBytesDocument(BaseModel, ValidableMixin):
    """This model represents a document with file.

    See here: https://core.telegram.org/bots/api#inputmediadocument
    """

    type: str = Field(  # noqa A003
        default="document",
        description="Type of the result, must be document.",
    )
    media: str = Field(
        description=dedent("""\
            File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended),
            pass an HTTP URL for Telegram to get a file from the Internet, or pass “attach://<file_attach_name>”
            to upload a new one using multipart/form-data under <file_attach_name> name.
        """),
    )
    media_content: bytes = Field(
        description="File to send in bytes.",
    )
    thumbnail: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported
            server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width
            and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data.
            Thumbnails can't be reused and can be only uploaded as a new file,
            so you can pass “attach://<file_attach_name>” if the thumbnail was uploaded
            using multipart/form-data under <file_attach_name>.
        """),
    )
    thumbnail_content: bytes | None = Field(
        default=None,
        description="Thumbnail of the sent file in bytes.",
    )
    caption: str = Field(
        default=None,
        max_length=1024,
        description="Optional. Caption of the document to be sent, 0-1024 characters after entities parsing.",
    )
    parse_mode: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Mode for parsing entities in the document caption. See formatting options for more details.
        """),
    )
    caption_entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. List of special entities that appear in the caption,
            which can be specified instead of parse_mode.
        """),
    )
    disable_content_type_detection: bool | None = Field(
        default=None,
        description=dedent("""\
            Optional. Disables automatic server-side content type detection for files uploaded using
            multipart/form-data. Always True, if the document is sent as part of an album.
        """),
    )


class CallbackQuery(BaseModel, ValidableMixin):
    """This object represents an incoming callback query from a callback button in an inline keyboard.

    See here: https://core.telegram.org/bots/api#callbackquery
    """

    id: str = Field(  # noqa A003
        alias="id",
        description="Unique identifier for this query.",
    )
    from_: User = Field(
        alias="from",
        description="Sender.",
    )
    message: Message | None = Field(
        default=None,
        description=dedent("""\
            Optional. Message with the callback button that originated the query. Note that message content
            and message date will not be available if the message is too old.
        """),
    )
    inline_message_id: str | None = Field(
        default=None,
        description="Optional. Identifier of the message sent via the bot in inline mode, that originated the query.",
    )
    chat_instance: str | None = Field(
        default=None,
        description=dedent("""\
            Global identifier, uniquely corresponding to the chat to which the message with the callback
            button was sent. Useful for high scores in games.
        """),
    )
    data: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Data associated with the callback button. Be aware that the message originated the
            query can contain no callback buttons with this data.
        """),
    )
    game_short_name: str | None = Field(
        default=None,
        description="Optional. Short name of a Game to be returned, serves as the unique identifier for the game.",
    )

    @root_validator
    def check_callback_query(cls: CallbackQuery, tg_request: dict) -> dict | None:  # noqa N805
        data = tg_request["data"]
        game_short_name = tg_request["game_short_name"]
        if not data and not game_short_name:
            raise ValueError(dedent("""\
                Both fields data and game_short_name are missing. At least one of them must be specified.
            """))

        return tg_request


class Location(BaseModel, ValidableMixin):
    """This object represents a point on the map.

    See here: https://core.telegram.org/bots/api#location
    """

    longitude: float = Field(
        description="Longitude as defined by sender.",
    )
    latitude: float = Field(
        description="Latitude as defined by sender.",
    )
    horizontal_accuracy: float | None = Field(
        default=None,
        description="Optional. The radius of uncertainty for the location, measured in meters; 0-1500.",
    )
    live_period: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. Time relative to the message sending date, during which the location can be updated;
            in seconds. For active live locations only.
        """),
    )
    heading: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The direction in which user is moving, in degrees; 1-360. For active live locations only.
        """),
    )
    proximity_alert_radius: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The maximum distance for proximity alerts about approaching another chat member,
            in meters. For sent live locations only.
        """),
    )


class InlineQuery(BaseModel, ValidableMixin):
    """This object represents an incoming inline query.

    When the user sends an empty query, your bot could return some default or trending results.
    See here: https://core.telegram.org/bots/api#inlinequery
    """

    id: str = Field(  # noqa A003
        description="Unique identifier for this query",
    )
    from_: User = Field(
        alias="from",
        description="Sender",
    )
    query: str = Field(
        description="Text of the query (up to 256 characters).",
    )
    offset: str = Field(
        description="Offset of the results to be returned, can be controlled by the bot.",
    )
    chat_type: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Type of the chat from which the inline query was sent. Can be either “sender” for a private
            chat with the inline query sender, “private”, “group”, “supergroup”, or “channel”. The chat type should
            be always known for requests sent from official clients and most third-party clients, unless the request
            was sent from a secret chat.
        """),
    )
    location: Location | None = Field(
        default=None,
        description="Optional. Sender location, only for bots that request user location.",
    )


class ChosenInlineResult(BaseModel, ValidableMixin):
    """Represents a result of an inline query that was chosen by the user and sent to their chat partner.

    Note: It is necessary to enable inline feedback via @BotFather in order to receive these objects in updates.
    See here: https://core.telegram.org/bots/api#choseninlineresult
    """

    result_id: str = Field(
        description="The unique identifier for the result that was chosen",
    )
    from_: User = Field(
        alias="from",
        description="The user that chose the result.",
    )
    location: Location | None = Field(
        default=None,
        description="Optional. Sender location, only for bots that require user location.",
    )
    inline_message_id: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Identifier of the sent inline message. Available only if there is an inline keyboard
            attached to the message. Will be also received in callback queries and can be used to edit the message.
        """),
    )
    query: str | None = Field(
        default=None,
        description="The query that was used to obtain the result.",
    )


class ShippingQuery(BaseModel, ValidableMixin):
    """This object contains information about an incoming shipping query.

    See here: https://core.telegram.org/bots/api#shippingquery
    """

    id: str = Field(  # noqa A003
        description="Unique query identifier.",
    )
    from_: User = Field(
        alias="from",
        description="User who sent the query.",
    )
    invoice_payload: str = Field(  # noqa A003
        description="Bot specified invoice payload.",
    )
    shipping_address: ShippingAddress = Field(
        description="User specified shipping address.",
    )


class PreCheckoutQuery(BaseModel, ValidableMixin):
    """This object contains information about an incoming pre-checkout query.

    See here: https://core.telegram.org/bots/api#precheckoutquery
    """

    id: str = Field(  # noqa A003
        description="Unique query identifier.",
    )
    from_: User = Field(
        alias="from",
        description="User who sent the query.",
    )
    currency: str = Field(
        description="Three-letter ISO 4217 currency code.",
    )
    total_amount: int = Field(
        description=dedent("""\
            Total price in the smallest units of the currency (integer, not float/double). For example,
            for a price of US$ 1.45 pass amount = 145. See the exp parameter in currencies.json, it shows
            the number of digits past the decimal point for each currency (2 for the majority of currencies).
        """),
    )
    invoice_payload: str = Field(
        description="Bot specified invoice payload.",
    )
    shipping_option_id: str | None = Field(
        default=None,
        description="Optional. Identifier of the shipping option chosen by the user.",
    )
    order_info: OrderInfo | None = Field(
        default=None,
        description="Optional. Order information provided by the user.",
    )


class PollOption(BaseModel, ValidableMixin):
    """This object contains information about one answer option in a poll.

    See here: https://core.telegram.org/bots/api#polloption
    """

    text: str = Field(
        description="Option text, 1-100 characters.",
    )
    voter_count: int = Field(
        description="Number of users that voted for this option.",
    )


class Poll(BaseModel, ValidableMixin):
    """This object contains information about a poll.

    See here: https://core.telegram.org/bots/api#poll
    """

    id: str = Field(  # noqa A003
        description="Unique poll identifier.",
    )
    question: str = Field(
        description="Poll question, 1-300 characters.",
    )
    options: list[PollOption] = Field(
        description="List of poll options.",
    )
    total_voter_count: int = Field(
        description="Total number of users that voted in the poll.",
    )
    is_closed: bool = Field(
        description="True, if the poll is closed.",
    )
    is_anonymous: bool = Field(  # noqa A003
        description="True, if the poll is anonymous.",
    )
    type: str = Field(  # noqa A003
        description="Poll type, currently can be “regular” or “quiz”.",
    )
    allows_multiple_answers: bool = Field(
        description="True, if the poll allows multiple answers.",
    )
    correct_option_id: int | None = Field(  # noqa A003
        default=None,
        description=dedent("""\
            Optional. 0-based identifier of the correct answer option. Available only for polls in the quiz mode,
            which are closed, or was sent (not forwarded) by the bot or to the private chat with the bot.
        """),
    )
    explanation: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Text that is shown when a user chooses an incorrect answer or taps
            on the lamp icon in a quiz-style poll, 0-200 characters.
        """),
    )
    explanation_entities: list[MessageEntity] | None = Field(
        default=None,
        description=dedent("""\
            Optional. Special entities like usernames, URLs, bot commands, etc. that appear in the explanation.
        """),
    )
    open_period: int | None = Field(
        default=None,
        description="Optional. Amount of time in seconds the poll will be active after creation.",
    )
    close_date: int | None = Field(
        default=None,
        description="Optional. Point in time (Unix timestamp) when the poll will be automatically closed.",
    )


class PollAnswer(BaseModel, ValidableMixin):
    """This object represents an answer of a user in a non-anonymous poll.

    See here: https://core.telegram.org/bots/api#pollanswer
    """

    poll_id: str = Field(
        description="Unique poll identifier.",
    )
    user: User = Field(
        description="Optional. The user that changed the answer to the poll, if the voter isn't anonymous.",
    )
    option_ids: list[int] = Field(
        description="0-based identifiers of chosen answer options. May be empty if the vote was retracted.",
    )


class ChatInviteLink(BaseModel, ValidableMixin):
    """Represents an invite link for a chat.

    See here: https://core.telegram.org/bots/api#chatinvitelink
    """

    invite_link: str = Field(
        description=dedent("""\
            The invite link. If the link was created by another chat administrator,
            then the second part of the link will be replaced with “…”.
        """),
    )
    creator: User = Field(
        description="Creator of the link.",
    )
    creates_join_request: bool = Field(
        description="True, if users joining the chat via the link need to be approved by chat administrators.",
    )
    is_primary: bool = Field(
        description="True, if the link is primary.",
    )
    is_revoked: bool = Field(
        description="True, if the link is revoked.",
    )
    name: str | None = Field(
        default=None,
        description="Optional. Invite link name.",
    )
    expire_date: int | None = Field(
        default=None,
        description="Optional. Point in time (Unix timestamp) when the link will expire or has been expired.",
    )
    member_limit: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The maximum number of users that can be members of the chat simultaneously
            after joining the chat via this invite link; 1-99999.
        """),
    )
    pending_join_request_count: int | None = Field(
        default=None,
        description="Optional. Number of pending join requests created using this link.",
    )


class ChatJoinRequest(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatjoinrequest
    """

    chat: Chat = Field(
        description="Chat to which the request was sent.",
    )
    from_: User = Field(
        alias="from",
        description="User that sent the join request.",
    )
    user_chat_id: int = Field(
        description=dedent("""\
            Identifier of a private chat with the user who sent the join request. This number may have
            more than 32 significant bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision
            float type are safe for storing this identifier. The bot can use this identifier for 5 minutes
            to send messages until the join request is processed, assuming no other administrator contacted the user.
        """),
    )
    date: int = Field(
        description="Date the request was sent in Unix time.",
    )
    bio: str | None = Field(
        default=None,
        description="Optional. Bio of the user.",
    )
    invite_link: ChatInviteLink | None = Field(
        default=None,
        description="Optional. Chat invite link that was used by the user to send the join request.",
    )


class ChatMemberOwner(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberowner
    """

    status: str = Field(
        description="The member's status in the chat, always “creator”.",
    )
    user: User = Field(
        description="Information about the user.",
    )
    is_anonymous: bool = Field(
        description="True, if the user's presence in the chat is hidden.",
    )
    custom_title: str = Field(
        description="Optional. Custom title for this user.",
    )


class ChatMemberAdministrator(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberadministrator
    """

    status: str = Field(
        description="The member's status in the chat, always “administrator”.",
    )
    user: User = Field(
        description="Information about the user.",
    )
    can_be_edited: bool = Field(
        description="True, if the bot is allowed to edit administrator privileges of that user.",
    )
    is_anonymous: bool = Field(
        description="True, if the user's presence in the chat is hidden.",
    )
    can_manage_chat: bool = Field(
        description=dedent("""\
            True, if the administrator can access the chat event log, boost list in channels,
            see channel members, report spam messages, see anonymous administrators in supergroups
            and ignore slow mode. Implied by any other administrator privilege.
        """),
    )
    can_delete_messages: bool = Field(
        description="True, if the administrator can delete messages of other users.",
    )
    can_manage_video_chats: bool = Field(
        description="True, if the administrator can manage video chats.",
    )
    can_restrict_members: bool = Field(
        description=dedent("""\
            True, if the administrator can restrict, ban or unban chat members, or access supergroup statistics.
        """),
    )
    can_promote_members: bool = Field(
        description=dedent("""\
            True, if the administrator can add new administrators with a subset of their own privileges or demote
            administrators that they have promoted, directly or indirectly
            (promoted by administrators that were appointed by the user).
        """),
    )
    can_change_info: bool = Field(
        description="True, if the user is allowed to change the chat title, photo and other settings.",
    )
    can_invite_users: bool = Field(
        description="True, if the user is allowed to invite new users to the chat.",
    )
    can_post_messages: bool = Field(
        description=dedent("""\
            Optional. True, if the administrator can post messages in the channel,
            or access channel statistics; channels only.
        """),
    )
    can_edit_messages: bool = Field(
        description=dedent("""\
            Optional. True, if the administrator can edit messages of other users and can pin messages; channels only.
        """),
    )
    can_pin_messages: bool = Field(
        description="Optional. True, if the user is allowed to pin messages; groups and supergroups only.",
    )
    can_manage_topics: bool = Field(
        description=dedent("""\
            Optional. True, if the user is allowed to create, rename, close,
            and reopen forum topics; supergroups only.
        """),
    )
    custom_title: bool = Field(
        description="Optional. Custom title for this user.",
    )


class ChatMemberMember(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmembermember
    """

    status: str = Field(
        description="The member's status in the chat, always “member”.",
    )
    user: User = Field(
        description="Information about the user.",
    )


class ChatMemberRestricted(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberrestricted
    """

    status: str = Field(
        description="The member's status in the chat, always “restricted”.",
    )
    user: User = Field(
        description="Information about the user.",
    )
    is_member: bool = Field(
        description="True, if the user is a member of the chat at the moment of the request.",
    )
    can_send_messages: bool = Field(
        description="True, if the user is allowed to send text messages, contacts, invoices, locations and venues.",
    )
    can_send_audios: bool = Field(
        description="True, if the user is allowed to send audios.",
    )
    can_send_documents: bool = Field(
        description="True, if the user is allowed to send documents.",
    )
    can_send_photos: bool = Field(
        description="True, if the user is allowed to send photos.",
    )
    can_send_videos: bool = Field(
        description="True, if the user is allowed to send videos.",
    )
    can_send_video_notes: bool = Field(
        description="True, if the user is allowed to send video notes.",
    )
    can_send_voice_notes: bool = Field(
        description="True, if the user is allowed to send voice notes.",
    )
    can_send_polls: bool = Field(
        description="True, if the user is allowed to send polls.",
    )
    can_send_other_messages: bool = Field(
        description="True, if the user is allowed to send animations, games, stickers and use inline bots.",
    )
    can_add_web_page_previews: bool = Field(
        description="True, if the user is allowed to add web page previews to their messages.",
    )
    can_change_info: bool = Field(
        description="True, if the user is allowed to change the chat title, photo and other settings.",
    )
    can_invite_users: bool = Field(
        description="True, if the user is allowed to invite new users to the chat.",
    )
    can_pin_messages: bool = Field(
        description="True, if the user is allowed to pin messages.",
    )
    can_manage_topics: bool = Field(
        description="True, if the user is allowed to create forum topics.",
    )
    until_date: bool = Field(
        description=dedent("""\
            Date when restrictions will be lifted for this user; Unix time. If 0, then the user is restricted forever.
        """),
    )


class ChatMemberLeft(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberleft
    """

    status: str = Field(
        description="The member's status in the chat, always “left”.",
    )
    user: User = Field(
        description="Information about the user.",
    )


class ChatMemberBanned(BaseModel, ValidableMixin):
    """Represents a join request sent to a chat.

    See here: https://core.telegram.org/bots/api#chatmemberbanned
    """

    status: str = Field(
        description="The member's status in the chat, always “kicked”.",
    )
    user: User = Field(
        description="Information about the user.",
    )
    until_date: int = Field(
        description=dedent("""\
            Date when restrictions will be lifted for this user; Unix time. If 0, then the user is banned forever.
        """),
    )


class ChatMemberUpdated(BaseModel, ValidableMixin):
    """This object represents changes in the status of a chat member.

    See here: https://core.telegram.org/bots/api#chatmemberupdated
    """

    chat: Chat = Field(
        description="Chat the user belongs to.",
    )
    from_: User = Field(
        alias="from",
        description="Performer of the action, which resulted in the change.",
    )
    date: int = Field(
        description="Date the change was done in Unix time.",
    )
    old_chat_member: Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ] = Field(
        description="Previous information about the chat member.",
    )
    new_chat_member: Union[
        ChatMemberOwner,
        ChatMemberAdministrator,
        ChatMemberMember,
        ChatMemberRestricted,
        ChatMemberLeft,
        ChatMemberBanned,
    ] = Field(
        description="New information about the chat member.",
    )
    invite_link: ChatInviteLink | None = Field(
        default=None,
        description=dedent("""\
            Optional. Chat invite link, which was used by the user to join the chat;
            for joining by invite link events only.
        """),
    )
    via_chat_folder_invite_link: bool = Field(
        default=None,
        description="Optional. True, if the user joined the chat via a chat folder invite link.",
    )


class Update(BaseModel, ValidableMixin):
    """This object represents an incoming update.

    See here: https://core.telegram.org/bots/api#update
    """

    update_id: int = Field(
        description=dedent("""\
            The update's unique identifier. Update identifiers start from a certain positive number
            and increase sequentially. This ID becomes especially handy if you're using webhooks, since
            it allows you to ignore repeated updates or to restore the correct update sequence, should they
            get out of order. If there are no new updates for at least a week, then identifier of the next update
            will be chosen randomly instead of sequentially.
        """),
    )
    message: Message | None = Field(
        default=None,
        description='Optional. New incoming message of any kind - text, photo, sticker, etc.',
    )
    edited_message: Message | None = Field(
        description='Optional. New version of a message that is known to the bot and was edited.',
    )
    channel_post: Message | None = Field(
        description='Optional. New incoming channel post of any kind - text, photo, sticker, etc.',
    )
    edited_channel_post: Message | None = Field(
        description='Optional. New version of a channel post that is known to the bot and was edited.',
    )
    inline_query: InlineQuery | None = Field(
        default=None,
        description="Optional. New incoming inline query.",
    )
    chosen_inline_result: ChosenInlineResult | None = Field(
        default=None,
        description=dedent("""\
            Optional. The result of an inline query that was chosen by a user and sent to their chat partner.
            Please see our documentation on the feedback collecting for details
            on how to enable these updates for your bot.
        """),
    )
    callback_query: CallbackQuery | None = Field(
        default=None,
        description="Optional. New incoming callback query.",
    )
    shipping_query: ShippingQuery | None = Field(
        default=None,
        description="Optional. New incoming shipping query. Only for invoices with flexible price.",
    )
    pre_checkout_query: PreCheckoutQuery | None = Field(
        default=None,
        description="Optional. New incoming pre-checkout query. Contains full information about checkout.",
    )
    poll: Poll | None = Field(
        default=None,
        description=dedent("""\
            Optional. New poll state. Bots receive only updates about
            stopped polls and polls, which are sent by the bot.
        """),
    )
    poll_answer: PollAnswer | None = Field(
        default=None,
        description=dedent("""\
            Optional. A user changed their answer in a non-anonymous poll.
            Bots receive new votes only in polls that were sent by the bot itself.
        """),
    )
    my_chat_member: ChatMemberUpdated | None = Field(
        default=None,
        description=dedent("""\
            Optional. The bot's chat member status was updated in a chat.
            For private chats, this update is received only when the bot is blocked or unblocked by the user.
        """),
    )
    chat_member: ChatMemberUpdated | None = Field(
        default=None,
        description=dedent("""\
            Optional. A chat member's status was updated in a chat. The bot must be an administrator
            in the chat and must explicitly specify `chat_member` in the list
            of allowed_updates to receive these updates.
        """),
    )
    chat_join_request: ChatJoinRequest | None = Field(
        default=None,
        description=dedent("""\
            Optional. A request to join the chat has been sent. The bot must have the can_invite_users
            administrator right in the chat to receive these updates.
        """),
    )

    @property
    def chat_id(self) -> int:
        if self.message:
            return self.message.chat.id
        if self.callback_query:
            return self.callback_query.from_.id


# TODO At most one of the optional parameters can be present in any given update.


class ResponseParameters(BaseModel, ValidableMixin):
    """Describes why a request was unsuccessful.

    See here: https://core.telegram.org/bots/api#responseparameters
    """

    migrate_to_chat_id: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. The group has been migrated to a supergroup with the specified identifier. This number may have
            more than 32 significant bits and some programming languages may have difficulty/silent defects
            in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision
            float type are safe for storing this identifier.
        """),
    )
    retry_after: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. In case of exceeding flood control, the number of seconds
            left to wait before the request can be repeated
        """),
    )


class WebhookInfo(BaseModel, ValidableMixin):
    """Describes the current status of a webhook.

    https://core.telegram.org/bots/api#webhookinfo
    """

    url: str = Field(
        description="Webhook URL, may be empty if webhook is not set up",
    )
    has_custom_certificate: bool = Field(
        description=dedent("""\
            True, if a custom certificate was provided for webhook certificate
            checks.
        """),
    )
    pending_update_count: int = Field(
        description="Number of updates awaiting delivery",
    )
    ip_address: str | None = Field(
        default=None,
        description="Optional. Currently used webhook IP address",
    )
    last_error_date: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. Unix time for the most recent error
            that happened when trying to deliver an update
            via webhook
        """),
    )
    last_error_message: str | None = Field(
        default=None,
        description=dedent("""\
            Optional. Error message in human-readable format
            for the most recent error that happened when trying to deliver
            an update via webhook
        """),
    )
    last_synchronization_error_date: int | None = Field(
        default=None,
        description=dedent("""\
            Optional. Unix time of the most recent error that happened
            when trying to synchronize available updates
            with Telegram datacenters
        """),
    )
    max_connections: int | None = Field(
        default=None,
        description=dedent("""\
           Optional. The maximum allowed number of simultaneous HTTPS
           connections to the webhook for update delivery
        """),
    )
    allowed_updates: list[str] | None = Field(
        default=None,
        description=dedent("""\
           Optional. A list of update types the bot is subscribed to.
           Defaults to all update types except chat_member
        """),
    )


# fix ForwardRef fpr cyclic refernces Chat --> Message --> Chat
Chat.update_forward_refs()
