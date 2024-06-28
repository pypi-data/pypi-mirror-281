""" This module provides a way to access the BitwardenHandler class and its methods. """
import os

from .exceptions import NotLoggedInError


class BitwardenHandler:
    """Class to handle Bitwarden operations."""

    _last_used_bitwarden = None

    @classmethod
    def get_attachment(cls, item_name: str, file_name: str, output_folder: str = os.getcwd()):
        """Retrieve an attachment from a Bitwarden credential group."""
        if cls._last_used_bitwarden is None or not cls._last_used_bitwarden.is_logged_in:
            raise NotLoggedInError("You must be logged in to Bitwarden to access attachments.")
        return cls._last_used_bitwarden.get_attachment(item_name, file_name, output_folder)


get_attachment = BitwardenHandler.get_attachment
