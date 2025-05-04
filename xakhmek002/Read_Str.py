from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error, Other_Errors
import re
import parser3
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from taci import Interpreter 
class Read_Str(Operation):
    def __init__(self, operation: xml.Element, interpreter: Interpreter):
        super().__init__(operation)
        self.interpreter = interpreter
        self.dst: xml.Element = None
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        
        if self.dst is None:
            raise Parsing_Error
            
        if self.dst.get('type') != 'variable':
            raise Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Semantic_Error
    def execute(self) -> None:
        try:
            value = self.interpreter.read_next_str()
            self.interpreter.variables[self.dst.text] = value
        except Exception as e:
            raise Other_Errors
