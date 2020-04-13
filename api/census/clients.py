from abc import ABC, abstractmethod

import httpx


class Client(ABC):

    @abstractmethod
    async def find_by_nif(self, nif) -> str:
        pass


class Palma(Client):
    BASE_URL = 'https://cens.palma.cat'
    URL = f'{BASE_URL}/portal/PALMA/cens/cens_principal1.jsp?codResi=1'

    def __init__(self, http_client=None):
        self.http_client = http_client or httpx.AsyncClient()

    async def find_by_nif(self, nif):
        params = self._build_params(nif)
        headers = self._build_headers()
        async with self.http_client as client:
            return await client.get(self.URL, params=params, headers=headers)

    def _build_params(self, nif):
        return {
            'form_name': 'formcenso',
            'seccion': 'Consulta.jsp',
            'nifPersona': nif
        }

    def _build_headers(self):
        return {
            'Origin': self.BASE_URL,
            'Referer': self.URL,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.8',
        }
