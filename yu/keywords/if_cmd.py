import re
import yu.global_storage as gs
import yu.global_definition as gd
import yu.calc as calc
from yu.utils import replace_placeholders
from yu.logic import logical_and, logical_or


def parse_single_condition(condition_str):
    condition_str = condition_str.strip()
    
    if condition_str == "True":
        return True, None
    if condition_str == "False":
        return False, None
    
    if ":=:" in condition_str:
        parts = condition_str.split(":=:", 1)
        left = parts[0].strip()
        right = parts[1].strip()
        
        if left in gs.constants:
            left_val = gs.constants[left]
        elif left in gs.variables:
            left_val = gs.variables[left]
        elif left.startswith('%') and left.endswith('%'):
            name = left[1:-1]
            if name in gs.constants:
                left_val = gs.constants[name]
            elif name in gs.variables:
                left_val = gs.variables[name]
            else:
                return None, f"Undefined variable: {name}"
        else:
            try:
                right_filled = replace_placeholders(left)
                left_val = calc.calc(right_filled)
                if isinstance(left_val, str) and left_val.startswith("Error"):
                    return None, f"Cannot evaluate left side: {left_val}"
            except Exception as e:
                return None, f"Undefined or invalid left side: {left}"
        
        if right == "True":
            right_val = True
        elif right == "False":
            right_val = False
        elif right.startswith('%') and right.endswith('%'):
            name = right[1:-1]
            if name in gs.constants:
                right_val = gs.constants[name]
            elif name in gs.variables:
                right_val = gs.variables[name]
            else:
                return None, f"Undefined variable: {name}"
        else:
            try:
                right_filled = replace_placeholders(right)
                right_val = calc.calc(right_filled)
                if isinstance(right_val, str) and right_val.startswith("Error"):
                    return None, f"Cannot evaluate right side: {right_val}"
            except Exception as e:
                return None, f"Invalid right side: {right}"
        
        return left_val == right_val, None
    
    if condition_str.startswith('%') and condition_str.endswith('%'):
        name = condition_str[1:-1]
        if name in gs.constants:
            val = gs.constants[name]
            return bool(val), None
        elif name in gs.variables:
            val = gs.variables[name]
            return bool(val), None
        else:
            return None, f"Undefined variable: {name}"
    
    if condition_str in gs.constants:
        val = gs.constants[condition_str]
        return bool(val), None
    if condition_str in gs.variables:
        val = gs.variables[condition_str]
        return bool(val), None
    
    try:
        expr_filled = replace_placeholders(condition_str)
        val = calc.calc(expr_filled)
        if isinstance(val, str) and val.startswith("Error"):
            return None, f"Cannot evaluate condition: {val}"
        return bool(val), None
    except:
        return None, f"Invalid condition: {condition_str}"

def parse_condition(condition_str):
    condition_str = condition_str.strip()
    
    tokens = []
    current_token = ""
    paren_count = 0
    
    for char in condition_str:
        if char == '(':
            paren_count += 1
            if current_token.strip():
                tokens.append(current_token.strip())
            current_token = "("
        elif char == ')':
            paren_count -= 1
            current_token += ")"
            if paren_count == 0:
                tokens.append(current_token.strip())
                current_token = ""
        elif char == ' ' and paren_count == 0:
            if current_token.strip():
                tokens.append(current_token.strip())
            current_token = ""
        else:
            current_token += char
    
    if current_token.strip():
        tokens.append(current_token.strip())
    
    or_indices = []
    for i, token in enumerate(tokens):
        if token.lower() == 'or':
            or_indices.append(i)
    
    if or_indices:
        left_tokens = tokens[:or_indices[0]]
        right_tokens = tokens[or_indices[0] + 1:]
        
        left_result, error = parse_condition(' '.join(left_tokens))
        if error:
            return None, error
        
        right_result, error = parse_condition(' '.join(right_tokens))
        if error:
            return None, error
        
        return logical_or(left_result, right_result), None
    
    and_indices = []
    for i, token in enumerate(tokens):
        if token.lower() == 'and':
            and_indices.append(i)
    
    if and_indices:
        left_tokens = tokens[:and_indices[0]]
        right_tokens = tokens[and_indices[0] + 1:]
        
        left_result, error = parse_condition(' '.join(left_tokens))
        if error:
            return None, error
        
        right_result, error = parse_condition(' '.join(right_tokens))
        if error:
            return None, error
        
        return logical_and(left_result, right_result), None
    
    return parse_single_condition(condition_str)


