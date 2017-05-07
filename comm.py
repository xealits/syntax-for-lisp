"""
Running this:

    guile -c (python3 parsing_scripts.py example7)

with user input instead of example7
"""

from parsing_scripts import parse_syntax, nod_tree_to_string
import logging, argparse
import subprocess


def input_multi(prompt="> "):
    '''input_ext(prompt="> ")

    should work as multiline input
    '''

    line = input(prompt)
    lines = [line]
    while line:
        line = input()
        lines.append(line)
    return '\n'.join(lines)

def is_CAPSLOCK():
    return subprocess.getoutput('xset q | grep LED')[-1] == '1'

interpreter_commlines = {'guile': "guile -c '%s'",
        'racket': "racket -e '%s'"}
#out = subprocess.getoutput("%s -c '%s'" % (intr, parsed_prog_string))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "a sketch of a shell for synax-lisp",
        epilog = "Example:\n$ python comm.py --interpreter racket"
        )

    parser.add_argument('-i', '--interpreter', help="the name of the lisp interpreter executable", default="guile")
    parser.add_argument('-d', '--debug', help="level of loggin = DEBUG", action="store_true")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)
    logging.debug(args.interpreter)
    intr = args.interpreter
    comm_line = interpreter_commlines[intr]

    # multicommands should be done with rlwrap
    # but it eats tabs...
    while True:
        inp = input_multi("com> ")
        # if CAPSLOCK is on the command goes to the shell itself
        if is_CAPSLOCK():
            logging.debug('CAPS inp:%s' % inp)
            if inp.strip() == 'EXIT':
                break

        logging.debug('inp:%s' % inp)
        if inp.strip():
            nod_tree = parse_syntax(inp)
            logging.debug('nods:%s' % nod_tree)
            parsed_prog_string = nod_tree_to_string(nod_tree)
            logging.debug('pros_str:%s' % parsed_prog_string)
            out = subprocess.getoutput(comm_line % parsed_prog_string)
            print(out)

