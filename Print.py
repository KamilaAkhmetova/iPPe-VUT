from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error, Run_Time_Error_2
import parser3
import re
import xml.etree.ElementTree as xml 

class Print(Operation):
    def __init__(self, operation: xml.Element, variables, output):
        super().__init__(operation)
        self.src1 = operation.find('src1')
        self.variables = variables 
        self.output = output
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
                value = str(self.variables[self.src1.text])
            else:
                value = self.src1.text
            if self.output:
                with open(self.output, 'a', encoding='utf-8') as f:
                    f.write(value + '')
            else:
                print(value, end='')
                
        except Run_Time_Error_2:
            raise
