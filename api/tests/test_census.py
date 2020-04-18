import unittest
from unittest.mock import Mock

import pytest

from census.census import Palma
from census.entities import Context, Voter


class PalmaCensusTest(unittest.TestCase):

    @pytest.mark.asyncio
    async def test_finds_nif(self):

        async def client_find_by_nif():
            response_mock = Mock()
            response_mock.text = 'client-response'
            return response_mock

        client = Mock()
        client.find_by_nif('12345678A')

        client.find_by_nif.return_value = client_find_by_nif()

        context = Context('12345678A')

        parser = Mock()
        parser.parse_response(context, 'client-response')
        parser.parse_response.return_value = Voter(None, None, None)

        census = Palma(client=client, parser=parser)
        await census.find_by_nif('12345678A')

        client.find_by_nif.assert_called_with('12345678A')
        parser.parse_response.assert_called_with(context, 'client-response')

