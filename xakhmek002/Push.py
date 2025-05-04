from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error, Run_Time_Error_2, Run_Time_Error_5
import re
import parser3
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from taci import Interpreter  


class Push(Operation):
    def __init__(self, operation: xml.Element):
        super().__init__(operation)
        self.src1: xml.Element = None
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        self.src1 = operation.find('src1')
        
        if self.src1 is None:
            raise Parsing_Error
            
        valid_types = {'variable', 'string', 'integer'}
        if self.src1.get('type') not in valid_types:
            raise Semantic_Error
            
        if (self.src1.get('type') == 'variable' and 
            not re.fullmatch(parser3.var, self.src1.text)) or \
           (self.src1.get('type') in {'string', 'integer'} and 
            not parser3.type_check(self.src1.text)):
            raise Semantic_Error

    def execute(self, interpreter: Interpreter) -> None:
        try:
            if self.src1.get('type') == 'variable':
                if self.src1.text not in interpreter.variables:
                    raise Run_Time_Error_2
                value = interpreter.variables[self.src1.text]
            else:
                value = self.src1.text
                if self.src1.get('type') == 'integer':
                    try:
                        value = int(value)
                    except ValueError:
                        raise Run_Time_Error_5
            
            interpreter.data_stack.append(value)
            
        except Run_Time_Error_2:
            raise
        except Run_Time_Error_5:
            raise
        except Exception as e:
            raise Run_Time_Error_5
