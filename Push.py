from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error, Run_Time_Error_2, Run_Time_Error_5
import re
import parser3
import xml.etree.ElementTree as xml

class Push(Operation):
    def __init__(self, operation: xml.Element, variables, data_stack):
        super().__init__(operation)
        self.src1 = operation.find('src1')
        self.variables = variables
        self.data_stack = data_stack
        self._check_structure()

    def _check_structure(self):
        if self.src1 is None:
            raise Parsing_Error
        valid_types = ['variable', 'string', 'integer']
        if self.src1.get('type') not in valid_types:
            raise Semantic_Error
        if (self.src1.get('type') == 'variable' and not re.fullmatch(parser3.var, self.src1.text)):
            raise Semantic_Error
        if self.src1.get('type') == 'integer' and not parser3.type_check_int(self.src1.text):
            raise Semantic_Error
        
    def execute(self):
        try:
            if self.src1.get('type') == 'variable':
                if self.src1.text not in self.variables:
                    raise Run_Time_Error_2
                value = self.variables[self.src1.text]
            else:
                value = self.src1.text
                if self.src1.get('type') == 'integer':
                    try:
                        value = int(value)
                    except ValueError:
                        raise Run_Time_Error_5
            self.data_stack.append(value)
            
        except Run_Time_Error_2:
            raise
        except Run_Time_Error_5:
            raise
