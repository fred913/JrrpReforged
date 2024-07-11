from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID


class McUuidModule(ABC):

    @staticmethod
    @abstractmethod
    def nameUUIDFromBytes(name: bytes) -> UUID:
        """
        Static factory to retrieve a type 3 (name based) UUID based on
        the specified byte array.

        :param name: A byte array to be used to construct a UUID

        :return: A UUID generated from the specified array
        """
        pass

    @staticmethod
    @abstractmethod
    def checkPlayerName(player: str) -> bool:
        """
        Check if player name is legal

        :param player: Player name

        :return: Return `True` if the player name is legal
        """
        pass

    @staticmethod
    @abstractmethod
    def offlineUUID(player: str, check_name: bool = True) -> Optional[UUID]:
        """
        Generate a UUID based on the player name

        :param player: Player name
        :param check_name: Whether to check the legitimacy of the player name

        :return: A UUID generated from the player name or `None` if the name is illegal
        """
        pass

    @staticmethod
    @abstractmethod
    def onlineUUID(player: str) -> UUID:
        """
        Get player's online UUID from Mojang API

        :param player: Player name

        :return: A UUID generated from the player name or `None` if the name is illegal
        """
        pass
