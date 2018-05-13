# -*- coding: utf-8 -*-

from lxml import html
from urllib.parse import urlencode, urlunparse
import requests
import re

class WebFlyerError(Exception):
    def __init__(self, msg):
        self.msg = msg

class WebFlyerInternalError(WebFlyerError):
    pass

class AmbiguousAirport(WebFlyerInternalError):
    pass

class InvalidAirport(WebFlyerInternalError):
    pass

class WebFlyerExternalError(WebFlyerError):
    def __init__(self, response):
        self.msg = 'Server sent error response: %s' % response.reason
        self.response = response

class WebFlyer:
    def __init__(self, origin, destination):
        self.origin = origin.upper()
        self.destination = destination.upper()
        self._tree       = None

    @property
    def route(self):
        return self.origin, self.destination

    @property
    def miles(self):
        node = self.tree.find('.//td[.="Distance"]/../td[2]')
        text = node.text_content()
        mileage = int(re.search(r'[0-9]+', text)[0])
        return mileage

    @property
    def tree(self):
        if self._tree is None:
            self._tree = html.fromstring(self.__data())
        return self._tree

    def __data(self):
        response = requests.get(self.endpoint)
        if not response.ok:
            raise WebFlyerExternalError(response=response)

        match = re.search(r'<b>(.*?)</b> has multiple matches', response.text)
        if match:
            raise AmbiguousAirport(msg='Ambiguous airport code: %s' % match.group(1))

        match = re.search(r'"<b>(.*?)</b>" was not found', response.text)
        if match:
            raise InvalidAirport(msg='Invalid airport code: %s' % match.group(1))

        return response.content

    @property
    def endpoint(self):
        return urlunparse((
            'http',
            'www.webflyer.com',
            '/travel/mileage_calculator/getmileage.php',
            '',
            urlencode([('city', self.origin), ('city', self.destination)]),
            ''
        ))
