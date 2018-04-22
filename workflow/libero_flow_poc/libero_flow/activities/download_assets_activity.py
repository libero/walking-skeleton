import json
import os
import time

import requests

from libero_flow.activities.base_activity import BaseActivity


class DownloadAssetsActivity(BaseActivity):

    def do_activity(self) -> str:
        """Download some static assets.

        :return: str
        """

        time.sleep(5)

        input_data = self.session_get('input_data')
        uris = self.session_get('uris')

        if input_data and uris:
            input_data = json.loads(input_data)
            data_dir = input_data.get('data_dir')

            uris = json.loads(uris.replace("'", '"'))

            for uri in uris['uris']:
                response = requests.get(url=uri)

                file_name = uri.split('/')[-1]

                with open(os.path.join(data_dir, file_name), 'wb') as asset_file:
                    asset_file.write(response.content)

            return self.SUCCEEDED

        return self.PERMANENT_FAILURE
