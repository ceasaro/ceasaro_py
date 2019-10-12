import requests
from bs4 import BeautifulSoup
from bunch import Bunch

from SAS.scrape.base import Scrapper


class TelefoonGids(Scrapper):
    DOMAIN = 'https://www.detelefoongids.nl'

    def parse_html_company(self, soup4_element):
        """
            <div class="resultItem active wrapper" itemscope="" itemtype="http://schema.org/LocalBusiness">
                <div class="business-card wrapper">
                    <div class="business-card__container wrapper">
                        <div class="business-card__metadata">
                            <div class="business-card__metadata--header">
                                <p class="index">1.</p>
                                <h2 id="17250935">
                                    <span>
                                        <a href="https://www.detelefoongids.nl/dacom-bv/17250935/5-1/" target="_blank"
                                           title="Dacom BV">
                                            <span itemprop="name">Dacom BV</span>
                                        </a>
                                    </span>
                                </h2>
                            </div>
                            <p class="category"><!-- react-text: 632 --><!-- /react-text -->
                                <span class="category">Computersoftware</span>
                                <!-- react-text: 634 --><!-- /react-text -->
                            </p>
                            <div class="business-card__metadata--info wrapper grid">
                                <div>
                                    <p class="address" itemprop="address" itemscope=""
                                       itemtype="http://schema.org/PostalAddress">
                                        <span itemprop="streetAddress"><!-- react-text: 639 -->Waanderweg
                                            <!-- /react-text --><!-- react-text: 640 --> <!-- /react-text -->
                                            <!-- react-text: 641 -->68
                                            <!-- /react-text -->
                                        </span><!-- react-text: 642 -->, <!-- /react-text -->
                                        <span itemprop="postalCode">7812HZ</span>
                                        <span><span>, </span><span itemprop="addressLocality" class="strong"><span><!-- react-text: 648 -->
                                            <!-- /react-text --><span></span><!-- react-text: 650 -->Emmen
                                            <!-- /react-text --></span>
                                        </span></span>
                                    </p>
                                </div><!-- react-empty: 651 -->
                            </div>
                            <div class="business-card__buttons margin-top">
                                <div class="buttons wrapper grid grid--gutter-0">
                                    <a class="button phone"
                                       href="https://www.detelefoongids.nl/dacom-bv/17250935/5-1/?sn=17250935" target="_blank">
                                        <span class="hidden">https://www.detelefoongids.nl/dacom-bv/17250935/5-1/?sn=17250935</span>
                                        <span class="hidden" itemprop="telephone">088-3226600</span><!-- react-text: 657 -->Toon
                                        nummer<!-- /react-text -->
                                    </a>
                                    <a class="button website" href="http://www.dacom.nl" target="_blank" title="Dacom BV"
                                       itemprop="url" rel="nofollow" data-listingid="17250935">Website</a>
                                    <a class="button route route-inline"
                                       href="https://google.com/maps?saddr=Current+Location&amp;daddr=52.752641,6.878647&amp;amp;"
                                       target="_blank" rel="nofollow">Plan route</a>
                                    <a class="button kvk"
                                       href="https://www.kvk.nl/orderstraat/bedrijf-kiezen/?q=04041685#!shop?&amp;q=04041685&amp;start=0&amp;prefproduct=&amp;prefpayment="
                                       target="_blank" rel="nofollow">KvK-gegevens</a>
                                    <!-- react-empty: 661 -->
                                </div>
                            </div>
                        </div>
                        <div class="business-card__extra">
                            <a class="reviewScore reviewLine"
                               href="https://www.detelefoongids.nl/dacom-bv/17250935/5-1/?goTo=review-toevoegen"
                               target="_blank" title="Review toevoegen voor Dacom BV">Beoordeel dit bedrijf
                            </a><!-- react-empty: 664 --></div>
                    </div>
                </div>
            </div>
        :return: a dict with the search results.
        """
        if soup4_element:
            company = Bunch()
            company.name = self.get_text(soup4_element, [('h2', {}), ('span', {'itemprop': 'name'})])
            company.category = self.get_text(soup4_element, [('span', {'class': 'category'})])
            address = soup4_element.find('p', {'class': 'address'})
            company.street = self.get_text(address, [('span', {'itemprop': 'streetAddress'})])
            company.zip_code = self.get_text(address, [('span', {'itemprop': 'postalCode'})])
            company.city = self.get_text(address, [('span', {'itemprop': 'addressLocality'})])
            business_card_buttons = soup4_element.find('div', {'class': 'business-card__buttons'})
            company.phone = self.get_text(business_card_buttons, [
                ('a', {'class': 'phone'}),
                ('span', {'itemprop': 'telephone'})])
            company.website = business_card_buttons.find('a', {'class': 'website'}).get('href')
            return company

    def search(self, name, zip_code=None, city=None):
        """
        https://www.detelefoongids.nl/dacom/emmen/3-1/
        https://www.detelefoongids.nl/dacom/4-1/
        :param name: the company name
        :param zip_code: the companies zip code (works better for searching than city
        :param city: the city where the companies resides, use zip_code if you have one.
        :return:
        """
        if zip_code or city:
            search_url = '{domain}/{name}/{zip_code}/3-1/'.format(domain=self.DOMAIN, name=name,
                                                                  zip_code=zip_code or city)
        else:
            search_url = '{domain}/{name}/4-1/'.format(domain=self.DOMAIN, name=name)
        resp = requests.get(search_url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        import pdb; pdb.set_trace()
        return self.parse_html_company(soup.find_all('div', {'class': 'resultItem'}))

    def complement(self, company):
        print("searching telefoon gids for {}, {} , {}".format(company.name, company.zip_code, company.city))
        result = self.search(company.name, company.zip_code, company.city)
        print("search result: {}".format(result))
        if result:
            company.website = result.website
            company.phone = result.phone
        return company
