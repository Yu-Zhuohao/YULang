#Basic Information:
Project name:YU Language(YUlang)
Author:[YuZhuohao]
License:[Undetermined]
Project start time: 2026.02.25
Project version: 26.08.01  (As of 2026.02.25)

## 项目结构
```
yu/
├── index.py              # 主程序入口
├── README.MD             # 使用文档
└── yu/
    ├── __init__.py
    ├── command.py        # 命令处理模块
    ├── utils.py          # 工具函数
    ├── calc.py           # 计算器模块
    ├── global_definition.py  # 全局定义
    ├── global_storage.py     # 全局存储
    └── keywords/
        ├── __init__.py
        └── sys/
            ├── __init__.py
            └── out_cmd.py     # sys.out命令
```

# 使用文档

## 运行方式
```bash
python3 index.py
```

## 命令列表

### help
显示帮助信息
```
>>> help
```

### quit() / exit()
退出程序
```
>>> quit()
>>> exit()
```

### yu --version
显示版本信息
```
>>> yu --version
```

### calc
计算数学表达式
```
>>> calc 1 + 2 * 3
>>> calc -5 + 3
>>> calc 3 + -2
```

### set
定义常量或变量
```
>>> set <name> :: <value>
>>> set <name> >> <value>
```

### link
导入模块
```
>>> link <module>
>>> link <module> as <alias>
```

### yu
运行脚本文件
```
>>> yu <filename>
```

## 模块系统

### 导入模块
使用link命令导入模块，支持别名
```
>>> link sys
>>> Module sys imported successfully
>>> link sys as s
>>> Module sys imported successfully
```

### sys模块
sys模块提供输出功能

#### sys.out
输出内容，支持字符串、数字、变量、常量及其拼接
```
>>> sys.out "Hello World"
Hello World
>>> sys.out "Value: " + %x%
Value: 10
>>> sys.out "a" + "b"
ab
```

## 脚本文件

### 创建脚本文件
创建.yu脚本文件，文件结尾必须包含_yuE_
```
link sys
set name :: "YU"
sys.out "Hello from " + %name% + "!"
_yuE_
```

### 运行脚本
```
>>> yu script.yu
Executing script: script.yu
Hello from YU!
```

### 脚本命令
脚本支持以下命令：
- link：导入模块
- set：定义常量或变量
- calc：计算表达式
- sys.out：输出内容
- if/elif/else：条件判断
- rep：循环

### 脚本示例
```
link sys
set a :: 5
set b >> 3
sys.out "Hello from YU script!"
calc %a% + %b%
sys.out "Result: " + %a%
_yuE_
```

输出：
```
Hello from YU script!
8
Result: 5
```

## 条件判断

### if命令
进行条件判断，对缩进不敏感

#### 语法格式
```
if <condition> <True|False> then => {}
if <condition> <True|False> then => {} else => {}
if <condition> <True|False> then => {} elif <condition> <True|False> then => {}
if <condition> <True|False> then => {} elif <condition> <True|False> then => {} else => {}
```

#### 参数说明
- `condition`: 条件表达式，支持以下格式：
  - `True` / `False`：字面布尔值
  - `变量/常量名`：使用变量或常量的布尔值
  - `变量/常量 :=: True/False/值`：比较变量/常量与指定值是否相等
  - 支持逻辑运算符：`and`、`or`
- `True|False`：触发条件
  - `True`：当condition为真时执行
  - `False`：当condition为假时执行
- `{}`：命令块，用分号分隔多个命令

#### 使用示例

**示例1：简单的条件判断**
```
set x >> 10
if %x% :=: 10 True then => { sys.out "x is 10" }
if %x% :=: 5 True then => { sys.out "x is 5" }
```

**示例2：使用变量作为条件**
```
set flag >> True
if %flag% True then => { sys.out "flag is true" }
set flag >> False
if %flag% False then => { sys.out "flag is false" }
```

**示例3：在脚本中使用if**
```
link sys
set age >> 18
if %age% :=: 18 True then => { sys.out "You are 18 years old" }
if %age% :=: 18 False then => { sys.out "You are not 18 years old" }
_yuE_
```

**示例4：嵌套条件**
```
link sys
set x >> 10
set y >> 20
if %x% :=: 10 True then => { if %y% :=: 20 True then => { sys.out "x=10 and y=20" } }
_yuE_
```

**示例5：使用表达式作为条件**
```
link sys
set a >> 5
set b >> 3
if %a% :=: %b% False then => { sys.out "a and b are not equal" }
_yuE_
```

