import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def detelefoongids_company_soup_snippet():
    html_snippet = """
        <div class="resultItem active wrapper" itemscope="" itemtype="http://schema.org/LocalBusiness">
            <div class="business-card wrapper">
                <div class="business-card__container wrapper">
                    <div class="business-card__metadata">
                        <div class="business-card__metadata--header"><p class="index">1.</p>
                            <h2 id="17250935"><span><a href="https://www.detelefoongids.nl/dacom-bv/17250935/5-1/"
                                                       target="_blank" title="Dacom BV"><span
                                    itemprop="name">Dacom BV</span></a></span></h2></div>
                        <p class="category"><!-- react-text: 632 --><!-- /react-text --><span class="category">Computersoftware</span>
                            <!-- react-text: 634 --><!-- /react-text --></p>
                        <div class="business-card__metadata--info wrapper grid">
                            <div><p class="address" itemprop="address" itemscope=""
                                    itemtype="http://schema.org/PostalAddress"><span itemprop="streetAddress"><!-- react-text: 639 -->Waanderweg
                                <!-- /react-text --><!-- react-text: 640 --> <!-- /react-text --><!-- react-text: 641 -->68
                                <!-- /react-text --></span><!-- react-text: 642 -->, <!-- /react-text --><span
                                    itemprop="postalCode">7812HZ</span><span><span>, </span><span itemprop="addressLocality"
                                                                                                  class="strong"><span><!-- react-text: 648 -->
                                <!-- /react-text --><span></span><!-- react-text: 650 -->Emmen
                                <!-- /react-text --></span></span></span></p></div><!-- react-empty: 651 --></div>
                        <div class="business-card__buttons margin-top">
                            <div class="buttons wrapper grid grid--gutter-0"><a class="button phone"
                                                                                href="https://www.detelefoongids.nl/dacom-bv/17250935/5-1/?sn=17250935"
                                                                                target="_blank"><span class="hidden">https://www.detelefoongids.nl/dacom-bv/17250935/5-1/?sn=17250935</span><span
                                    class="hidden" itemprop="telephone">088-3226600</span><!-- react-text: 657 -->Toon
                                nummer<!-- /react-text --></a><a class="button website" href="http://www.dacom.nl"
                                                                 target="_blank" title="Dacom BV" itemprop="url"
                                                                 rel="nofollow" data-listingid="17250935">Website</a><a
                                    class="button route route-inline"
                                    href="https://google.com/maps?saddr=Current+Location&amp;daddr=52.752641,6.878647&amp;amp;"
                                    target="_blank" rel="nofollow">Plan route</a><a class="button kvk"
                                                                                    href="https://www.kvk.nl/orderstraat/bedrijf-kiezen/?q=04041685#!shop?&amp;q=04041685&amp;start=0&amp;prefproduct=&amp;prefpayment="
                                                                                    target="_blank" rel="nofollow">KvK-gegevens</a>
                                <!-- react-empty: 661 --></div>
                        </div>
                    </div>
                    <div class="business-card__extra"><a class="reviewScore reviewLine"
                                                         href="https://www.detelefoongids.nl/dacom-bv/17250935/5-1/?goTo=review-toevoegen"
                                                         target="_blank" title="Review toevoegen voor Dacom BV">Beoordeel
                        dit bedrijf</a><!-- react-empty: 664 --></div>
                </div>
            </div>
        </div>
    """
    return BeautifulSoup(html_snippet, 'html.parser')
