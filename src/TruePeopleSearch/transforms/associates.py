from canari.framework import EnableDebugWindow
from canari.maltego.transform import Transform

from .common.entities import TruePerson
from .common.scrapper import scrape

__author__ = 'thehappydinoa'
__copyright__ = 'Copyright 2018, TruePeopleSearch Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'thehappydinoa'
__email__ = 'thehappydinoa@gmail.com'
__status__ = 'Development'


class Associates(Transform):
    """Gathers associates from TruePeopleSearch"""
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
            associates = soup.find_all(
                attrs={"data-link-to-more": "associate"})
            for associate in associates:
                response += TruePerson(associate.get_text(),
                                       properties_url=config['TruePeopleSearch.local.base_url'] + associate['href'])

        return response

    def on_terminate(self):
        pass
