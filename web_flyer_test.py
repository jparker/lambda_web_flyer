# -*- coding: utf-8 -*-

import unittest
import httpretty
import vcr
from web_flyer import WebFlyer, AmbiguousAirport, InvalidAirport, WebFlyerExternalError

class WebFlyerTest(unittest.TestCase):
    def test_route(self):
        api = WebFlyer(origin='san', destination='pdx')
        self.assertEqual(('SAN', 'PDX'), api.route)
        self.assertEqual(
            'http://www.webflyer.com' \
            '/travel/mileage_calculator/getmileage.php' \
            '?city=SAN&city=PDX',
            api.endpoint
        )

    @vcr.use_cassette('vcr_cassettes/san-pdx.yml')
    def test_san_pdx(self):
        api = WebFlyer(origin='SAN', destination='PDX')
        self.assertEqual(933, api.miles)

    @vcr.use_cassette('vcr_cassettes/sfo-san.yml')
    def test_sfo_san(self):
        api = WebFlyer(origin='SFO', destination='SAN')
        self.assertEqual(447, api.miles)

    @vcr.use_cassette('vcr_cassettes/san-nrt.yml')
    def test_sfo_san(self):
        api = WebFlyer(origin='SAN', destination='NRT')
        self.assertEqual(5540, api.miles)

    @vcr.use_cassette('vcr_cassettes/san-xxx.yml')
    def test_invalid_airport(self):
        with self.assertRaises(InvalidAirport) as cm:
            api = WebFlyer(origin='SAN', destination='XXX')
            api.miles
        self.assertEqual('Invalid airport code: XXX', cm.exception.msg)

    @vcr.use_cassette('vcr_cassettes/san-l.yml')
    def test_ambiguous_airport(self):
        with self.assertRaises(AmbiguousAirport) as cm:
            api = WebFlyer(origin='SAN', destination='L')
            api.miles
        self.assertEqual('Ambiguous airport code: L', cm.exception.msg)

    @httpretty.activate
    def test_server_error(self):
        httpretty.register_uri(
            httpretty.GET,
            'http://www.webflyer.com/travel/mileage_calculator/getmileage.php',
            body='Internal Server Error',
            status=500,
        )
        with self.assertRaises(WebFlyerExternalError) as cm:
            api = WebFlyer(origin='SAN', destination='PDX')
            api.miles
        self.assertEqual(500, cm.exception.response.status_code)
