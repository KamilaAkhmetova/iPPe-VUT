from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import parser3
import re
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from taci import Interpreter  


class Div(ClassOperation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.src2 = operation.find('src2')
        if None in (self.dst, self.src1, self.src2):
            raise Operation.Parsing_Error
        if len(list(operation)) != 3:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'variable':
            raise Operation.Semantic_Error            
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Operation.Semantic_Error            
        valid_types = {'variable', 'integer'}
        if (self.src1.get('type') not in valid_types or 
            self.src2.get('type') not in valid_types):
            raise Operation.Semantic_Error

    def execute(self, interpreter: Interpreter) -> None:
        def get_value(src: xml.Element) -> int:
            src_type = src.get('type')
            src_text = src.text
            if src_type == 'integer':
                try:
                    return int(src_text)
                except ValueError:
                    raise Operation.Run_Time_Error_5
            elif src_type == 'variable':
                if src_text not in interpreter.variables:
                    raise Operation.Run_Time_Error_2
                value = interpreter.variables[src_text]
                if not isinstance(value, int):
                    raise Operation.Run_Time_Error_5
                return value
            else:
                raise Operation.Semantic_Error
        try:
            val1 = get_value(self.src1)
            val2 = get_value(self.src2)
            if val2 == 0:
                raise Operation.Run_Time_Error_5
            interpreter.variables[self.dst.text] = val1 // val2  
        except (ValueError, TypeError) as e:
            raise Operation.Run_Time_Error_5
        
