"""
Provides a convenience utility for loading workflow definitions and activity classes
"""

import os
import json
from typing import Dict


# TODO needs to be set by config
WORKFLOWS_DIR = os.path.join(os.path.dirname(__file__), 'workflows')


class FlowLoader:

    _workflow_map = {}

    def __init__(self):
        pass

    def get_activity(self, name):
        pass

    def get_workflow(self, name):
        return self.workflow_map.get(name, None)

    @property
    def workflow_map(self) -> Dict[str, Dict]:
        if not self._workflow_map:
            workflow_def_files = os.listdir(WORKFLOWS_DIR)

            for def_file in workflow_def_files:
                with open(os.path.join(WORKFLOWS_DIR, def_file)) as file_obj:
                    definition = json.load(file_obj)
                self._workflow_map[definition.get('name')] = definition

        return self._workflow_map