#### 注意事项
- if命令对缩进不敏感，可以使用任意缩进格式
- 命令块中的命令用分号分隔
- 支持嵌套if语句
- 支持elif和else
- 在脚本和交互模式中都可以使用

#### elif和else使用示例

**示例6：使用else**
```
link sys
set x >> 5
if %x% :=: 10 True then => { sys.out "x is 10" } else => { sys.out "x is not 10" }
```

**示例7：使用elif**
```
link sys
set score >> 85
if %score% :=: 100 True then => { sys.out "Perfect!" } elif %score% >= 90 True then => { sys.out "Excellent!" } elif %score% >= 60 True then => { sys.out "Good!" } else => { sys.out "Try again!" }
```

**示例8：完整的if-elif-else链**
```
link sys
set day >> 3
if %day% :=: 1 True then => { sys.out "Monday" } elif %day% :=: 2 True then => { sys.out "Tuesday" } elif %day% :=: 3 True then => { sys.out "Wednesday" } elif %day% :=: 4 True then => { sys.out "Thursday" } elif %day% :=: 5 True then => { sys.out "Friday" } elif %day% :=: 6 True then => { sys.out "Saturday" } elif %day% :=: 7 True then => { sys.out "Sunday" } else => { sys.out "Invalid day" }
```

**示例9：使用and运算符**
```
link sys
set age >> 20
set score >> 85
if %age% >= 18 and %score% >= 60 True then => { sys.out "成年且及格" }
```

**示例10：使用or运算符**
```
link sys
set day >> 6
if %day% :=: 6 or %day% :=: 7 True then => { sys.out "周末" } else => { sys.out "工作日" }
```

**示例11：组合使用and和or**
```
link sys
set age >> 25
set income >> 50000
set credit >> 700
if %age% >= 18 and %income% >= 30000 and %credit% >= 650 True then => { sys.out "符合贷款条件" } else => { sys.out "不符合贷款条件" }
```

## 循环

### rep命令
进行循环操作，支持有限循环和无限循环

#### 语法格式
```
rep <condition> <True|False> <int|infinite> => {}
```

#### 参数说明
- `condition`: 条件表达式，与if语句的condition格式相同，支持and和or
- `True|False`: 触发条件
  - `True`：当condition为真时执行循环
  - `False`：当condition为假时执行循环
- `<int|infinite>`: 循环次数
  - 正整数：循环指定次数
  - `infinite`：无限循环（只能使用这个字符串）
- `{}`: 命令块，用分号分隔多个命令

#### wait命令
在循环中使用wait命令可以暂停执行
- `wait <int>s`：等待int秒（支持浮点数）
- `wait <int>ms`：等待int毫秒（支持浮点数）

#### 使用示例

**示例1：有限循环**
```
link sys
set count >> 3
rep True True %count% => { sys.out "Loop iteration"; wait 1s }
```
输出：
```
Loop iteration
Loop iteration
Loop iteration
```

**示例2：使用毫秒级等待**
```
link sys
rep True True 5 => { sys.out "Fast loop"; wait 500ms }
```

**示例3：条件触发循环**
```
link sys
set flag >> True
if %flag% True then => { rep True True 3 => { sys.out "Running" } }
```

**示例4：在脚本中使用循环**
```
link sys
set n >> 5
set i >> 0
rep %i% < %n% True %n% => { set i >> %i% + 1; sys.out "i = %i%"; wait 0.5s }
_yuE_
```

**示例5：嵌套循环**
```
link sys
rep True True 3 => { sys.out "Outer loop"; rep True True 2 => { sys.out "  Inner loop" }; wait 1s }
```

**示例6：在循环中使用brk()**
```
link sys
set i >> 0
rep True True 10 => { set i >> %i% + 1; if %i% :=: 5 True then => { brk() }; sys.out "i = %i%" }
```
输出：
```
i = 1
i = 2
i = 3
i = 4
```

**示例7：在循环中使用cont()**
```
link sys
set i >> 0
rep True True 10 => { set i >> %i% + 1; if %i% :=: 5 True then => { cont() }; sys.out "i = %i%" }
```
输出：
```
i = 1
i = 2
i = 3
i = 4
i = 6
i = 7
i = 8
i = 9
i = 10
```

**示例8：在循环中使用and条件**
```
link sys
set i >> 0
rep %i% < 10 and %i% >= 0 True 10 => { set i >> %i% + 1; sys.out "i = %i%" }
```

**示例9：在循环中使用or条件**
```
link sys
set flag >> True
set count >> 0
rep %flag% True or %count% < 5 True 10 => { set count >> %count% + 1; sys.out "count = %count%" }
```

