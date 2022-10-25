# First challenge is figuring out when a block of code begins and ends.
# Or does that even matter?

# How about we just focus on this:
# replace function names with nonsense
# replace variable names with nonsense
# remove ANY comments
# remove any whitespace between code

# More advanced things after the simple stuff:
# Handling things inside parenthesis.
# Handling imported stuff
# Get rid of typing
# Dont mess with built-in functions

import random
import re
from config import NONSENSE


comment_re = re.compile(r"#.*\n")
function_re = re.compile(r"\s*def *(?P<name>\w*)\((?P<args>[\w, ]*)\):")
declaration_re = re.compile(r"(?P<decl>[\w]*) * = *(?!=)")

name_map = {}

def get_replacement(name: str):
    if not len(NONSENSE):
        raise Exception("No more replacements left.")
    replacement = NONSENSE.pop( random.randint(0, len(NONSENSE) - 1) )
    name_map[name] = replacement
    return replacement


def main():
    file_name = input("What file would you like to obfuscate? (./inputs/{filename}) ")

    with (open(f"./inputs/{file_name}", 'r') as input_file, 
            open(f"./output/{file_name}", 'w') as output_file):
        text = input_file.read()

        # for line in lines:
        # print(f"Before: {line}")
        # Strip any comments that are on this line.
        # We need to make sure not to strip anything within ().
        text = comment_re.sub("\n", text)
        # Check if its an empty line now. If it is, continue to next line.
        # whitespace_check = line.strip()
        # if len(whitespace_check) == 0:
        #     continue
        # If there are any things, left. Check if we can replace names
        # and then write the line.

        # Check for functions.
        if (headers := function_re.findall(text)) is not None:
            print(headers)
            for header in headers:
                name, args = header
                print(f"{name=}, {args=}")
                name_repl = get_replacement(name)
                arg_repl = [get_replacement(arg.strip()) for arg in args.split(',')]
                # text = f"def {name_repl}({','.join(arg_repl) if len(arg_repl) > 1 else arg_repl[0]}):\n"
                
                text = re.sub(name, name_repl, text)
            
        # Check for variable declarations
        if (declarations := declaration_re.findall(text)) is not None:
            for declaration in declarations:
                print(f"{declaration=}")
                var_repl = get_replacement(declaration.strip().strip('='))
                text = declaration_re.sub(f"{var_repl}=", text)
            # line = declaration_re.sub()

        # Check for function calls

        # Check for variable use

        # print(f"After: {line}")
        output_file.write(text)

main()