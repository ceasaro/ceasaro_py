#!/home/cees/.virtualenvs/ceasaro_py/bin/python
import os
import sys

# add the parent dir of this script to the python path
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

from SAS.scrape.kvk_scrape import search_kvk
from SAS.scrape.detelefoongids_scrape import TelefoonGids
from SAS.models import SasManager, Company


# VOORBEELD URL:
# https://zoeken.kvk.nl/search.ashx?handelsnaam=&kvknummer=&straat=&postcode=9635AT&huisnummer=&plaats=&hoofdvestiging=1&rechtspersoon=1&nevenvestiging=1&zoekvervallen=0&zoekuitgeschreven=1&start=0&searchfield=uitgebreidzoeken&_=1565523624456


def main(prog_args):
    sas_manager = SasManager()
    telefoon_gids = TelefoonGids()

    companies = []
    # companies += search_kvk()
    companies.append(Company(name='Dacom', zip_code='7812HZ'))
    for company in companies:
        telefoon_gids.complement(company)
    sas_manager.add_companies(companies)
    sas_manager.save()


if __name__ == '__main__':
    sys.exit(main(sys.argv))
