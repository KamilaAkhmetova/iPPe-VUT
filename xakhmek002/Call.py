# current order!!
from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import re
import parser3
from typing import TYPE_CHECKING
import xml.etree.ElementTree

if TYPE_CHECKING:
    from taci import Interpreter  

class Call(ClassOperation):
    def __init__(self, operation: xml.etree.ElementTree.Element):
        super().__init__(operation)
        self._check_structure(operation)
        self.order = operation.get('order')

    def _check_structure(self, operation: xml.etree.ElementTree.Element) -> None:
        self.dst = operation.find('dst')
        
        if self.dst is None:
            raise Operation.Parsing_Error
            
        if self.dst.get('type') != 'label':
            raise Operation.Semantic_Error
            
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self, interpreter: Interpreter) -> None:
        if self.dst.text not in interpreter.labels:
            raise Operation.Run_Time_Error_1
            
        interpreter.call_return_stack.append(self.order)
        
        interpreter.current_order = interpreter.labels[self.dst.text]
