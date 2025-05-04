#corrected version 
import xml.etree.ElementTree as xml
import re
from xml.dom import minidom
import sys

ippe_file= sys.argv[1]
if ippe_file== "-":
    lines = []
    try:
        for i in sys.stdin:
            lines.append(i.rstrip('\n'))
        file_content = '\n'.join(lines)
    except Exception:
        print("Internal errors")
        exit()
else:
    try:
        with open(ippe_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
    except FileNotFoundError:
        print("Internal errors")
        exit()
class ParsingError1(Exception):
    pass
class ParsingError2(Exception):
    pass
class ParsingError3(Exception):
    pass
class OtherError(Exception):
    pass

operations = ['MOV', 'ADD', 'SUB', 'MUL', 'DIV', 'READINT',
            'READSTR', 'PRINT', 'PRINTLN', 'LABEL', 'JUMP',
            'JUMPIFEQ', 'JUMPIFLT', 'CALL', 'RETURN','PUSH', 'POP']
var = r"^[A-Za-z$_&%][A-Za-z0-9$_&%]*$"
label = r"^@[A-Za-z$_&%][A-Za-z0-9$_&%]*$"
variables = {}
labels = {}
call_return_stack = []
data_stack = []
error_is_caught = False

def type_check_int(src):
    if src in variables:
        val = str(variables[src])
    else: val = str(src)
    return re.match(r"^[+-]?\d+$", src) is not None and not (len(val) > 1 and val.lstrip("+-").startswith("0"))
def type_check_str(src):
    if isinstance(src, str):
        if src in variables:
            val = variables[src]
            return val.startswith('"') and val.endswith('"')
        return re.match(r'^".*"$', src) is not None
    return False
def type_check(src):
    return type_check_int(src) or type_check_str(src)

def dst_src_adding(tag_name, tac, tag_type, text):
    if tac is not None:  
        tag = xml.SubElement(tac, tag_name)
        tag.set('type', tag_type)
        tag.text = str(text) if text is not None else ''
    else:
        raise ParsingError1
def tag_adding_type_ch(tag_name, tac, text):
    if type_check_int(text):
        dst_src_adding(tag_name, tac, 'integer', str(text))
    elif type_check_str(text):
        dst_src_adding(tag_name, tac, 'string', str(text).strip('"'))
    else:
        dst_src_adding(tag_name, tac, 'variable', str(text))

def to_indents(elem):
    str = xml.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(str)
    return reparsed.toprettyxml(indent="  ")

lines = file_content.splitlines()
first_line = lines[0] if lines else ""
if first_line.startswith('#'):
    name = re.sub(r'^\s*#\s*', '', first_line).strip()
else:
    name = "name"

program = xml.Element('program') 
program.set('name', name)
order = 1


for line in lines:
    line = line.strip()
    if not line or line.startswith('#'):
        continue
    try:
        splitted = line.split()
        if not splitted:
            continue
        operation = splitted[0].upper()
        if operation not in operations:
            raise ParsingError1
        tac = xml.SubElement(program, 'tac')
        tac.set('opcode', operation)
        tac.set('order', str(order))
        order += 1

        if operation == "MOV":
            if len(splitted) != 3:
                raise ParsingError2
            if re.match(label, splitted[1]):
                raise ParsingError3
            if not re.match(var, splitted[1]):
                raise OtherError
            if not (splitted[2] in variables or type_check(splitted[2])):
                raise OtherError
            variables[splitted[1]] = splitted[2] if splitted[2] in variables else str(splitted[2])
            dst_src_adding('dst', tac, 'variable', splitted[1])
            tag_adding_type_ch('src1', tac, splitted[2])

        elif operation in ['ADD','SUB', 'MUL', 'DIV']:
            if len(splitted) != 4:
                raise ParsingError2
            if re.match(label, splitted[1]):
                raise ParsingError3
            if not re.match(var, splitted[1]):
                raise OtherError 
            a = splitted[2]
            b = splitted[3]
            if (not (a in variables or type_check_int(a))) or \
               (not (b in variables or type_check_int(b))):
                raise OtherError
            val1 = int(variables.get(a, a))
            val2 = int(variables.get(b, b))
            if operation == 'ADD': 
                variables[splitted[1]] = str(val1 + val2)
            elif operation == 'SUB': 
                variables[splitted[1]] = str(val1 - val2)
            elif operation == 'MUL': 
                variables[splitted[1]] = str(val1 * val2)
            else:
                if val2 == 0:
                    raise OtherError
                variables[splitted[1]] = str(val1 // val2)  
            dst_src_adding('dst', tac, 'variable', splitted[1])
            tag_adding_type_ch('src1', tac, a)
            tag_adding_type_ch('src2', tac, b)

        elif operation in ['READINT', 'READSTR']:
            if len(splitted) != 2:
                raise ParsingError2
            if re.match(label, splitted[1]):
                raise ParsingError3
            if not re.match(var, splitted[1]):
                raise OtherError  
            if operation == 'READINT':
                try:
                    val = input()
                    int(val)
                    variables[splitted[1]] = val
                except ValueError:
                    raise ParsingError3
            else:
                inp = f'"{input()}"' 
                variables[splitted[1]] = inp 
            dst_src_adding('dst', tac, 'variable', splitted[1])
                
        elif operation in ['PRINT', 'PRINTLN']:
            if len(splitted) != 2:
                raise ParsingError2
            if re.match(label, splitted[1]):
                raise ParsingError3
            if not (re.match(var, splitted[1]) or type_check(splitted[1])):
                raise OtherError
            value = variables.get(splitted[1], splitted[1])
            if operation == 'PRINT':
                if isinstance(value, str) and value.startswith('"'):
                    print(value.strip('"'), end="") 
                else:
                    print(value, end="")             
            else:
                print(value.strip('"') if isinstance(value, str) and value.startswith('"') else value)    
            tag_adding_type_ch('src1', tac, splitted[1])
        
        elif operation in ['LABEL', 'JUMP']:
            if len(splitted) != 2:
                raise ParsingError2
            if re.match(var, splitted[1]):
                raise ParsingError3
            if not re.match(label, splitted[1]):
                raise OtherError
            if operation == 'LABEL':
                labels[splitted[1]] = order - 1
            else:
                if splitted[1] not in labels:
                    raise ParsingError3
                order = labels[splitted[1]]
            dst_src_adding('dst', tac, 'label', splitted[1])

        elif operation in ['JUMPIFEQ', 'JUMPIFLT']:
            if len(splitted) != 4:
                raise ParsingError2
            if re.match(var, splitted[1]):
                raise ParsingError3
            if not re.match(label, splitted[1]):
                raise OtherError
            a = splitted[2]
            b = splitted[3]
            if (not (a in variables or type_check(a))) or \
               (not (b in variables or type_check(b))):
                raise OtherError
            val1 = variables.get(a, a)
            val2 = variables.get(b, b)
            if type_check_int(val1) and type_check_int(val2):
                val1 = int(val1)
                val2 = int(val2)
            elif type_check_str(val1) and type_check_str(val2):
                val1 = str(val1).strip('"')
                val2 = str(val2).strip('"')
            else:
                raise OtherError
            if operation == 'JUMPIFEQ':
                if val1 == val2: 
                    order = labels[splitted[1]]
            else:
                if val1 < val2: 
                    order = labels[splitted[1]]
            dst_src_adding('dst', tac, 'label', splitted[1])
            tag_adding_type_ch('src1', tac, a)
            tag_adding_type_ch('src2', tac, b)
        
        elif operation == 'CALL':
            if len(splitted) != 2:
                raise ParsingError2
            if re.match(var, splitted[1]):
                raise ParsingError3
            if not re.match(label, splitted[1]):
                raise OtherError
            call_return_stack.append(order)
            order = labels[splitted[1]]
            dst_src_adding('dst', tac, 'label', splitted[1])

        elif operation == 'RETURN':
            if len(splitted) != 1:
                raise ParsingError2
            if not call_return_stack:
                raise OtherError
            order = call_return_stack.pop()
            dst_src_adding('dst', tac, 'return', str(order))

        elif operation == 'PUSH':
            if len(splitted) != 2:
                raise ParsingError2
            if re.match(label, splitted[1]):
                raise ParsingError3
            if not (re.match(var, splitted[1]) or type_check(splitted[1])):
                raise OtherError
            value = variables.get(splitted[1], splitted[1])
            data_stack.append(str(value))
            tag_adding_type_ch('src1', tac, splitted[1])

        elif operation == 'POP':
            if len(splitted) != 2:
                raise ParsingError2
            if re.match(label, splitted[1]):
                raise ParsingError3
            if not re.match(var, splitted[1]):
                raise OtherError
            if not data_stack:
                raise OtherError
            variables[splitted[1]] = data_stack.pop()
            dst_src_adding('dst', tac, 'variable', splitted[1])

    except ParsingError1:
        print(f'Parsing Error: Unknown operation code of instruction at line {order}')
        error_is_caught = True
    except ParsingError2:
        print(f'Parsing Error: Missing or excessing operand of instruction at line {order}')
        error_is_caught = True
    except ParsingError3:
        print(f'Parsing Error: Bad kind of operand at line {order}')
        error_is_caught = True
    except OtherError:
        print(f'Other Error: Lexical or syntax error at line {order}')
        error_is_caught = True

xml_content = to_indents(program)
xml_content = '\n'.join(line for line in xml_content.split('\n') if line.strip())


if ippe_file== '-':
    with open("out.xml", 'w', encoding='utf-8') as f:
        f.write(xml_content)
else:
# first occurence of .
    output_file = f"{ippe_file.rsplit('.', 1)[0]}.xml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
print()
if error_is_caught == True:
    print(1)
else: print(0)