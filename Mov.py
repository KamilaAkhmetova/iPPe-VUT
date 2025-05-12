from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error
import re
import parser3
import xml.etree.ElementTree as xml

class Mov(Operation):
    def __init__(self, operation: xml.Element, variables):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.variables = variables 
        self._check_structure()

    def _check_structure(self) -> None:
        if self.dst is None or self.src1 is None:
            raise Parsing_Error 
        if self.dst.get('type') != 'variable':
            raise Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Semantic_Error
        if self.src1.get('type') not in ['integer', 'string', 'variable']:
            raise Semantic_Error
        if self.src1.get('type') == 'integer' and not parser3.type_check_int(self.src1.text):
            raise Semantic_Error
        elif self.src1.get('type') == 'variable' and not re.fullmatch(parser3.var, self.src1.text):
            raise RuntimeError
        
    def execute(self):
        value = None
        if self.src1.get('type') == 'integer':
            value = int(self.src1.text)
        elif self.src1.get('type') == 'string':
            value = self.src1.text
        elif self.src1.get('type') == 'variable':
            if self.src1.text in self.variables:
                value = self.variables[self.src1.text]
            else:
                raise RuntimeError
        self.variables[self.dst.text] = value
