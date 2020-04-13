import re
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from census.entities import Voter, CensusInformation, School
from census.errors import InvalidNif


class Parser(ABC):

    @abstractmethod
    def parse_response(self, response) -> Voter:
        pass


class Palma(Parser):

    def parse_response(self, context, response) -> Voter:
        soup = BeautifulSoup(response, 'html.parser')

        self._assert_nif_is_valid(soup)

        info = soup.find('div', {'id': 'mesaInfo'})
        li_items = info.find_all('li')
        li_district, li_section, li_table, li_school, li_address = li_items

        census_information = CensusInformation(
            self._extract_value(li_district.text),
            self._extract_value(li_section.text),
            self._extract_value(li_table.text)
        )

        school = School(
            self._extract_value(li_school.text),
            self._extract_value(li_address.text)
        )

        return Voter(context.nif, census_information, school)

    def _assert_nif_is_valid(self, soup):
        if soup.find('table', {'id' : 'formcenso-errors'}):
            raise InvalidNif()

    def _extract_value(self, text) -> str:
        regex = re.compile('(.*): (.*)')
        match = regex.search(text)
        return match.group(2).strip() if match else None