def parse_block(block_str):
    block_str = block_str.strip()
    
    if not block_str.startswith("=>"):
        return None, "Block must start with '=>'"
    
    brace_start = block_str.find('{')
    if brace_start == -1:
        return None, "Block must be enclosed in { }"
    
    brace_count = 0
    in_quotes = False
    quote_char = None
    i = brace_start
    while i < len(block_str):
        char = block_str[i]
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
        elif char == quote_char and in_quotes:
            in_quotes = False
        elif char == '{' and not in_quotes:
            brace_count += 1
        elif char == '}' and not in_quotes:
            brace_count -= 1
            if brace_count == 0:
                break
        i += 1
    
    if i >= len(block_str):
        return None, "Block must be enclosed in { }"
    
    commands_str = block_str[brace_start + 1:i].strip()
    
    commands = []
    if commands_str:
        current_cmd = ""
        in_quotes = False
        quote_char = None
        inner_brace_count = 0
        for char in commands_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current_cmd += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                current_cmd += char
            elif char == '{' and not in_quotes:
                inner_brace_count += 1
                current_cmd += char
            elif char == '}' and not in_quotes:
                inner_brace_count -= 1
                current_cmd += char
            elif char == ';' and not in_quotes and inner_brace_count == 0:
                cmd = current_cmd.strip()
                if cmd:
                    commands.append(cmd)
                current_cmd = ""
            else:
                current_cmd += char
        if current_cmd.strip():
            commands.append(current_cmd.strip())
    
    return commands, None


