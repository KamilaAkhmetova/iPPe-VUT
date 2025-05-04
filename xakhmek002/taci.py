import sys
import parser3
import xml.etree.ElementTree as xml
# import argparse

class ParsingError(Exception):
    def __init__(self, message="Parsing Error during the parsing of XML, invalid XML input, file cannot be opened."):
        super().__init__(message)
class SemanticError(Exception):
    def __init__(self, message="Semantic Error during the semantic checks (e.g., a label occurs several times)."):
        super().__init__(message)
class RuntimeError1(Exception):
    def __init__(self, message = "Run-time Error: Jump/call to a non-existing label."):
        super().__init__(message)
class RuntimeError2(Exception):
    def __init__(self, message = "Run-time Error: Read access to a non-defined variable."):
        super().__init__(message)
class RuntimeError3(Exception):
    def __init__(self, message = "Run-time Error: Division by zero using DIV instruction."):
        super().__init__(message)
class RuntimeError4(Exception):
    def __init__(self, message="Run-time Error: READINT get invalid value (not an integer)."):
        super().__init__(message)
class RuntimeError5(Exception):
    def __init__(self, message = "Run-time Error: Operands of incompatible type."):
        super().__init__(message)
class RuntimeError6(Exception):
    def __init__(self, message = "Run-time Error: Pop from the empty (data/call) stack is forbidden"):
        super().__init__(message)
class InternalError(Exception):
    def __init__(self, message="Internal errors."):
        super().__init__(message)

class Interpreter():
    def __init__(self):
        self.input = ''
        self.program = ''
        self.output = ''
        self.xml_file = None
        self.variables = {}
        self.labels = {}
        self.input_file = None
        self.input_file_lines = []
        self.input_file_line_counter = 0
        self.call_return_stack = []
        self.data_stack = []
        self.operations = []

    # def parse_arguments(self):
    #     source = sys.argv[1] 
    #     if source is None:
    #         raise ParsingError
    #     input_arg = None
    #     program_arg = None
    #     output_arg = None
    #     if source.startswith('--input='):
    #         input_arg = source.split('=', 1)[1]
    #         program_arg = sys.argv[2]
    #         if sys.argv[3] != None:
    #             output_arg = sys.argv[3]
    #     else:
    #         program_arg = sys.argv[1]
    #         if sys.argv[3] != None:
    #             output_arg = sys.argv[3]
    #     self.input = input_arg
    #     self.program = program_arg
    #     self.output = output_arg

        # for s in sources:
        #     if s.startswith('--input='):
        #         if input_arg is not None:
        #             raise ParsingError
        #         input_arg = s.split('=', 1)[1]
        #     elif program_arg is None:
        #         program_arg = s
        #     elif output_arg is None:
        #         output_arg = s
        #     else:
        #         raise ParsingError 
        # if program_arg is None:
        #     raise ParsingError

        
    def parse_arguments(self):
        sources = sys.argv[1:] 
        if len(sources) < 1:
            raise ParsingError
        input_arg = None
        program_arg = None
        output_arg = None
        for s in sources:
            if s.startswith('--input='):
                # if input_arg is not None:
                #     raise ParsingError
                input_arg = s.split('=', 1)[1]
            elif program_arg is None:
                program_arg = s
            elif output_arg is None:
                output_arg = s
            else:
                raise ParsingError 
        if program_arg is None:
            raise ParsingError
        self.input = input_arg
        self.program = program_arg
        self.output = output_arg



    # def parse_arguments(self):
    #     sources = sys.argv
    #     if len(sources) < 2:
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
    #         if len(sources) < 2:
    #             raise ParsingError
    #         self.program = sources[0]
    #         if len(sources) > 1:
    #             self.output = sources[1]
    #         if len(sources) > 2:
    #             print(sources)
    #             raise ParsingError
    
    def read_file(self):
        try:
            content, self.program = parser3.read_file(self.program)
            self.xml_file = (content, self.program)
        except Exception:
            raise ParsingError
        
    def read_input_file(self):
        if self.input:
            try:
                with open(self.input, 'r') as f:
                    self.input_file_lines = [line.strip() for line in f.readlines()]
            except:
                raise ParsingError
        # else: print('тут')
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
        # временно
        print('ccccc')
        opcode = tac_element.get('opcode')
        if opcode == 'MOV':
            from Mov import Mov
            # return Mov(tac_element)
            print('creating mov')
            return Mov(tac_element, self.variables)
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
        # временно 
        print('bbbb')
        # lines = self.xml_file[0].splitlines()
        # connected = '\n'.join(lines)
        try:
            # временно
            # print(self.xml_file[0])
            xml_element = xml.fromstring(self.xml_file[0])
            # print(xml_element)
        except xml.ParseError:
            raise ParsingError
        if xml_element.tag != 'program':
            raise ParsingError
        self.read_input_file()
        # tac is xml element
        for tac in xml_element.findall('tac'):
            # print('я туть')
            opcode = tac.get('opcode')
            order = tac.get('order')
            print(opcode)
            print(order)
            if opcode is None or order is None:
                raise ParsingError
            print('looking for mistake')
            # Operation operation = self.create_operation(tac)
            operation = self.create_operation(tac)
            # не доходит
            print('append operation')
            self.operations.append(operation)
            # не доходит
            print('before polimorphism')
        for operation in self.operations:
            # не доходит
            print('on my way to polimorphism')
            # example of polimorphism
            operation.execute(self)
            # opcode = tac.get('opcode') #returns string like MOV
            # order = tac.get('order')
    #  for -help operation
    # def toString():
    #     return  
interpreter = Interpreter()
# interpreter.read_input_file()
interpreter.parse_arguments()
interpreter.read_file()
interpreter.run()