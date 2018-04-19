import json
import os

import requests

from libero_flow.activities.base_activity import BaseActivity


class DownloadArticleXMLActivity(BaseActivity):

    def do_activity(self) -> str:
        """Download some article xml and store in a public location

        :return: str
        """

        input_data = self.session_get('input_data')

        if input_data:
            input_data = json.loads(input_data)
            data_dir = input_data.get('data_dir')
            file_urls = input_data.get('urls')

            if not os.path.isdir(data_dir):
                os.mkdir(data_dir)

            if file_urls:
                for url in file_urls:
                    response = requests.get(url=url)

                    file_name = url.split('/')[-1]

                    with open(os.path.join(data_dir, file_name), 'w') as xml_file:
                        xml_file.write(response.text)

                return self.SUCCEEDED

        return self.PERMANENT_FAILURE
