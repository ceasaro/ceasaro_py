import os

from SAS.google_api_client import Client as GoogleClient


class SasException(Exception):
    pass


class SasManager(object):
    HEADER_ROW = ['kvk', 'name', 'vestiging nr', 'street', 'zip code', 'city', 'email', 'phone', 'website', 'status']

    def __init__(self, companies=None):
        self.companies = companies or []
        self.raw_sas_data = None
        self.google_client = GoogleClient(
            os.environ['GOOGLE_DRIVE_CLIENT_ID'],
            os.environ['GOOGLE_DRIVE_CLIENT_SECRET'],
            os.environ['TEST_SAS_COMPANIES_DRIVE_FILE_ID'])
        self.load()

    def add_company(self, company):
        for i, c in enumerate(self.companies):
            if c == company:
                self.companies[i] = company
                return False
        self.companies.append(company)
        return True

    def _to_google_values(self):
        data = [c.to_google_spreadsheet_row() for c in self.companies]
        data.insert(0, self.HEADER_ROW)
        return data

    def _from_google_values(self, google_data):
        header_row = google_data.pop(0)
        if header_row != self.HEADER_ROW:
            raise SasException("Spreadsheet header differs from expected header, can't load data. {} != {}.".format(header_row, self.HEADER_ROW))
        for row in google_data:
            self.companies.append(Company.create(row))

    def save(self):
        self.google_client.store_sas_file(self._to_google_values())

    def load(self, overwrite=False):
        if self.raw_sas_data and not overwrite:
            raise SasException("sas data already loaded from google, use the 'overwrite' parameter to load anyway")
        self.raw_sas_data = self.google_client.get_sas_file()
        self._from_google_values(self.raw_sas_data)
        return self.companies

    def add_companies(self, companies):
        for c in companies:
            self.add_company(c)


class Company(object):

    def __init__(self, kvk=None, name=None, vestiging_nr=None, street=None, zip_code=None,
                 city=None, email=None, phone=None, website=None, status='NEW') -> None:
        self.kvk = kvk
        self.name = name
        self.vestiging_nr = vestiging_nr
        self.street = street
        self.zip_code = zip_code
        self.city = city
        self.email = email
        self.phone = phone
        self.website = website
        self.status = status

    @classmethod
    def create(cls, google_row):
        return Company(kvk=google_row[SasManager.HEADER_ROW.index('kvk')],
                       name=google_row[SasManager.HEADER_ROW.index('name')],
                       vestiging_nr=google_row[SasManager.HEADER_ROW.index('vestiging nr')],
                       street=google_row[SasManager.HEADER_ROW.index('street')],
                       zip_code=google_row[SasManager.HEADER_ROW.index('zip code')],
                       city=google_row[SasManager.HEADER_ROW.index('city')],
                       email=google_row[SasManager.HEADER_ROW.index('email')],
                       phone=google_row[SasManager.HEADER_ROW.index('phone')],
                       website=google_row[SasManager.HEADER_ROW.index('website')],
                       status=google_row[SasManager.HEADER_ROW.index('status')]
                       )

    def to_google_spreadsheet_row(self):
        return [self.kvk, self.name, self.vestiging_nr, self.street, self.zip_code, self.city, self.email, self.phone,
                self.website, self.status]

    def __eq__(self, other_kvk) -> bool:
        return self.kvk == other_kvk.kvk

    def __str__(self) -> str:
        return "<{}: {}>".format(self.__class__.__name__, self.kvk)

    def __repr__(self) -> str:
        return self.__str__()
