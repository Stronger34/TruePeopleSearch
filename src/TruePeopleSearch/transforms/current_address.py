from canari.framework import EnableDebugWindow
from canari.maltego.entities import Location
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


class CurrentAddress(Transform):
    """Gathers current address from TruePeopleSearch"""
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
            addresses = soup.find_all(
                attrs={"data-link-to-more": "address"})
            if addresses:
                address = addresses[0].get_text().split(" ")
                address[-1] = address[-1].split("-")[0]
                response += Location(" ".join(address))

        return response

    def on_terminate(self):
        pass
