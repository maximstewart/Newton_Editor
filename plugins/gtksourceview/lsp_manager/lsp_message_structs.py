# Python imports
from dataclasses import dataclass
import json

# Lib imports

# Application imports



def get_message_obj(data: str):
    return json.loads(data)


@dataclass
class LSPResponseRequest(object):
        """
        Constructs a new LSP Response Request instance.

        :param id result: The id of the given message.
        :param dict result: The arguments of the given method.
        """
        jsonrpc: str
        id: int
        result: dict

@dataclass
class LSPResponseNotification(object):
        """
        Constructs a new LSP Response Notification instance.

        :param str method: The type of lsp notification being made.
        :params dict result: The arguments of the given method.
        """
        jsonrpc: str
        method: str
        params: dict


class LSPResponseTypes(LSPResponseRequest, LSPResponseNotification):
    ...