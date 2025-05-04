from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error
import re
import parser3
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from taci import Interpreter 


class Label(Operation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self.dst: xml.Element = None
        self.order: str = operation.get('order')
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        
        if self.dst is None:
            raise Parsing_Error
            
        if self.dst.get('type') != 'label':
            raise Semantic_Error
            
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Semantic_Error

    def execute(self, interpreter: Interpreter) -> None:
       
        if not self.order.isdigit():
            raise Semantic_Error
            
        label_name = self.dst.text
        label_position = int(self.order) - 1
        
        if label_name in interpreter.labels:
            raise Semantic_Error
            
        interpreter.labels[label_name] = label_position