def parse_single_condition_branch(cmd_str, start_pos=0):
    cmd_str = cmd_str[start_pos:].strip()
    
    then_pos = cmd_str.find(" then ")
    if then_pos == -1:
        return None, 0, "Missing 'then' keyword. Format: if/elif <condition> <True|False> then => {}"
    
    condition_and_trigger = cmd_str[:then_pos].strip()
    block_part = cmd_str[then_pos + 6:].strip()
    
    parts = condition_and_trigger.split()
    
    if parts and parts[0] in ["if", "elif"]:
        parts = parts[1:]
    
    if len(parts) < 2:
        return None, 0, "Invalid format. Expected: if/elif <condition> <True|False> then => {}"
    
    trigger = parts[-1]
    if trigger not in ["True", "False"]:
        return None, 0, "Trigger must be 'True' or 'False'"
    
    condition_str = ' '.join(parts[:-1]).strip()
    
    condition_result, error = parse_condition(condition_str)
    if error:
        return None, 0, error
    
    if not block_part.startswith("=>"):
        return None, 0, "Block must start with '=>'"
    
    brace_start = block_part.find('{')
    if brace_start == -1:
        return None, 0, "Block must be enclosed in { }"
    
    brace_count = 0
    i = brace_start
    while i < len(block_part):
        if block_part[i] == '{':
            brace_count += 1
        elif block_part[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                break
        i += 1
    
    if i >= len(block_part):
        return None, 0, "Block must be enclosed in { }"
    
    commands_str = block_part[brace_start + 1:i].strip()
    
    commands = []
    if commands_str:
        current_cmd = ""
        in_quotes = False
        quote_char = None
        for char in commands_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current_cmd += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                current_cmd += char
            elif char == ';' and not in_quotes:
                cmd = current_cmd.strip()
                if cmd:
                    commands.append(cmd)
                current_cmd = ""
            else:
                current_cmd += char
        if current_cmd.strip():
            commands.append(current_cmd.strip())
    
    block_end_in_cmd_str = then_pos + 6 + (i + 1)
    
    return {
        'condition': condition_result,
        'trigger': trigger == "True",
        'commands': commands
    }, start_pos + block_end_in_cmd_str, None


def parse_else_branch(cmd_str, start_pos=0):
    """
    解析else分支
    返回: (commands, next_pos, error)
    """
    cmd_str = cmd_str[start_pos:].strip()
    
    # 检查是否以else开头
    if not cmd_str.startswith("else"):
        return None, 0, "Expected 'else' keyword"
    
    # 移除else
    block_part = cmd_str[4:].strip()
    
    # 解析block - 手动查找匹配的大括号
    if not block_part.startswith("=>"):
        return None, 0, "Block must start with '=>'"
    
    brace_start = block_part.find('{')
    if brace_start == -1:
        return None, 0, "Block must be enclosed in { }"
    
    # 查找匹配的右大括号
    brace_count = 0
    i = brace_start
    while i < len(block_part):
        if block_part[i] == '{':
            brace_count += 1
        elif block_part[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                break
        i += 1
    
    if i >= len(block_part):
        return None, 0, "Block must be enclosed in { }"
    
    # 提取命令内容
    commands_str = block_part[brace_start + 1:i].strip()
    
    # 按分号分割命令
    commands = []
    if commands_str:
        for cmd in commands_str.split(';'):
            cmd = cmd.strip()
            if cmd:
                commands.append(cmd)
    
    # 计算block在原始字符串中的结束位置
    block_end_in_cmd_str = 4 + (i + 1)  # 4 是 "else" 的长度，i + 1 是右大括号的位置
    
    return commands, start_pos + block_end_in_cmd_str, None


def parse_if_command_full(cmd_str):
    """
    解析if命令（支持elif和else）
    格式: 
    - if <condition> <True|False> then => {}
    - if <condition> <True|False> then => {} else => {}
    - if <condition> <True|False> then => {} elif <condition> <True|False> then => {}
    - if <condition> <True|False> then => {} elif <condition> <True|False> then => {} else => {}
    返回: (result_dict, error)
    """
    cmd_str = cmd_str.strip()
    
    # 检查是否以if开头
    if not cmd_str.startswith("if "):
        return None, "Command must start with 'if'"
    
    # 解析if分支
    current_pos = 3  # 跳过"if "
    if_branch, current_pos, error = parse_single_condition_branch(cmd_str, current_pos)
    if error:
        return None, error
    
    result = {
        'if_branch': if_branch,
        'elif_branches': [],
        'else_commands': None
    }
    
    # 解析elif分支
    remaining = cmd_str[current_pos:].strip()
    while remaining.startswith("elif "):
        elif_branch, current_pos, error = parse_single_condition_branch(cmd_str, current_pos)
        if error:
            return None, error
        result['elif_branches'].append(elif_branch)
        remaining = cmd_str[current_pos:].strip()
    
    # 解析else分支
    remaining = cmd_str[current_pos:].strip()
    if remaining.startswith("else"):
        else_commands, current_pos, error = parse_else_branch(cmd_str, current_pos)
        if error:
            return None, error
        result['else_commands'] = else_commands
    
    return result, None


def execute_if(cmd_str):
    cmd_str = cmd_str.strip()
    if not cmd_str.startswith("if "):
        cmd_str = "if " + cmd_str
    result, error = parse_if_command_full(cmd_str)
    if error:
        print(f"Error: {error}")
        return False
    
    condition_is_true = result['if_branch']['condition']
    trigger_when_true = result['if_branch']['trigger']
    
    should_execute_if = (condition_is_true and trigger_when_true) or \
                        (not condition_is_true and not trigger_when_true)
    
    if should_execute_if:
        execute_commands(result['if_branch']['commands'])
        return True
    
    for elif_branch in result['elif_branches']:
        condition_is_true = elif_branch['condition']
        trigger_when_true = elif_branch['trigger']
        
        should_execute_elif = (condition_is_true and trigger_when_true) or \
                              (not condition_is_true and not trigger_when_true)
        
        if should_execute_elif:
            execute_commands(elif_branch['commands'])
            return True
    
    if result['else_commands'] is not None:
        execute_commands(result['else_commands'])
    
    return True


def execute_commands(commands):
    from yu import command
    for cmd in commands:
        if cmd == "brk()":
            from yu.public import brk
            brk()
            return
        elif cmd == "cont()":
            from yu.public import cont
            cont()
            return
        elif cmd.startswith("calc"):
            command.handle_calc(cmd)
        elif cmd.startswith("set"):
            command.handle_set(cmd)
        elif cmd.startswith("link"):
            command.handle_link(cmd)
        elif cmd.startswith("if"):
            execute_if(cmd)
        elif cmd.startswith("rep"):
            from yu.keywords.rep_cmd import execute_rep
            execute_rep(cmd)
        elif '.' in cmd:
            command.handle_module_call(cmd)