#### 注意事项
- 无限循环需要谨慎使用，确保有退出机制
- wait命令的时间参数支持浮点数
- 循环次数必须为正整数
- 支持在循环中使用其他命令，包括if和嵌套的rep
- 在脚本和交互模式中都可以使用

## 变量和常量

### 定义常量
常量一旦定义，不能重新定义
```
>>> set pi :: 3.14159
>>> constant pi defined as 3.14159
```

### 定义变量
变量可以重新定义
```
>>> set x >> 10
>>> variable x defined as 10
```

### 使用变量
在表达式中使用变量，支持两种格式：
- `%name%`
- `%{name}%`

```
>>> set a :: 5
>>> calc %a% + 3
>>> calc %{a}% * 2
```

## 运算符

### 算术运算符
| 运算符 | 说明 | 示例 |
|--------|------|------|
| + | 加法 | 1 + 2 |
| - | 减法 | 5 - 3 |
| * | 乘法 | 2 * 3 |
| / | 除法 | 6 / 2 |
| % | 取余 | 5 % 2 |
| ^ | 幂运算 | 2 ^ 3 |

### 一元运算符
| 运算符 | 说明 | 示例 |
|--------|------|------|
| + | 正号 | +5 |
| - | 负号 | -5 |

### 运算符优先级
1. 一元运算符（+, -）：最高优先级
2. 幂运算（^）
3. 乘、除、取余（*, /, %）
4. 加、减（+, -）：最低优先级

### 括号
使用括号改变运算优先级
```
>>> calc (1 + 2) * 3
>>> calc 1 + (2 * 3)
```

### 逻辑运算符
| 运算符 | 说明 | 示例 |
|--------|------|------|
| and | 逻辑与（短路求值） | %a% > 5 and %b% < 10 |
| or | 逻辑或（短路求值） | %x% :=: 1 or %x% :=: 2 |

#### 逻辑运算符特性
- `and`：如果左边的条件为真，才检查右边的条件；否则直接返回False
- `or`：如果左边的条件为真，直接返回True；否则检查右边的条件
- 支持短路求值，提高性能

#### 使用示例
```
link sys
set a >> 10
set b >> 5
if %a% > 5 and %b% < 10 True then => { sys.out "条件满足" }
if %a% :=: 1 or %a% :=: 10 True then => { sys.out "a是1或10" }
```

## 循环控制

### brk()
中断循环，退出当前循环体
- 在if、elif、else、rep语句中可用
- 立即退出最内层的循环

### cont()
跳过本次循环，继续下一次循环
- 在if、elif、else、rep语句中可用
- 跳过当前迭代，直接进入下一次迭代

#### 使用示例

**示例1：使用brk()中断循环**
```
link sys
set i >> 0
rep True True 10 => { set i >> %i% + 1; if %i% :=: 5 True then => { brk() }; sys.out "i = %i%" }
```
输出：
```
i = 1
i = 2
i = 3
i = 4
```

**示例2：使用cont()跳过循环**
```
link sys
set i >> 0
rep True True 10 => { set i >> %i% + 1; if %i% :=: 5 True then => { cont() }; sys.out "i = %i%" }
```
输出：
```
i = 1
i = 2
i = 3
i = 4
i = 6
i = 7
i = 8
i = 9
i = 10
```

**示例3：在脚本中使用brk()和cont()**
```
link sys
set i >> 0
rep True True infinite => { set i >> %i% + 1; if %i% > 10 True then => { brk() }; if %i% :=: 5 True then => { cont() }; sys.out "Processing: %i%" }
_yuE_
```

#### 注意事项
- brk()和cont()只能在循环体（if/elif/else/rep语句）中使用
- brk()会立即退出整个循环
- cont()只会跳过当前迭代，不会退出循环
- 支持嵌套循环中的使用

## 示例

### 基本计算
```
>>> calc 1 + 2
3
>>> calc 3 * 4
12
>>> calc 10 / 2
5.0
>>> calc 2 ^ 3
8
```

### 一元运算符
```
>>> calc -5
-5
>>> calc +5
5
>>> calc 3 + -2
1
>>> calc 3 * -2
-6
>>> calc -3 ^ 2
9
>>> calc (-3) ^ 2
9
```

### 变量使用
```
>>> set a :: 10
>>> constant a defined as 10
>>> set b >> 5
>>> variable b defined as 5
>>> calc %a% + %b%
15
>>> calc %a% * %{b}%
50
>>> calc -%a%
-10
```

### 复杂表达式
```
>>> calc 3 + 4 * 2 / (1 - 5)^2
3.5
>>> calc -(3 + 2)
-5
>>> calc --5
5
```