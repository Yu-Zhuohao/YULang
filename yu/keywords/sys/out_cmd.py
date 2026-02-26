import yu.global_storage as gs
import yu.calc as calc
from yu.utils import replace_placeholders

def parse_args(expr):
    result = ""
    current_expr = ""
    in_string = False
    string_char = None
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch in ('"', "'"):
            if not in_string:
                in_string = True
                string_char = ch
                current_expr += ch
            elif ch == string_char:
                current_expr += ch
                in_string = False
                string_char = None
            else:
                current_expr += ch
        elif ch == '+' and not in_string:
            if current_expr.strip():
                arg = current_expr.strip()
                if arg.startswith('"') or arg.startswith("'"):
                    try:
                        string_value = eval(arg)
                        string_filled = replace_placeholders(string_value)
                        result += string_filled
                    except:
                        result += arg
                else:
                    try:
                        arg_filled = replace_placeholders(arg)
                        value = calc.calc(arg_filled)
                        if isinstance(value, str) and value.startswith("Error"):
                            result += arg_filled
                        else:
                            result += str(value)
                    except Exception as e:
                        try:
                            arg_filled = replace_placeholders(arg)
                            result += arg_filled
                        except:
                            result += arg
                current_expr = ""
        elif not ch.isspace() or in_string:
            current_expr += ch
        i += 1
    if current_expr.strip():
        arg = current_expr.strip()
        if arg.startswith('"') or arg.startswith("'"):
            try:
                string_value = eval(arg)
                string_filled = replace_placeholders(string_value)
                result += string_filled
            except:
                result += arg
        else:
            try:
                arg_filled = replace_placeholders(arg)
                value = calc.calc(arg_filled)
                if isinstance(value, str) and value.startswith("Error"):
                    result += arg_filled
                else:
                    result += str(value)
            except Exception as e:
                try:
                    arg_filled = replace_placeholders(arg)
                    result += arg_filled
                except:
                    result += arg
    return [result]

def out(*args):
    result = ""
    for arg in args:
        if isinstance(arg, str):
            result += arg
        else:
            result += str(arg)
    print(result)