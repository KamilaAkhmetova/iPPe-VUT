from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import re
import parser3
import xml.etree.ElementTree as xml

class Pop(ClassOperation):
    def __init__(self, operation: xml.Element, variables, data_stack):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.variables = variables
        self.data_stack = data_stack
        self._check_structure()

    def _check_structure(self):
        if self.dst is None:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'variable':
            raise Operation.Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self):
        if self.dst.text not in self.variables:
            raise Operation.Semantic_Error
        self.data_stack.append(self.variables[self.dst.text])
