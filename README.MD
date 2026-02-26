#Basic Information:
Project name:YU Language(YUlang)
Author:[YuZhuohao]
License:[Undetermined]
Project start time: 2026.02.25
Project version: 26.08.01  (As of 2026.02.25)

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