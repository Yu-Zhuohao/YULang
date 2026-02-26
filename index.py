import sys
import os
import re
import yu.global_definition as gd
import yu.global_storage as gs
import yu.calc as calc

def aboutM():
    print(gd.aboutM)
    
def replace_placeholders(expr):
    def repl(match):
        name = match.group(1)
        if name in gs.constants:
            return str(gs.constants[name])
        elif name in gs.variables:
            return str(gs.variables[name])
        else:
            raise NameError(gd.name_undefinedM.format(name))
    pattern = r'%\{([^}]+)\}%'
    result = re.sub(pattern, repl, expr)
    pattern2 = r'%([a-zA-Z_][a-zA-Z0-9_]*)%'
    result = re.sub(pattern2, repl, result)
    return result

def main():
    aboutM()
    while True:
        usr_input = input(">>> ")
        usr_input_strip = usr_input.strip()
        if not usr_input_strip:
            continue
        space_index = usr_input_strip.find(' ')
        if space_index != -1:
            first_part = usr_input_strip[:space_index]
        else:
            first_part = usr_input_strip
        if first_part not in gd.keywords:
            print(gd.unk_cmdM)
            continue
        if usr_input_strip == "quit()" or usr_input_strip == "exit()":
            print(gd.quitM)
            sys.exit(0)
        elif usr_input_strip.startswith("yu --version"):
            print(gd.versionM)
        elif usr_input_strip == "help":
            print(gd.helpM)
        if usr_input_strip.startswith("set"):
            parts = usr_input_strip.split()
            if len(parts) < 4:
                print(gd.set_syntaxM)
                continue
            name = parts[1]
            op = parts[2]
            value_expr = ' '.join(parts[3:])
            try:
                expr_filled = replace_placeholders(value_expr)
                value = calc.calc(expr_filled)
                if isinstance(value, str) and value.startswith("Error"):
                    print(value)
                    continue
            except Exception as e:
                print(f"{gd.value_errorM}: {e}")
                continue
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
            continue
        if usr_input_strip.startswith("calc"):
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
            continue

if __name__ == "__main__":
    main()