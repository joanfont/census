from copy import copy
from bs4 import BeautifulSoup
import requests
from re import compile


class BaseError(Exception):
    def __init__(self, error_code, error_desc, status_code):
        self.error_code = error_code
        self.error_desc = error_desc
        self.status_code = status_code

    def to_dict(self):
        return {
            'error_code': self.error_code,
            'error_desc': self.error_desc,
        }


class NifRequiredError(BaseError):
    pass


class InvalidNifError(BaseError):
    pass


class Voter:
    def __init__(self, nif, district, section, table, school, address):
        self.nif = nif
        self.district = district
        self.section = section
        self.table = table
        self.school = school
        self.address = address

    def to_dict(self):
        return {
            'nif': self.nif,
            'district': self.district,
            'section': self.section,
            'table': self.table,
            'school': self.school,
            'address': self.address,
        }

    @classmethod
    def from_li_items(cls, nif, li_items):
        def _extract_number(li):
            regex = compile('(\d+)')
            text = li.text
            res = regex.search(text)
            return int(res.group(1).strip()) if res else None

        def _extract_string(li):
            regex = compile('(.*):(.*)')
            text = li.text
            res = regex.search(text)
            return res.group(2).strip() if res else None

        li_district, li_section, li_table, li_school, li_address = li_items

        district = _extract_number(li_district)
        section = _extract_number(li_section)
        table = _extract_string(li_table)
        school = _extract_string(li_school)
        address = _extract_string(li_address)

        return cls(nif, district, section, table, school, address)


class ElectoralCensus:

    BASE_URL = 'https://cens.palma.cat'
    URL = '{base}/portal/PALMA/cens/cens_principal1.jsp?codResi=1'.format(base=BASE_URL)

    DEFAULT_PARAMS = {
        'form_name': 'formcenso',
        'seccion': 'Consulta.jsp',
    }

    DEFAULT_HEADERS = {
        'Origin': BASE_URL,
        'Referer': URL,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.8',

    }

    @classmethod
    def find_by_nif(cls, nif):

        if not nif:
            raise NifRequiredError('bad_request', 'El camp NIF és obligatori', 400)

        soup = cls.get_soup(nif)

        if soup.find('table', {'id': 'formcenso-errors'}):
            error_desc = 'El NIF {} és invàlid'.format(nif)
            raise InvalidNifError('not_found', error_desc, 404)

        ul = soup.find('div', {'id': 'mesaInfo'})
        li_items = ul.find_all('li')

        voter = Voter.from_li_items(nif, li_items)

        return voter

    @classmethod
    def get_soup(cls, nif):
        url_params = copy(cls.DEFAULT_PARAMS)
        url_params.update({
            'nifPersona': nif,
        })

        response = requests.post(cls.URL, params=url_params, headers=cls.DEFAULT_HEADERS)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        return soup