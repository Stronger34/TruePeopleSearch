from canari.framework import EnableDebugWindow
from canari.maltego.entities import EmailAddress, Location, PhoneNumber
from canari.maltego.transform import Transform

from .common.entities import TruePerson
from .common.scrapper import scrape

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.2'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'


class FullSearch(Transform):
    """Gathers all information from TruePeopleSearch"""
    input_type = TruePerson

    def do_transform(self, request, response, config):
        person = request.entity
        fields = person.fields

        if fields.get("properties.url"):
            url = fields.get("properties.url").value
        else:
            url = None

        soup = scrape(url)

        if soup:
            email_addresses = soup.find_all(attrs={"class": "__cf_email__"})
            for email_address in email_addresses:
                fp = email_address['data-cfemail']
                r = int(fp[:2], 16)
                email = ''.join([chr(int(fp[i:i + 2], 16) ^ r)
                                 for i in range(2, len(fp), 2)])
                response += EmailAddress(email)

            phone_numbers = soup.find_all(attrs={"data-link-to-more": "phone"})
            for phone_number in phone_numbers:
                response += PhoneNumber(phone_number.get_text())

            addresses = soup.find_all(attrs={"data-link-to-more": "address"})
            for unformated_address in addresses:
                address = unformated_address.get_text().split(" ")
                address[-1] = address[-1].split("-")[0]
                response += Location(" ".join(address))

            relatives = soup.find_all(attrs={"data-link-to-more": "relative"})
            for relative in relatives:
                response += TruePerson(relative.get_text(),
                                       properties_url=config['TruePeopleSearch.local.base_url'] + relative['href'])

            associates = soup.find_all(
                attrs={"data-link-to-more": "associate"})
            for associate in associates:
                response += TruePerson(associate.get_text(),
                                       properties_url=config['TruePeopleSearch.local.base_url'] + associate['href'])

        return response

    def on_terminate(self):
        pass
