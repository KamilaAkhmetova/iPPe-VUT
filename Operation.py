from abc import ABC, abstractmethod
import xml.etree.ElementTree as xml

class Parsing_Error(Exception):
    def __init__(self, message="Parsing Error during the parsing of XML, invalid XML input, file cannot be opened."):
        super().__init__(message)
class Semantic_Error(Exception):
    def __init__(self, message="Semantic Error during the semantic checks (e.g., a label occurs several times)."):
        super().__init__(message)
class Run_Time_Error_1(Exception):
    def __init__(self, message = "Run-time Error: Jump/call to a non-existing label."):
        super().__init__(message)
class Run_Time_Error_2(Exception):
    def __init__(self, message = "Run-time Error: Read access to a non-defined variable."):
        super().__init__(message)
class Run_Time_Error_3(Exception):
    def __init__(self, message = "Run-time Error: Division by zero using DIV instruction."):
        super().__init__(message)
class Run_Time_Error_4(Exception):
    def __init__(self, message="Run-time Error: READINT get invalid value (not an integer)."):
        super().__init__(message)
class Run_Time_Error_5(Exception):
    def __init__(self, message = "Run-time Error: Operands of incompatible type."):
        super().__init__(message)
class Run_Time_Error_6(Exception):
    def __init__(self, message = "Run-time Error: Pop from the empty (data/call) stack is forbidden"):
        super().__init__(message)
class Internal_Errors(Exception):
    def __init__(self, message="Internal errors."):
        super().__init__(message)
class Other_Errors(Exception):
    def __init__(self, message="Other run-time errors."):
        super().__init__(message)

class OrderCounter:
    counter = 0
    @classmethod
    def increment(cls):
        cls.counter += 1
        return cls.counter

class Operation(ABC):
    def __init__(self, operation: xml.Element):
        self.opcode = operation.get('opcode')
        if not self.opcode:
            raise Semantic_Error
        self.order = int(operation.get('order'))
        self.order_counter = OrderCounter.increment()
        if self.order != self.order_counter:
            raise Semantic_Error
        # self.dict_of_tags = self.parse_tac_elements(operation)

    def parse_tac_elements(self, operation: xml.Element):
        return {child.tag: child.text for child in operation}
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.opcode == other.opcode
    
    def __hash__(self):
        return hash(self.opcode)
    
    def _get_value(self, src: xml.Element, variables: dict):
        try:
            if src.get('type') == 'integer':
                return int(src.text)
            elif src.get('type') == 'variable':
                var_name = src.text
                if var_name not in variables:
                    raise Run_Time_Error_2
                if not isinstance(variables[var_name], int):
                    raise Run_Time_Error_5
                return variables[var_name]
        except ValueError:
            raise Run_Time_Error_5

    @abstractmethod
    def execute(self, interpreter):
        pass
