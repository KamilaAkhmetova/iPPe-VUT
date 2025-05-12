from __future__ import annotations
from Operation import Operation, Parsing_Error, Run_Time_Error_6
import xml.etree.ElementTree as xml

class Return(Operation):
    def __init__(self, operation: xml.Element, call_stack_return):
        super().__init__(operation)
        self.call_stack_return = call_stack_return
        if len(list(operation)) > 0:
            raise Parsing_Error
        self._check_structure()

    def _check_structure(self):
        pass

    def execute(self):
        if not self.call_return_stack:
            raise Run_Time_Error_6
        return int(self.call_return_stack.pop())
