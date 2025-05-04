from __future__ import annotations
from Operation import Operation, Parsing_Error, Run_Time_Error_6
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from taci import Interpreter 


class Return(Operation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        if len(list(operation)) > 0:
            raise Parsing_Error

    def execute(self, interpreter: Interpreter) -> Optional[int]:
        if not interpreter.call_return_stack:
            raise Run_Time_Error_6
        return interpreter.call_return_stack.pop()
