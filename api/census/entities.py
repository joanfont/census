from dataclasses import dataclass


@dataclass
class Context:
    nif: str


@dataclass
class School:
    name: str
    address: str


@dataclass
class CensusInformation:
    district: str
    section: str
    table: str


@dataclass
class Voter:
    nif: str
    census_information: CensusInformation
    school: School

    def to_dict(self):
        return {
            'nif': self.nif,
            'district': self.census_information.district,
            'section': self.census_information.section,
            'table': self.census_information.table,
            'school': self.school.name,
            'address': self.school.address,
        }
