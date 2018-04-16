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
        time.sleep(5)

        return self.SUCCEEDED
