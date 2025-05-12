from __future__ import annotations
from Operation import Operation, Parsing_Error, Semantic_Error
import re
import parser3
import xml.etree.ElementTree as xml
 
class Label(Operation):
    def __init__(self, operation: xml.Element, labels):
        super().__init__(operation)
        self.dst = operation.find('dst')
        self.order = operation.get('order')
        self.labels = labels
        self._check_structure()

    def _check_structure(self):
        if self.dst is None:
            raise Parsing_Error
        if self.dst.get('type') != 'label':
            raise Semantic_Error
        if not re.fullmatch(parser3.label, self.dst.text):
            raise Semantic_Error
        label_name = self.dst.text
        label_position = int(self.order) - 1
        if not self.order.isdigit():
            raise Semantic_Error
        if label_name in self.labels:
            raise Semantic_Error
        self.labels[label_name] = label_position
        
    def execute(self):
        pass
