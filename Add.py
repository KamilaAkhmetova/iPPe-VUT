from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import parser3
import re
import xml.etree.ElementTree as xml

class Add(ClassOperation):
    def __init__(self, operation: xml.Element, variables):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.src2 = operation.find('src2')
        self.variables = variables
        if len(list(operation)) != 3:
            raise Operation.Parsing_Error
        self._check_structure()

    def _check_structure(self):
        if self.dst is None or self.src1 is None or self.src2 is None:
            raise Operation.Parsing_Error 
        if self.dst.get('type') != 'variable':
            raise Operation.Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Operation.Semantic_Error
        valid_types = ['variable', 'integer']
        if (self.src1.get('type') not in valid_types or 
            self.src2.get('type') not in valid_types):
            raise Operation.Semantic_Error
        if self.src1.get('type') == 'integer' and not parser3.type_check_int(self.src1.text):
            raise Operation.Semantic_Error
        elif self.src1.get('type') == 'variable' and not re.fullmatch(parser3.var, self.src1.text):
            raise RuntimeError
        if self.src2.get('type') == 'integer' and not parser3.type_check_int(self.src2.text):
            raise Operation.Semantic_Error
        elif self.src2.get('type') == 'variable' and not re.fullmatch(parser3.var, self.src2.text):
            raise RuntimeError
        
    def execute(self):
        try:
            val1 = super()._get_value(self.src1, self.variables)
            val2 = super()._get_value(self.src2, self.variables)
            self.variables[self.dst.text] = val1 + val2
        except Operation.Run_Time_Error_2:
            raise
        except Operation.Run_Time_Error_5:
            raise
        except Exception as e:
            raise Operation.Run_Time_Error_5
