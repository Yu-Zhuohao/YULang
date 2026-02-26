import sys
import yu.global_definition as gd
import yu.command as cmd
from yu.keywords.if_cmd import execute_if
from yu.keywords.rep_cmd import execute_rep

def aboutM():
    print(gd.aboutM)

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
        if usr_input_strip == "quit()" or usr_input_strip == "exit()":
            print(gd.quitM)
            sys.exit(0)
        elif usr_input_strip.startswith("yu --version"):
            print(gd.versionM)
        elif usr_input_strip == "help":
            print(gd.helpM)
        elif usr_input_strip.startswith("link"):
            cmd.handle_link(usr_input_strip)
        elif usr_input_strip.startswith("yu ") and len(usr_input_strip) > 3:
            filename = usr_input_strip[3:].strip()
            cmd.handle_script(filename)
        elif '.' in first_part:
            cmd.handle_module_call(usr_input_strip)
        elif first_part not in gd.keywords:
            print(gd.unk_cmdM)
        elif usr_input_strip.startswith("set"):
            cmd.handle_set(usr_input_strip)
        elif usr_input_strip.startswith("calc"):
            cmd.handle_calc(usr_input_strip)
        elif usr_input_strip.startswith("if"):
            execute_if(usr_input_strip)
        elif usr_input_strip.startswith("rep"):
            execute_rep(usr_input_strip)

if __name__ == "__main__":
    main()