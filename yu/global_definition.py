aboutM = "YULang\nType \"help\" for help."
quitM = "Goodbye!"
versionM = "YULang - 26.8.101"
keywords = ['help', 'quit()', 'exit()', 'yu', 'calc', 'set', 'link', 'if', 'rep']
unk_cmdM = "Unknown Command. Type \"help\" for available commands."
helpM = """YULang Help - Available Commands:

Basic Commands:
  help                    显示帮助信息
  quit() / exit()         退出程序
  yu --version            显示版本信息

Variables & Constants:
  set <name> :: <value>   定义常量（不可重新定义）
  set <name> >> <value>   定义变量（可重新定义）

Calculation:
  calc <expression>       计算数学表达式
                          支持运算符: +, -, *, /, %, ^
                          支持括号: (, )

Condition:
  if <condition> <True|False> then => {}
                          条件判断命令
                          condition: True/False/变量/常量 :=: 值
                          支持逻辑运算符: and, or
                          支持elif和else
                          支持brk()中断循环和cont()跳过本次循环
                          示例: if %x% :=: 10 True then => { sys.out "x=10" }
                          示例: if %x% > 5 and %x% < 15 True then => { sys.out "x在5和15之间" }
                          示例: if %x% :=: 10 True then => { cmd } elif ... else => { cmd }

Loop:
  rep <condition> <True|False> <int|infinite> => {}
                          循环命令
                          condition: 与if语句相同，支持and和or
                          <int>: 循环次数（正整数）
                          infinite: 无限循环
                          支持wait <int>s/ms（等待秒/毫秒）
                          支持brk()中断循环和cont()跳过本次循环
                          示例: rep True True 5 => { sys.out "Hello"; wait 1s }
                          示例: rep %i% < 10 True 10 => { if %i% :=: 5 True then => { brk() } }

Flow Control:
  brk()                   中断循环（在if/elif/else/rep语句中）
  cont()                  跳过本次循环，继续下一次（在if/elif/else/rep语句中）

Logical Operators:
  and                     逻辑与（短路求值）
  or                      逻辑或（短路求值）
                          示例: if %a% > 5 and %b% < 10 True then => { ... }
                          示例: if %x% :=: 1 or %x% :=: 2 True then => { ... }

Modules:
  link <module>           导入模块
  link <module> as <alias> 导入模块并指定别名

Scripts:
  yu <filename>           运行脚本文件（.yu）
                          脚本结尾必须包含 _yuE_

Variables Usage:
  %name% 或 %{name}%      使用变量/常量的值

Examples:
  set x >> 10             定义变量x为10
  calc %x% + 5            计算10 + 5 = 15
  link sys                导入sys模块
  sys.out "Hello"         输出Hello
  if %x% :=: 10 True then => { sys.out "Equal" }  条件判断
  rep True True 3 => { sys.out "Loop"; wait 0.5s }  循环3次
"""
e1 = "Warning: Pls type an expression"
e2 = "ArgumentError: Divisor cannot be zero"
e3 = "ExpressionError: Insufficient number of operations"
e5 = "ExpressionError: Extra number of operations"
const_definedM = "constant {} defined as {}"
var_definedM = "variable {} defined as {}"
const_existsM = "constant {} already exists，cannot be redefined"
set_syntaxM = "Error,usage: set <name> :: <value> or set <name> >> <value>"
name_undefinedM = "Undefined name: {}"
value_errorM = "ValueError"
calc_errorM = "Error"
illegal_charM = "Unexpected character: {}"
invalid_numberM = "Unexpected number format"
paren_mismatchM = "Parentheses do not match"
import_successM = "Module {} imported successfully"
import_syntaxM = "Error,usage: link <module> or link <module> as <name>"
module_not_foundM = "Module {} not found"
script_not_foundM = "Script file {} not found"
script_incompleteM = "Error: Script file incomplete, missing _yuE_ at the end"
script_execM = "Executing script: {}"