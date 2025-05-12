from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import parser3
import re
import xml.etree.ElementTree as xml

class Jumpiflt(ClassOperation):
    def __init__(self, operation: xml.Element, variables, labels):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.src1 = operation.find('src1')
        self.src2 = operation.find('src2')
        self.variables = variables
        self.labels = labels
        self.label_name = self.dst.text
        self._check_structure()

    def _check_structure(self):
        if self.dst is None or self.src1 is None or self.src2 is None:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'label':
            raise Operation.Semantic_Error
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self):
        if self.dst is None or self.dst.text not in self.labels:
            raise Operation.Run_Time_Error_1
        try:
            val1 = super()._get_value(self.src1, self.variables)
            val2 = super()._get_value(self.src2, self.variables)
            if type(val1) != type(val2):
                raise Operation.Run_Time_Error_2
            if val1 < val2:
                return self.labels[self.dst.text]
            return None

        except Operation.Run_Time_Error_5:
            raise
        except Operation.Run_Time_Error_2:
            raise
    
    def get_label_name(self):
        return self.label_name
