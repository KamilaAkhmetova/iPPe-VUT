# current order!!
from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import re
import parser3
import xml.etree.ElementTree 

class Call(ClassOperation):
    def __init__(self, operation: xml.etree.ElementTree.Element, labels, call_return_stack):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.order = operation.get('order')
        self.labels = labels
        self.call_return_stack = call_return_stack
        self._check_structure()

    def _check_structure(self) :        
        if self.dst is None:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'label':
            raise Operation.Semantic_Error
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self):
        if self.dst.text not in self.labels:
            raise Operation.Run_Time_Error_1    
        self.call_return_stack.append(self.order)
        return int(self.labels[self.dst.text]) + 2
        # self.current_order = self.labels[self.dst.text]
