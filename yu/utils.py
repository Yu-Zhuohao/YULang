import re
import yu.global_storage as gs
import yu.global_definition as gd
import yu.calc as calc

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