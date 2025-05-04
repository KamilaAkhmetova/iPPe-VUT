from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import parser3
import re
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from taci import Interpreter  


class Jumpifeq(ClassOperation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self.dst: Optional[xml.Element] = None
        self.src1: Optional[xml.Element] = None
        self.src2: Optional[xml.Element] = None
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.src2 = operation.find('src2')

        if None in (self.dst, self.src1, self.src2):
            raise Operation.Parsing_Error

        if self.dst.get('type') != 'label':
            raise Operation.Semantic_Error

        if not re.fullmatch(parser3.label, self.dst.text):
            raise Operation.Semantic_Error

    def _get_value(self, value: xml.Element, interpreter: Interpreter) -> Union[int, str]:
        val_type = value.get('type')
        val_text = value.text
        if val_type == 'integer':
            if not parser3.type_check_int(val_text):
                raise Operation.Run_Time_Error_5
            return int(val_text)
        elif val_type == 'string':
            return str(val_text)
        elif val_type == 'variable':
            if val_text not in interpreter.variables:
                raise Operation.Run_Time_Error_2
            var_value = interpreter.variables[val_text]
            if not isinstance(var_value, (int, str)):
                raise Operation.Run_Time_Error_2
            return var_value
        else:
            raise Operation.Semantic_Error

    def execute(self, interpreter: Interpreter) -> Optional[int]:
        if self.dst is None or self.dst.text not in interpreter.labels:
            raise Operation.Run_Time_Error_1

        try:
            val1 = self._get_value(self.src1, interpreter)
            val2 = self._get_value(self.src2, interpreter)

            if type(val1) != type(val2):
                raise Operation.Run_Time_Error_2

            if val1 == val2:
                return interpreter.labels[self.dst.text]
            return None

        except Operation.Run_Time_Error_5:
            raise
        except Operation.Run_Time_Error_2:
            raise
        except Exception as e:
            raise Operation.Run_Time_Error_2
