import sys
import xml.etree.ElementTree as xml

class ParsingError(Exception):
    def __init__(self, message="Parsing Error during the parsing of XML, invalid XML input, file cannot be opened."):
        super().__init__(message)

class Interpreter:
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

    def parse_arguments(self):
        sources = sys.argv
        if len(sources) < 2:
            raise ParsingError("Program file argument is missing.")
        
        input_arg = None
        for s in sources:
            if s.startswith('--input='):
                if input_arg is not None:
                    raise ParsingError("Duplicate --input argument.")
                input_arg = s
                self.input = s.split('=', 1)[1]

        if input_arg:
            sources.remove(input_arg)
        
        if len(sources) < 2:
            raise ParsingError("Program file argument is missing.")
        
        self.program = sources[1]
        if len(sources) > 1:
            self.output = sources[1]
        # if len(sources) > 2:
        #     raise ParsingError("Too many arguments.")
        
    def read_input_file(self):
        if self.input:
            try:
                with open(self.input, 'r') as f:
                    self.input_file_lines = [line.strip() for line in f.readlines()]
            except Exception:
                raise ParsingError("Error reading input file.")
    
    def read_file(self):
        # Чтение XML файла и парсинг
        try:
            tree = xml.parse(self.program)
            root = tree.getroot()
            self.xml_file = root  # Теперь xml_file - это корневой элемент XML
        except FileNotFoundError:
            raise ParsingError(f"File {self.program} not found.")
        except xml.ParseError:
            raise ParsingError("Error parsing XML file.")
    
    def read_next_int(self):
        try:
            if self.input:
                if self.input_file_line_counter >= len(self.input_file_lines):
                    raise RuntimeError("No more input values.")
                value = self.input_file_lines[self.input_file_line_counter]
                self.input_file_line_counter += 1
                return int(value)
            else:
                return int(sys.stdin.readline().strip())
        except:
            raise RuntimeError("Error reading integer input.")

    def read_next_str(self):
        try:
            if self.input:
                if self.input_file_line_counter >= len(self.input_file_lines):
                    raise RuntimeError("No more input values.")
                value = self.input_file_lines[self.input_file_line_counter]
                self.input_file_line_counter += 1
                return str(value)
            else:
                return str(sys.stdin.readline().strip())
        except:
            raise RuntimeError("Error reading string input.")

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
            from xakhmek002.Return import Return
            return Return(tac_element)
        elif opcode == 'PUSH':
            from Push import Push
            return Push(tac_element)
        elif opcode == 'POP':
            from Pop import Pop
            return Pop(tac_element)
        # else:
        #     raise SemanticError("Unknown opcode.")

    def run(self):
        try:
            if self.xml_file is None:
                raise ParsingError("XML file not loaded.")
            
            # Прочитали и парсим XML содержимое
            for tac in self.xml_file.findall('tac'):
                opcode = tac.get('opcode')
                order = tac.get('order')
                if opcode is None or order is None:
                    raise ParsingError("Invalid TAC element: missing opcode or order.")
                operation = self.create_operation(tac)
                self.operations.append(operation)

            for operation in self.operations:
                operation.execute(self)

        except Exception as e:
            raise RuntimeError(f"Runtime error: {e}")
            

# Пример использования:
interpreter = Interpreter()
interpreter.parse_arguments()
interpreter.read_file()  # Чтение и парсинг XML файла
interpreter.run()  # Запуск обработки TAC
