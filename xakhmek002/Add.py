from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import parser3
import re
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from taci import Interpreter


class Add(ClassOperation):
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

    def _get_value(self, src: xml.Element, interpreter: Interpreter) -> int:
        try:
            if src.get('type') == 'integer':
                return int(src.text)
            elif src.get('type') == 'variable':
                var_name = src.text
                if var_name not in interpreter.variables:
                    raise Operation.Run_Time_Error_2
                if not isinstance(interpreter.variables[var_name], int):
                    raise Operation.Run_Time_Error_5
                return interpreter.variables[var_name]
        except ValueError:
            raise Operation.Run_Time_Error_5

    def execute(self, interpreter: Interpreter) -> None:
        try:
            val1 = self._get_value(self.src1, interpreter)
            val2 = self._get_value(self.src2, interpreter)
            interpreter.variables[self.dst.text] = val1 + val2
        except Operation.Run_Time_Error_2:
            raise
        except Operation.Run_Time_Error_5:
            raise
        except Exception as e:
            raise Operation.Run_Time_Error_5
