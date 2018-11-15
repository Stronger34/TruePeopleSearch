from canari.framework import EnableDebugWindow
from canari.maltego.entities import PhoneNumber
from canari.maltego.transform import Transform

from .common.entities import TruePerson

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'


class PhoneNumbers(Transform):
    """Gathers phone numbers from TruePeopleSearch"""
    input_type = TruePerson

    def do_transform(self, request, response, config):
        person = request.entity
        fields = person.fields

        soup = scrape(fields.get("properties.url"))

        if soup:
            phone_numbers = soup.find_all(attrs={"data-link-to-more": "phone"})
            for phone_number in phone_numbers:
                response += PhoneNumber(phone_number.get_text())

        return response

    def on_terminate(self):
        pass
