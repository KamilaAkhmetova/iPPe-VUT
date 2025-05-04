from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error
import re
import parser3
import xml.etree.ElementTree as xml
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from taci import Interpreter

class Mov(Operation):
    def __init__(self, operation: xml.Element, variables):
        # super().__init__(operation)
        # self.dst: xml.Element = None
        # self.src1: xml.Element = None
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.src2 = operation.find('src2') 
        self.variables = variables 
        self._check_structure(operation)

    def _check_structure(self, operation: xml.Element) -> None:
        # self.dst = operation.find('dst')
        # self.src1 = operation.find('src1')
        print('in mov')
        # error_is_in_mov = False
        if self.dst is None or self.src1 is None:
            print(000)
            raise Parsing_Error 
        # if len(list(operation)) != 2:
        #     raise Parsing_Error 
        if self.dst.get('type') != 'variable':
            print(111)
            raise Semantic_Error
        if not re.fullmatch(parser3.var, self.dst.text):
            print(222)
            raise Semantic_Error
        if self.src1.get('type') not in ['integer', 'string', 'variable']:
            print(333)
            raise Semantic_Error
        if self.src1.get('type') == 'integer' and not parser3.type_check_int(self.src1.text):
            print(444)
            raise Semantic_Error
        elif self.src1.get('type') == 'variable' and self.src1.text not in self.variables:
            print(555)
            raise RuntimeError
        # if (self.src1.get('type') == 'integer' and 
        #     not parser3.type_check_int(self.src1.text)) or \
        #    (self.src1.get('type') == 'string' and 
        #     not parser3.type_check_str(self.src1.text)):
        #     raise Semantic_Error
        print('in move check struct')
    def execute(self, interpreter):
        # didnt execute it
        print('executing mov')
        value = None
        if self.src1.get('type') == 'integer':
            value = int(self.src1.text)
        elif self.src1.get('type') == 'string':
            value = self.src1.text
        elif self.src1.get('type') == 'variable':
            if self.src1.text in interpreter.variables:
                value = interpreter.variables[self.src1.text]
            else:
                raise RuntimeError(f"Read access to undefined variable: {self.src1.text}")
        interpreter.variables[self.dst.text] = value
    # def execute(self, interpreter: Interpreter) -> None:
    #     if self.src1.get('type') == 'integer':
    #         value = int(self.src1.text)
    #     else:
    #         value = str(self.src1.text)
    #     interpreter.variables[self.dst.text] = value
# from Operation import Operation as ClassOperation
# import Operation
# # import taci
# import parser3
# import re

# class Mov(ClassOperation):
#     def __init__(self, operation):
#         super().__init__(operation)
#         self._check_structure(operation)

#     def _check_structure(self, operation):
#         self.dst = operation.find('dst')
#         self.src1 = operation.find('src1')
#         if self.dst is None or self.src1 is None:
#             raise Operation.Parsing_Error 
#         if len(list(operation)) != 2:
#             raise Operation.Parsing_Error 
#         if self.dst.get('type') != 'variable':
#             raise Operation.Semantic_Error
#         if re.match(parser3.var, self.dst.text) != True:
#             raise Operation.Semantic_Error
#         if self.src1.get('type') not in ['integer','string']:
#             raise Operation.Semantic_Error
#         if (self.src1.get('type') == 'integer' and \
#             parser3.type_check_int(self.src1.text) == False) or \
#                 (self.src1.get('type') == 'string' and \
#                     parser3.type_check_str(self.src1.text) == False):
#             raise Operation.Semantic_Error
        
#     def execute(self, interpreter):
#         if self.src1.get('type') == 'integer':
#             value = int(self.src1.text)
#         elif self.src1.get('type') == 'string':
#             value = str(self.src1.text)
#         interpreter.variables[self.dst.text] = value
#         # dst = self.dict_of_tags
#         # if parser3.type_check(self.src1.text) != True :
#         #     raise 
#         # self.dict_of_tags_mov = {
#         #     'dst': self.dict_of_tags['dst'],
#         #     'src1':self.dict_of_tags['src1']
#         # }
#     #     self.dict_of_tags_mov = self.parse_
#     # def parse_
#     # name starts with _(protected) means that we are using this method only inside the class
    