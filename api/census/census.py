from abc import ABC, abstractmethod
from copy import copy

from httpx import AsyncClient

from census import clients
from census import parsers
from census.entities import Context, Voter


class Census(ABC):

    @abstractmethod
    async def find_by_nif(self, nif) -> Voter:
        pass


class Palma(Census):

    def __init__(self, client=None, parser=None):
        self.client = client or clients.Palma()
        self.parser = parser or parsers.Palma()

    async def find_by_nif(self, nif) -> Voter:
        context = Context(nif)
        response = await self.client.find_by_nif(nif)
        return self.parser.parse_response(context, response.text)
