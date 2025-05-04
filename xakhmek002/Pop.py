from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import re
import parser3
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from taci import Interpreter

class Pop(ClassOperation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self.dst: xml.Element = None
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        if self.dst is None:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'variable':
            raise Operation.Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self, interpreter: Interpreter) -> None:
       
        if self.dst.text not in interpreter.variables:
            raise Operation.Semantic_Error
            
        interpreter.data_stack.append(interpreter.variables[self.dst.text])
