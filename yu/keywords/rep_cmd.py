import time
import yu.global_storage as gs
import yu.global_definition as gd
import yu.calc as calc
from yu.utils import replace_placeholders
from yu.keywords.if_cmd import parse_condition, parse_block, execute_commands
from yu.logic import logical_and, logical_or


def parse_rep_command(cmd_str):
    """
    解析rep命令
    格式: rep <condition> <True|False> <int|infinite> => {}
    """
    cmd_str = cmd_str.strip()
    
    # 检查是否以rep开头
    if not cmd_str.startswith("rep "):
        return None, "Command must start with 'rep'"
    
    # 移除rep
    cmd_str = cmd_str[4:].strip()
    
    # 解析condition部分（直到=>之前）
    arrow_pos = cmd_str.find("=>")
    if arrow_pos == -1:
        return None, "Missing '=>' in rep command. Format: rep <condition> <True|False> <int|infinite> => {}"
    
    condition_part = cmd_str[:arrow_pos].strip()
    block_part = cmd_str[arrow_pos:].strip()
    
    # 解析condition部分
    # 格式: <condition> <True|False> <int|infinite>
    parts = condition_part.split()
    if len(parts) < 3:
        return None, "Invalid format. Expected: rep <condition> <True|False> <int|infinite> => {}"
    
    # 最后一部分是循环次数
    count_str = parts[-1]
    
    # 检查是否是infinite
    if count_str == "infinite":
        is_infinite = True
        loop_count = None
    else:
        is_infinite = False
        # 尝试解析为整数
        try:
            loop_count = int(count_str)
            if loop_count <= 0:
                return None, "Loop count must be a positive integer"
        except ValueError:
            return None, "Loop count must be a positive integer or 'infinite'"
    
    # 倒数第二部分是trigger（True或False）
    trigger = parts[-2]
    if trigger not in ["True", "False"]:
        return None, "Trigger must be 'True' or 'False'"
    
    # 剩余部分是condition
    condition_str = ' '.join(parts[:-2]).strip()
    
    # 解析block
    commands, error = parse_block(block_part)
    if error:
        return None, error
    
    # 解析condition
    condition_result, error = parse_condition(condition_str)
    if error:
        return None, error
    
    # 解析命令中的wait语句
    parsed_commands = []
    for cmd in commands:
        parsed_cmd, error = parse_wait_command(cmd)
        if error:
            return None, f"Error in command '{cmd}': {error}"
        parsed_commands.append(parsed_cmd)
    
    return {
        'condition': condition_result,
        'trigger': trigger == "True",
        'is_infinite': is_infinite,
        'loop_count': loop_count,
        'commands': parsed_commands
    }, None


def parse_wait_command(cmd_str):
    """
    解析命令中的wait语句
    格式: wait <int>s 或 wait <int>ms
    返回: (parsed_cmd_dict, error)
    """
    cmd_str = cmd_str.strip()
    
    # 检查是否是wait命令
    if cmd_str.startswith("wait "):
        wait_parts = cmd_str[5:].strip().split()
        if len(wait_parts) != 1:
            return None, "Invalid wait format. Use: wait <int>s or wait <int>ms"
        
        time_str = wait_parts[0]
        
        # 检查单位（先检查 ms，因为 ms 也以 s 结尾）
        if time_str.endswith('ms'):
            # 毫秒
            try:
                wait_time = float(time_str[:-2])
                if wait_time < 0:
                    return None, "Wait time must be non-negative"
                return {
                    'type': 'wait',
                    'unit': 'milliseconds',
                    'time': wait_time
                }, None
            except ValueError:
                return None, "Invalid wait time. Must be a number"
        elif time_str.endswith('s'):
            # 秒
            try:
                wait_time = float(time_str[:-1])
                if wait_time < 0:
                    return None, "Wait time must be non-negative"
                return {
                    'type': 'wait',
                    'unit': 'seconds',
                    'time': wait_time
                }, None
            except ValueError:
                return None, "Invalid wait time. Must be a number"
        else:
            return None, "Invalid wait unit. Use 's' for seconds or 'ms' for milliseconds"
    else:
        # 不是wait命令，返回普通命令
        return {
            'type': 'normal',
            'command': cmd_str
        }, None


def execute_rep(cmd_str):
    result, error = parse_rep_command(cmd_str)
    if error:
        print(f"Error: {error}")
        return False
    
    condition_is_true = result['condition']
    trigger_when_true = result['trigger']
    
    should_execute = (condition_is_true and trigger_when_true) or \
                     (not condition_is_true and not trigger_when_true)
    
    if not should_execute:
        return True
    
    if result['is_infinite']:
        while True:
            execute_rep_commands(result['commands'])
            if gs.break_flag:
                gs.break_flag = False
                break
            if gs.continue_flag:
                gs.continue_flag = False
                continue
    else:
        for _ in range(result['loop_count']):
            execute_rep_commands(result['commands'])
            if gs.break_flag:
                gs.break_flag = False
                break
            if gs.continue_flag:
                gs.continue_flag = False
                continue
    
    return True


def execute_rep_commands(commands):
    for cmd in commands:
        if gs.break_flag or gs.continue_flag:
            return
        if cmd['type'] == 'wait':
            if cmd['unit'] == 'seconds':
                time.sleep(cmd['time'])
            elif cmd['unit'] == 'milliseconds':
                time.sleep(cmd['time'] / 1000.0)
        elif cmd['type'] == 'normal':
            execute_commands([cmd['command']])
            if gs.break_flag or gs.continue_flag:
                return
            if gs.break_flag or gs.continue_flag:
                return
            if gs.break_flag or gs.continue_flag:
                return