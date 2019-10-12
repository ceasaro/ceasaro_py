import requests
from bs4 import BeautifulSoup

# VOORBEELD URL:
# https://zoeken.kvk.nl/search.ashx?handelsnaam=&kvknummer=&straat=&postcode=9635AT&huisnummer=&plaats=&hoofdvestiging=1&rechtspersoon=1&nevenvestiging=1&zoekvervallen=0&zoekuitgeschreven=1&start=0&searchfield=uitgebreidzoeken&_=1565523624456
from SAS.models import Company, SasManager

KVK_SEARCH_URL = 'https://zoeken.kvk.nl/search.ashx?'
KVK_SEARCH_PARAMS = {
    'handelsnaam': '',
    'kvknummer': '',
    'straat': '',
    'postcode': '',
    'huisnummer': '',
    'plaats': 'Noordbroek',
    'hoofdvestiging': 1,
    'rechtspersoon': 1,
    'nevenvestiging': 1,
    'zoekvervallen': 0,
    'zoekuitgeschreven': 1,
    'start': 0,
    'searchfield': 'uitgebreidzoeken',
    '_': '1565523624456'
}


def parse_html_kvk_company(bs4_company):
    """
        <li class="type1">
            <div class="handelsnaamHeaderWrapper">
                <h3 class="handelsnaamHeader">
                    <a href="/orderstraat/product-kiezen/?kvknummer=539115630000">J.C. Vermue en R.J. Vermue</a>
                </h3>
                <A href="/orderstraat/product-kiezen/?kvknummer=539115630000"
                   class="hoofdvestigingTag">Hoofdvestiging</A>
            </div>
            <div class="more-search-info">
                <h4>Bestaande handelsnamen</h4>
                <p>J.C. Vermue en R.J. Vermue | Agrarische Dienstverlening J.C. Vermue en R.J. Vermue</p>
                <h4>Naam samenwerkingsverband</h4>
                <p>Stille maatschap tussen J.C. Vermue en R.J. Vermue</p>
            </div>
            <div class="content">
                <ul class="kvk-meta">
                    <li>KVK 53911563</li>
                    <li>Vestigingsnr. 000023754427</li>
                    <li>Hoofdstraat 67</li>
                    <li>9635AT</li>
                    <li>Noordbroek</li>
                    <li></li>
                </ul>
            </div>
            <p class="snippet-result">53911563 0000 000023754427 J.C. Vermue en R.J. Vermue Stille maatschap tussen J.C.
                Vermue en R.J. Vermue Stille mts. J.C. Vermue & R.J. <b>9635AT</b> <b>...</b>
            </p>
            <p class="section">
                <span class="cta"><a href="/orderstraat/product-kiezen/?kvknummer=539115630000">Bestel nu</a></span>
            </p>
        </li>
    :return:
    """
    more_search_info = bs4_company.find('div', class_='more-search-info')
    if more_search_info:
        existing_trade_name_header = more_search_info.find('h4', string='Bestaande handelsnamen')
        existing_trade_name = existing_trade_name_header.find_next('p').text
        kvk_meta = bs4_company.find('ul', class_='kvk-meta')
        kvk_meta_items = kvk_meta.find_all('li') if kvk_meta else []
        len_kvk_meta = len(kvk_meta_items)
        if kvk_meta_items:
            KVK_nr = kvk_meta_items[0].text
            if KVK_nr:
                KVK_nr = KVK_nr[len('KVK '):]  # strip off prefix
            vestiging_nr = kvk_meta_items[1].text if len_kvk_meta >= 1 else None
            if vestiging_nr:
                vestiging_nr = vestiging_nr[len('Vestigingsnr. '):]  # strip off prefix
            street = kvk_meta_items[2].text if len_kvk_meta >= 2 else None
            zipcode = kvk_meta_items[3].text if len_kvk_meta >= 3 else None
            city = kvk_meta_items[4].text if len_kvk_meta >= 4 else None
            return Company(kvk=KVK_nr, name=existing_trade_name, vestiging_nr=vestiging_nr, street=street,
                           zip_code=zipcode, city=city)


def search_kvk():
    companies = []
    resp = requests.get(KVK_SEARCH_URL, KVK_SEARCH_PARAMS)
    soup = BeautifulSoup(resp.content, 'html.parser')
    result_list = soup.find('ul', class_='results')
    for company_html in result_list.findChildren('li', recursive=False):
        company = parse_html_kvk_company(company_html)
        if company:
            companies.append(company)
    return companies
