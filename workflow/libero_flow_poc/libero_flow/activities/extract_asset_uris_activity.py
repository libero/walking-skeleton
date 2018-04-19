import json

from bs4 import BeautifulSoup
import requests

from libero_flow.activities.base_activity import BaseActivity


class ExtractAssetURIsActivity(BaseActivity):

    def do_activity(self) -> str:
        """Download some article xml and extract asset URIs from XML.

        :return: str
        """

        input_data = self.session_get('input_data')

        if input_data:
            input_data = json.loads(input_data)
            file_urls = input_data.get('urls')

            uris = []

            if file_urls:
                for url in file_urls:
                    response = requests.get(url=url)
                    xml = BeautifulSoup(response.text, 'lxml-xml')
                    uris += [var.contents[0] for var in xml.find_all('source')
                             if var.attrs['media-type'] == 'image/tiff']

                self.session_set('uris', {'uris': uris})

                return self.SUCCEEDED

        return self.PERMANENT_FAILURE
