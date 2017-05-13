"""
Running this:

    rlwrap -p'0;31' python3 comm.py -i racket

need to:
 * spawn a separate process for racket, connecting it's stdout to current stdout, but controling the stdin for syntax parsing
   or just organize stdin/stdout with linux stuff somehow

   term { stdin  <--- keyboard
              \----------> rlwrap (split!)------> comm.py -------> scheme.interpreter |
          stdout <- (hist/col)/       <-(only debug)/                      <---------

   --- this simple splitting is kind of easy to do with /proc/PID/fd/
       but not with commandline utilities (the unix tradition..)

       I need to split the output of comm.py:
           the scheme interpreter gets only parsed syntax,
           thus comm.py send only parsed result on stdout,
           debug and prompt go to stderr

       1) It seems logging sends stuff to stderr by default.
       2) Racket, guile and mit-scheme work well with pipe. (Guile unnecessary clears the prompt..)
       All ok!
"""

from parsing_scripts import parse_syntax, nod_tree_to_list, nod_tree_to_string
import logging, argparse
import subprocess
import pexpect
import builtins, sys


def input(prompt=None):
    """input(prompt=None)

    redefining the builtin 'input' to write the prompt to stderr
    since stdout is used for parsed syntax only
    """
    if prompt:
        sys.stderr.write(str(prompt))
    return builtins.input()

def input_multi(prompt="> "):
    '''input_ext(prompt="> ")

    should work as multiline input
    exits on empty line (two newlines '\n\n')
    '''

    line = input(prompt)
    lines = [line]
    while line:
        line = input()
        lines.append(line)
    return '\n'.join(lines)

def is_CAPSLOCK():
    return subprocess.getoutput('xset q | grep LED')[-1] == '1'

interpreter_commlines = {
        'echo': "echo '%s'",
        'guile': "guile -c '%s'",
        'racket': "racket -e '%s'"}
#out = subprocess.getoutput("%s -c '%s'" % (intr, parsed_prog_string))

if __name__ == '__main__':
    lisp_prompt = '> '

    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "a sketch of a shell for synax-lisp",
        epilog = "Example:\n$ python3 comm.py | racket"
        )

    parser.add_argument('-d', '--debug', help="level of loggin = DEBUG", action="store_true")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)

    # multicommands should be done with rlwrap
    # but it eats tabs...
    while True:
        inp = input_multi('')
        # if CAPSLOCK is on the command goes to the shell itself
        inp = inp.strip()
        if inp == 'EXIT':
            break
        elif 'FILE' in inp: # source input from the file
            _, filename = inp.split()
            with open(filename) as f:
                inp = f.read()
            # TODO: handle NoFile exception

        logging.debug('inp:%s' % inp)
        if inp.strip():
            nod_tree = parse_syntax(inp)
            logging.debug('nods:%s' % nod_tree)
            # only echo behavior is supported -- pipe the output to interpreters for interactive use
            parsed_str = nod_tree_to_string(nod_tree)
            print(parsed_str)
            logging.debug("echo parsed_str:%s" % parsed_str)

