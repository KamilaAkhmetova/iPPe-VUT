import sys
import parser3
import xml.etree.ElementTree as xml
import argparse

class OperationError(Exception):
    pass

class ParsingError(OperationError):
    def __init__(self, message="Parsing Error during the parsing of XML, invalid XML input, file cannot be opened."):
        super().__init__(message)

class SemanticError(OperationError):
    def __init__(self, message="Semantic Error during the semantic checks (e.g., a label occurs several times)."):
        super().__init__(message)

class RuntimeError1(OperationError):
    def __init__(self, message = "Run-time Error: Jump/call to a non-existing label."):
        super().__init__(message)

class RuntimeError2(OperationError):
    def __init__(self, message = "Run-time Error: Read access to a non-defined variable."):
        super().__init__(message)

class RuntimeError3(OperationError):
    def __init__(self, message = "Run-time Error: Division by zero using DIV instruction."):
        super().__init__(message)

class RuntimeError4(OperationError):
    def __init__(self, message="Run-time Error: READINT get invalid value (not an integer)."):
        super().__init__(message)

class RuntimeError5(OperationError):
    def __init__(self, message = "Run-time Error: Operands of incompatible type."):
        super().__init__(message)

class RuntimeError6(OperationError):
    def __init__(self, message = "Run-time Error: Pop from the empty (data/call) stack is forbidden"):
        super().__init__(message)

class InternalError(OperationError):
    def __init__(self, message="Internal errors."):
        super().__init__(message)


class Interpreter():
    def __init__(self):
        self.input = ''
        self.program = ''
        self.output = ''
        self.xml_tree = None
        self.variables = {}
        self.labels = {}
        self.input_file = None
        self.input_file_lines = []
        self.input_file_line_counter = 0
        self.call_return_stack = []
        self.data_stack = []
        self.operations = []

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='TAC Interpreter')
    
    # Добавляем аргументы согласно условиям
        parser.add_argument('--input', dest='input_file', 
                            help='input file for READINT/READSTR (default: stdin)',
                            default=sys.stdin)
        parser.add_argument('program', 
                            help='XML program file (mandatory)')
        parser.add_argument('output', nargs='?', 
                            help='output file for PRINT (default: stdout)',
                            default=sys.stdout)
        
        args = parser.parse_args()
        self.input = args.input_file
        self.program = args.program
        self.output = args.output
        return args
    # def parse_arguments(self):
    #     sources = sys.argv[1:]
    #     if not sources:
    #         raise ParsingError
    #     input_arg = None
    #     for s in sources:
    #         if s.startswith('--input='):
    #             if input_arg is not None:
    #                 raise ParsingError
    #             input_arg = s
    #             self.input = s.split('=', 1)[1]
    #     if input_arg:
    #         sources.remove(input_arg)
    #     if not sources:
    #         raise ParsingError
    #     self.program = sources[0]
    #     if len(sources) > 1:
    #         self.output = sources[1]
    #     if len(sources) > 2:
    #         raise ParsingError
        
    def read_input_file(self):
        if self.input:
            try:
                with open(self.input, 'r') as f:
                    self.input_file_lines = [line.strip() for line in f.readlines()]
            except:
                raise ParsingError
    
    def read_file(self):
        try:
            # it returns tuple, content=[0], path=[1]
            self.xml_file = parser3.read_file(self.program)
        except:
            raise ParsingError
    def read_next_int(self):
        try:
            if self.input:
                if self.input_file_line_counter >= len(self.input_file_lines):
                    
                    raise RuntimeError2
                value = self.input_file_lines[self.input_file_line_counter]
                self.input_file_line_counter += 1
                return int(value)
            else:
                
                return int(sys.stdin.readline().strip())
        except:
            raise RuntimeError4
    def read_next_str(self):
        try:
            if self.input:
                if self.input_file_line_counter >= len(self.input_file_lines):
                    raise RuntimeError2
                value = self.input_file_lines[self.input_file_line_counter]
                self.input_file_line_counter += 1
                return str(value)
            else:
                return str(sys.stdin.readline().strip())
        except:
            raise RuntimeError4
    # def read_value():
    def create_operation(self, tac_element: xml.Element):
        opcode = tac_element.get('opcode')

        if opcode == 'MOV':
            from Mov import Mov
            return Mov(tac_element)
        elif opcode == 'ADD':
            from Add import Add
            return Add(tac_element)
        elif opcode == 'SUB':
            from Sub import Sub
            return Sub(tac_element)
        elif opcode == 'MUL':
            from Mul import Mul
            return Mul(tac_element)
        elif opcode == 'DIV':
            from Div import Div
            return Div(tac_element)
        elif opcode == 'READINT':
            from Read_Int import Read_Int
            return Read_Int(tac_element)
        elif opcode == 'READSTR':
            from Read_Str import Read_Str
            return Read_Str(tac_element)
        elif opcode == 'PRINT':
            from Print import Print
            return Print(tac_element)
        elif opcode == 'PRINTLN':
            from Println import Println
            return Println(tac_element)
        elif opcode == 'LABEL':
            from Label import Label
            return Label(tac_element)
        elif opcode == 'JUMP':
            from Jump import Jump
            return Jump(tac_element)
        elif opcode == 'JUMPIFEQ':
            from Jumpifeq import Jumpifeq
            return Jumpifeq(tac_element)
        elif opcode == 'JUMPIFLT':
            from Jumpiflt import Jumpiflt
            return Jumpiflt(tac_element)
        elif opcode == 'CALL':
            from Call import Call
            return Call(tac_element)
        elif opcode == 'RETURN':
            from Return import Return
            return Return(tac_element)
        elif opcode == 'PUSH':
            from Push import Push
            return Push(tac_element)
        elif opcode == 'POP':
            from Pop import Pop
            return Pop(tac_element)
        else:
            raise SemanticError

    # иду по хмл 
    def run(self):
        lines = self.xml_file[0].splitlines()
        connected = '\n'.join(lines)
        try:
            xml_element = xml.fromstring(connected)
        # либо так except xml.ParseError: 
        except ParsingError:
            print("Parsing Error during the parsing of XML, invalid XML input, file cannot be opened.")
        if xml_element.tag != 'program':
            raise ParsingError
        self.read_input_file()
        # tac is xml element
        for tac in xml_element.findall('tac'):
            opcode = tac.get('opcode')
            order = tac.get('order')
            if opcode is None or order is None:
                raise ParsingError
            operation = self.create_operation(tac)
            self.operations.append(operation)
        for operation in self.operations:
            operation.execute(self)
            # opcode = tac.get('opcode') #returns string like MOV
            # order = tac.get('order')
    #  for -help operation
    # def toString():
    #     return  
interpreter = Interpreter()
interpreter.parse_arguments()
interpreter.read_file()
interpreter.run()