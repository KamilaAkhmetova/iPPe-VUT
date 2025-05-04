from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error, Run_Time_Error_2
import parser3
import re
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from taci import Interpreter 


class Sub(Operation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self.dst: xml.Element = None
        self.src1: xml.Element = None
        self.src2: xml.Element = None
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.src2 = operation.find('src2')

        if None in (self.dst, self.src1, self.src2):
            raise Parsing_Error
        if len(list(operation)) != 3:
            raise Parsing_Error
        if self.dst.get('type') != 'variable':
            raise Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            raise Semantic_Error

        valid_src_types = {'variable', 'integer'}
        if (self.src1.get('type') not in valid_src_types or 
            self.src2.get('type') not in valid_src_types):
            raise Semantic_Error

    def _get_numeric_value(self, src: xml.Element, interpreter: Interpreter) -> int:
        src_type = src.get('type')
        src_text = src.text

        if src_type == 'integer':
            if not parser3.type_check_int(src_text):
                raise Semantic_Error
            return int(src_text)

        elif src_type == 'variable':
            if src_text not in interpreter.variables:
                raise Run_Time_Error_2
            
            value = interpreter.variables[src_text]
            if not isinstance(value, int):
                raise Run_Time_Error_2
            return value

        else:
            raise Semantic_Error

    def execute(self, interpreter: Interpreter) -> None:
        try:
            val1 = self._get_numeric_value(self.src1, interpreter)
            val2 = self._get_numeric_value(self.src2, interpreter)
            interpreter.variables[self.dst.text] = val1 - val2
        except Run_Time_Error_2:
            raise
        except Exception as e:
            raise Run_Time_Error_2
