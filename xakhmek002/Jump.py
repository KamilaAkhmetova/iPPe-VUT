from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import re
import parser3
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from taci import Interpreter  
class Jump(ClassOperation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self._check_structure(operation)
        self.dst: Optional[xml.Element] = None
    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        if self.dst is None:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'label':
            raise Operation.Semantic_Error
            
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self, interpreter: Interpreter) -> Optional[int]:
        
        if self.dst is None or self.dst.text not in interpreter.labels:
            raise Operation.Run_Time_Error_1
            
        return interpreter.labels[self.dst.text]
