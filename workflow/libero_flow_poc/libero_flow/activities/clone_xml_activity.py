import time

from libero_flow.activities.base_activity import BaseActivity


class CloneXMLActivity(BaseActivity):
    """
    **complete**
    """

    def do_activity(self):
        """

        :return:
        """
        print(self.__class__)
        # simulate some work
        self.session_set('cloned_xml_path', 'foo')
        time.sleep(15)

        return self.SUCCEEDED
