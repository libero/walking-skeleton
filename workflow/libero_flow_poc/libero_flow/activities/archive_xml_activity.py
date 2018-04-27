import time

from libero_flow.activities.base_activity import BaseActivity


class ArchiveXMLActivity(BaseActivity):
    """
    **complete**
    """
    def do_activity(self):
        """

        :return:
        """
        print(self.__class__)
        # simulate some work
        xml_path = self.session_get('cloned_xml_path')
        self.session_set('archived_xml_path', f'foo {xml_path}')
        time.sleep(5)

        return self.SUCCEEDED
