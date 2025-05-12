import sys
import parser3
import xml.etree.ElementTree as xml

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
        self.operations_dictionary = {}
        
    def parse_arguments(self):
        sources = sys.argv[1:] 
        if len(sources) < 1:
            raise ParsingError
        input_arg = None
        program_arg = None
        output_arg = None
        for s in sources:
            if s.startswith('--input='):
                if input_arg is not None:
                    raise ParsingError
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
        
    def create_operation(self, tac_element: xml.Element):
        opcode = tac_element.get('opcode')
        if opcode == 'MOV':
            from Mov import Mov
            return Mov(tac_element, self.variables)
        elif opcode == 'ADD':
            from Add import Add
            return Add(tac_element, self.variables)
        elif opcode == 'SUB':
            from Sub import Sub
            return Sub(tac_element, self.variables)
        elif opcode == 'MUL':
            from Mul import Mul
            return Mul(tac_element, self.variables)
        elif opcode == 'DIV':
            from Div import Div
            return Div(tac_element, self.variables)
        elif opcode == 'READINT':
            from Read_Int import Read_Int
            return Read_Int(tac_element, self)
        elif opcode == 'READSTR':
            from Read_Str import Read_Str
            return Read_Str(tac_element, self)
        elif opcode == 'PRINT':
            from Print import Print
            return Print(tac_element, self.variables, self.output)
        elif opcode == 'PRINTLN':
            from Println import Println
            return Println(tac_element, self.variables, self.output)
        elif opcode == 'LABEL':
            from Label import Label
            return Label(tac_element, self.labels)
        elif opcode == 'JUMP':
            from Jump import Jump
            return Jump(tac_element, self.labels)
        elif opcode == 'JUMPIFEQ':
            from Jumpifeq import Jumpifeq
            return Jumpifeq(tac_element, self.labels, self.variables)
        elif opcode == 'JUMPIFLT':
            from Jumpiflt import Jumpiflt
            return Jumpiflt(tac_element, self.variables, self.labels)
        elif opcode == 'CALL':
            from Call import Call
            return Call(tac_element, self.labels, self.call_return_stack)
        elif opcode == 'RETURN':
            from Return import Return
            return Return(tac_element, self.call_return_stack)
        elif opcode == 'PUSH':
            from Push import Push
            return Push(tac_element, self.variables, self.data_stack)
        elif opcode == 'POP':
            from Pop import Pop
            return Pop(tac_element, self.variables, self.data_stack)
        else:
            raise SemanticError
        
    def run(self):
        try:
            xml_element = xml.fromstring(self.xml_file[0])
        except xml.ParseError:
            raise ParsingError
        if xml_element.tag != 'program':
            raise ParsingError
        self.read_input_file()

        if self.output:
            with open(self.output, 'w', encoding='utf-8') as f:
                pass

        for tac in xml_element.findall('tac'):
            opcode = tac.get('opcode')
            order = tac.get('order')
            if opcode is None or order is None:
                raise ParsingError
            operation = self.create_operation(tac)
            self.operations.append(operation)
            self.operations_dictionary[int(order)] = operation

        step = 1
        last_order = max(self.operations_dictionary.keys())

        while step <= last_order:
            from Jump import Jump
            from Jumpifeq import Jumpifeq
            from Jumpiflt import Jumpiflt
            from Call import Call 
            from Return import Return
            operation = self.operations_dictionary.get(step)
            if operation is None:
                break
            
            if isinstance(operation, (Jump, Jumpifeq, Jumpiflt, Call, Return)):
                new_step = self.operations_dictionary[step].execute()
                if new_step is not None:
                    step = new_step
                    continue
            else:
                self.operations_dictionary[step].execute()
            step += 1

try:
        interpreter = Interpreter()
        interpreter.parse_arguments()
        interpreter.read_file()
        interpreter.run()
        print(0)  
except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)