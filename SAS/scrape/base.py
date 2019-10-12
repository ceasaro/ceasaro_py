import re

from bs4 import Comment


class Scrapper(object):

    def parse_html_company(self, soup4_element):
        """
        :param soup4_element: a beautiful soup object contains a company html snippet
        :return: dict
        """
        raise NotImplemented()

    def find_companies(self, search_keys=None):
        raise NotImplemented()

    def search(self, *args, **kwargs):
        raise NotImplemented()

    def complement(self, company):
        raise NotImplemented()

    def get_text(self, soup4_element, search_arg_list=None):
        if not soup4_element:
            return
        if not search_arg_list:
            for element in soup4_element(text=lambda text: isinstance(text, Comment)):
                element.extract()
            return re.sub('\s+', ' ', soup4_element.getText()).strip()
        else:
            search_args = search_arg_list[0]
            tag_name = search_args[0] if search_args else ''
            kwargs = search_args[1] if len(search_args) > 0 else {}
            return self.get_text(soup4_element.find(tag_name, **kwargs), search_arg_list=search_arg_list[1:])
