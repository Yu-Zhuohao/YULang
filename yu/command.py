import os
import yu.global_definition as gd
import yu.global_storage as gs
import yu.calc as calc
import yu.keywords
from yu.utils import replace_placeholders
from yu.keywords.sys.out_cmd import parse_args as parse_sys_out_args
from yu.keywords.if_cmd import execute_if
from yu.keywords.rep_cmd import execute_rep

def handle_link(usr_input_strip):
    parts = usr_input_strip.split()
    if len(parts) < 2:
        print(gd.import_syntaxM)
        return True
    module_name = parts[1]
    if len(parts) >= 4 and parts[2] == "as":
        alias = parts[3]
    else:
        alias = module_name
    if module_name == "sys":
        if alias not in gs.imports:
            gs.imports[alias] = yu.keywords.sys
            print(gd.import_successM.format(module_name))
        else:
            print(f"Module already imported as {alias}")
    else:
        print(gd.module_not_foundM.format(module_name))
    return True

def handle_set(usr_input_strip):
    parts = usr_input_strip.split()
    if len(parts) < 4:
        print(gd.set_syntaxM)
        return True
    name = parts[1]
    op = parts[2]
    value_expr = ' '.join(parts[3:])
    try:
        expr_filled = replace_placeholders(value_expr)
        # 检查是否是字面值 True/False
        if expr_filled == "True":
            value = True
        elif expr_filled == "False":
            value = False
        elif (expr_filled.startswith('"') and expr_filled.endswith('"')) or (expr_filled.startswith("'") and expr_filled.endswith("'")):
            value = expr_filled[1:-1]
        else:
            value = calc.calc(expr_filled)
            if isinstance(value, str) and value.startswith("Error"):
                print(value)
                return True
    except Exception as e:
        print(f"{gd.value_errorM}: {e}")
        return True
    if op == "::":
        if name in gs.constants:
            print(gd.const_existsM.format(name))
        else:
            gs.constants[name] = value
            print(gd.const_definedM.format(name, value))
    elif op == ">>":
        gs.variables[name] = value
        print(gd.var_definedM.format(name, value))
    else:
        print(gd.set_syntaxM)
    return True

def handle_calc(usr_input_strip):
    expr = usr_input_strip[4:].strip()
    if not expr:
        print(gd.e1)
    else:
        try:
            expr_filled = replace_placeholders(expr)
            result = calc.calc(expr_filled)
            print(result)
        except Exception as e:
            print(f"{gd.calc_errorM}: {e}")
    return True

def handle_module_call(usr_input_strip):
    dot_index = usr_input_strip.find('.')
    module_alias = usr_input_strip[:dot_index]
    rest = usr_input_strip[dot_index + 1:].strip()
    space_index = rest.find(' ')
    if space_index != -1:
        function_name = rest[:space_index]
    else:
        function_name = rest
    if module_alias in gs.imports:
        module = gs.imports[module_alias]
        if hasattr(module, function_name):
            func = getattr(module, function_name)
            expr = usr_input_strip[dot_index + len(function_name) + 2:].strip()
            if not expr:
                func()
            else:
                args = parse_sys_out_args(expr)
                func(*args)
        else:
            print(f"{gd.unk_cmdM}")
    else:
        print(f"{gd.unk_cmdM}")
    return True

def handle_script(filename):
    if not os.path.exists(filename):
        print(gd.script_not_foundM.format(filename))
        return True
    with open(filename, 'r') as f:
        script_content = f.read()
    if not script_content.strip().endswith("_yuE_"):
        print(gd.script_incompleteM)
        return True
    print(gd.script_execM.format(filename))
    for line in script_content.split('\n'):
        line = line.strip()
        if line and not line.startswith("#") and line != "_yuE_":
            exec_line = line
            if exec_line.startswith("calc"):
                expr = exec_line[4:].strip()
                if expr:
                    try:
                        expr_filled = replace_placeholders(expr)
                        result = calc.calc(expr_filled)
                        print(result)
                    except Exception as e:
                        print(f"{gd.calc_errorM}: {e}")
            elif exec_line.startswith("set"):
                parts = exec_line.split()
                if len(parts) >= 4:
                    name = parts[1]
                    op = parts[2]
                    value_expr = ' '.join(parts[3:])
                    try:
                        expr_filled = replace_placeholders(value_expr)
                        # 检查是否是字面值 True/False
                        if expr_filled == "True":
                            value = True
                        elif expr_filled == "False":
                            value = False
                        elif (expr_filled.startswith('"') and expr_filled.endswith('"')) or (expr_filled.startswith("'") and expr_filled.endswith("'")):
                            value = expr_filled[1:-1]
                        else:
                            value = calc.calc(expr_filled)
                            if isinstance(value, str) and value.startswith("Error"):
                                continue
                        if op == "::":
                            if name not in gs.constants:
                                gs.constants[name] = value
                        elif op == ">>":
                            gs.variables[name] = value
                    except Exception as e:
                        pass
            elif exec_line.startswith("link"):
                parts = exec_line.split()
                if len(parts) >= 2:
                    module_name = parts[1]
                    if len(parts) >= 4 and parts[2] == "as":
                        alias = parts[3]
                    else:
                        alias = module_name
                    if module_name == "sys":
                        if alias not in gs.imports:
                            gs.imports[alias] = yu.keywords.sys
            elif exec_line.startswith("if"):
                execute_if(exec_line)
            elif exec_line.startswith("rep"):
                execute_rep(exec_line)
            elif '.' in exec_line:
                dot_index = exec_line.find('.')
                exec_module = exec_line[:dot_index]
                rest = exec_line[dot_index + 1:].strip()
                space_index = rest.find(' ')
                if space_index != -1:
                    exec_func = rest[:space_index]
                else:
                    exec_func = rest
                if exec_module in gs.imports:
                    exec_module_obj = gs.imports[exec_module]
                    if hasattr(exec_module_obj, exec_func):
                        exec_func_obj = getattr(exec_module_obj, exec_func)
                        expr = exec_line[dot_index + len(exec_func) + 2:].strip()
                        if expr:
                            args = parse_sys_out_args(expr)
                            exec_func_obj(*args)
                        else:
                            exec_func_obj()
    return True