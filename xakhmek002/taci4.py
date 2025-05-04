import sys
import xml.etree.ElementTree as xml
from Mov import Mov
from Add import Add
from Sub import Sub
from Mul import Mul
from Div import Div
from Read_Int import Read_Int
from Read_Str import Read_Str
from Print import Print
from Println import Println
from Label import Label
from Jump import Jump
from Jumpifeq import Jumpifeq
from Jumpiflt import Jumpiflt
from Call import Call
from xakhmek002.Return import Return
from Push import Push
from Pop import Pop

class ParsingError(Exception):
    def __init__(self, message="Parsing Error during the parsing of XML, invalid XML input, file cannot be opened."):
        super().__init__(message)

class SemanticError(Exception):
    def __init__(self, message="Semantic Error during the semantic checks."):
        super().__init__(message)

class RuntimeError(Exception):
    def __init__(self, message="Run-time Error"):
        super().__init__(message)

class Interpreter():
    def __init__(self):
        self.input = ''
        self.program = ''
        self.output = ''
        self.xml_root = None
        self.variables = {}
        self.labels = {}
        self.input_file_lines = []
        self.input_file_line_counter = 0
        self.call_return_stack = []
        self.data_stack = []
        self.operations = []

    def parse_arguments(self):
        sources = sys.argv[1:]  # Игнорируем имя скрипта
        if not sources:
            raise ParsingError("Usage: python taci3.py <program.xml> [output] [--input=input.txt]")
        
        # Обработка --input=
        input_args = [s for s in sources if s.startswith('--input=')]
        if len(input_args) > 1:
            raise ParsingError("Only one --input argument allowed")
        
        if input_args:
            self.input = input_args[0].split('=', 1)[1]
            sources.remove(input_args[0])
        
        if not sources:
            raise ParsingError("Program file argument is missing.")
        
        self.program = sources[0]
        if len(sources) > 1:
            self.output = sources[1]

    def read_file(self):
        try:
            tree = xml.parse(self.program)
            self.xml_root = tree.getroot()
            if self.xml_root.tag != 'program':
                raise ParsingError("Root XML element must be 'program'")
        except FileNotFoundError:
            raise ParsingError(f"File {self.program} not found")
        except xml.ParseError as e:
            raise ParsingError(f"XML parsing error: {str(e)}")
        except Exception as e:
            raise ParsingError(f"Error reading file: {str(e)}")

    def read_input_file(self):
        if not self.input:
            return
            
        try:
            with open(self.input, 'r') as f:
                self.input_file_lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            raise ParsingError(f"Error reading input file: {str(e)}")

    def read_next_int(self):
        try:
            if self.input:
                if self.input_file_line_counter >= len(self.input_file_lines):
                    raise RuntimeError("No more input values available")
                value = self.input_file_lines[self.input_file_line_counter]
                self.input_file_line_counter += 1
                return int(value)
            return int(sys.stdin.readline().strip())
        except ValueError:
            raise RuntimeError("READINT got invalid value (not an integer)")
        except Exception as e:
            raise RuntimeError(f"Error reading integer input: {str(e)}")

    def read_next_str(self):
        try:
            if self.input:
                if self.input_file_line_counter >= len(self.input_file_lines):
                    raise RuntimeError("No more input values available")
                value = self.input_file_lines[self.input_file_line_counter]
                self.input_file_line_counter += 1
                return str(value)
            return str(sys.stdin.readline().strip())
        except Exception as e:
            raise RuntimeError(f"Error reading string input: {str(e)}")

    def create_operation(self, tac_element):
        opcode = tac_element.get('opcode')
        if opcode is None:
            raise SemanticError("Missing opcode in TAC element")
            
        op_classes = {
            'MOV': Mov,
            'ADD': Add,
            'SUB': Sub,
            'MUL': Mul,
            'DIV': Div,
            'READINT': Read_Int,
            'READSTR': Read_Str,
            'PRINT': Print,
            'PRINTLN': Println,
            'LABEL': Label,
            'JUMP': Jump,
            'JUMPIFEQ': Jumpifeq,
            'JUMPIFLT': Jumpiflt,
            'CALL': Call,
            'RETURN': Return,
            'PUSH': Push,
            'POP': Pop
        }
        
        if opcode not in op_classes:
            raise SemanticError(f"Unknown opcode: {opcode}")
            
        return op_classes[opcode](tac_element)

    def run(self):
        if self.xml_root is None:
            raise ParsingError("XML file not loaded")
            
        self.read_input_file()
        
        # Сначала собираем все LABEL
        for tac in self.xml_root.findall('tac'):
            if tac.get('opcode') == 'LABEL':
                label_name = tac.get('dst')
                if not label_name:
                    raise SemanticError("LABEL instruction missing 'dst' attribute")
                if label_name in self.labels:
                    raise SemanticError(f"Duplicate label: {label_name}")
                self.labels[label_name] = len(self.operations)
                self.operations.append(self.create_operation(tac))
        
        # Затем обрабатываем остальные операции
        for tac in self.xml_root.findall('tac'):
            if tac.get('opcode') != 'LABEL':
                operation = self.create_operation(tac)
                self.operations.append(operation)
        
        # Выполняем операции
        pc = 0  # program counter
        while pc < len(self.operations):
            try:
                new_pc = self.operations[pc].execute(self, pc)
                if new_pc is None:
                    pc += 1
                else:
                    pc = new_pc
            except Exception as e:
                raise RuntimeError(f"Runtime error at operation {pc} ({self.operations[pc].__class__.__name__}): {str(e)}")

if __name__ == "__main__":
    try:
        interpreter = Interpreter()
        interpreter.parse_arguments()
        interpreter.read_file()
        interpreter.run()
    except ParsingError as e:
        print(f"Parsing Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except SemanticError as e:
        print(f"Semantic Error: {str(e)}", file=sys.stderr)
        sys.exit(2)
    except RuntimeError as e:
        print(f"Runtime Error: {str(e)}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"Internal Error: {str(e)}", file=sys.stderr)
        sys.exit(99)