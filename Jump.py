from __future__ import annotations
from Operation import Operation as ClassOperation
import Operation
import re
import parser3
import xml.etree.ElementTree as xml
 
class Jump(ClassOperation):
    def __init__(self, operation: xml.Element, labels):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.labels = labels
        self.label_name = self.dst.text
        self._check_structure()

    def _check_structure(self):
        if self.dst is None:
            raise Operation.Parsing_Error
        if self.dst.get('type') != 'label':
            raise Operation.Semantic_Error
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Operation.Semantic_Error

    def execute(self):
        if self.dst is None or self.dst.text not in self.labels:
            raise Operation.Run_Time_Error_1
        return int(self.labels[self.dst.text]) + 2
    
    def get_label_name(self):
        return self.label_name