from SAS.scrape.detelefoongids_scrape import TelefoonGids


def test_parse_html(detelefoongids_company_soup_snippet):
    telefoon_gids = TelefoonGids()
    result = telefoon_gids.parse_html_company(detelefoongids_company_soup_snippet)
    assert result.name == 'Dacom BV'
    assert result.category == 'Computersoftware'
    assert result.phone == '088-3226600'
    assert result.website == 'http://www.dacom.nl'
    assert result.street == 'Waanderweg 68'
    assert result.zip_code == '7812HZ'
    assert result.city == 'Emmen'
