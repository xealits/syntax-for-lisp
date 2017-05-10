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
 * spawning a process you need to kill it afterwards etc..
   thus I'll connect to a given PID (if the interpreter option isnumeric())
   and use its' /proc/PID/fd for input/output
   ...
   but starting a process on shell means binding stdin/stdout of the shell to it
   also reading stdout blocks...
   ..asynchronous unix...
   ...very logical, rational unix tradition...very usable in development of very diverse stuff..

   actually:

       $ ls /proc/17279/fd -l
       total 0
       lrwx------ 1 alex alex 64 May 10 20:07 0 -> /dev/pts/4
       lrwx------ 1 alex alex 64 May 10 20:07 1 -> /dev/pts/4
       lrwx------ 1 alex alex 64 May 10 20:07 2 -> /dev/pts/4
       lr-x------ 1 alex alex 64 May 10 20:09 3 -> /proc/17279/maps
       lr-x------ 1 alex alex 64 May 10 20:09 4 -> pipe:[425871]
       l-wx------ 1 alex alex 64 May 10 20:09 5 -> pipe:[425871]
       lrwx------ 1 alex alex 64 May 10 20:09 6 -> anon_inode:[eventpoll]
       lr-x------ 1 alex alex 64 May 10 20:09 7 -> /dev/null

   the terminal stuff kicks in...

   so, fork it is..

       from subprocess import Popen, PIPE, STDOUT
       p = Popen(['racket'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
       stdout_data = p.communicate(input='(+ 1 2)')[0]

   -- no, .communicate is for 1-time message in, message out

   p.stdin and p.stdout can be made NONBLOCK
   but now I send stuff to stdin and get nothing from stdout...
   but it doesn't block indeed

       >>> p = Popen(['racket'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
       >>> fd = p.stdout.fileno()
       >>> fl = fcntl.fcntl(fd, fcntl.F_GETFL)
       >>> fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
       0
       >>> p.stdin.write(b'(+ 1 2)\n')
       8
       >>> p.stdout.read()
       b'Welcome to Racket v5.3.6.\n> '
       >>> p.stdout.read()
       >>> 
       >>> p.stdout.read()
       >>> p.stdout.read()
       >>> p.stdin.write(b'(+ 1 2)\n')
       8
       >>> p.stdout.read()

   unix -- everything is hardcoded, not hardwired

   the last hope is module pexpect
   example:

       import pexpect
       
       analyzer = pexpect.spawnu('hfst-lookup analyser-gt-desc.hfstol')
       analyzer.expect('> ')
       
       for newWord in ['слово','сработай'] :
           print('Trying', newWord, '...')
           analyzer.sendline( newWord )
           analyzer.expect('> ')
           print(analyzer.before)

   it does work kind of -- sometimes input and "expect" desynchronize
"""

from parsing_scripts import parse_syntax, nod_tree_to_list
import logging, argparse
import subprocess
import pexpect


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
        epilog = "Example:\n$ python comm.py --interpreter racket"
        )

    parser.add_argument('-i', '--interpreter', help="the name of the lisp interpreter executable\nor 'echo' for test of syntax parsing", default="racket")
    parser.add_argument('-d', '--debug', help="level of loggin = DEBUG", action="store_true")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)
    logging.debug(args.interpreter)
    intr = args.interpreter
    #comm_line = interpreter_commlines.get(intr) # None for connected run

    # no, this doesn't work
    #if intr == "external": # fork a process and write/read its' stdin/stdout
        #flags = os.O_RDONLY | os.O_NONBLOCK
        #stdin = open('/proc/'+intr+'/fd/0', 'w')
        #stdout, stderr = (os.open('/proc/'+intr+'/fd/%s' % i, flags) for i in (1, 2))
    # spawning an interpreter with pexpect
    if not intr == "echo":
        # then spawn
        lisp_interpreter = pexpect.spawnu(intr)
        lisp_interpreter.expect(lisp_prompt) # here I need the prompt of the interpreter, racket uses '> ', guile 'scheme@(guile-user)> '
    else:
        lisp_interpreter = None

    # multicommands should be done with rlwrap
    # but it eats tabs...
    while True:
        inp = input_multi('com> ')
        # if CAPSLOCK is on the command goes to the shell itself
        if is_CAPSLOCK():
            logging.debug('CAPS inp:%s' % inp)
            if inp.strip() == 'EXIT':
                break
            elif inp.strip() == 'F' and lisp_interpreter:
                lisp_interpreter.expect(lisp_prompt)
                print(lisp_interpreter.before)
                continue

        logging.debug('inp:%s' % inp)
        if inp.strip():
            nod_tree = parse_syntax(inp)
            logging.debug('nods:%s' % nod_tree)
            parsed_prog = nod_tree_to_list(nod_tree)
            logging.debug('pros_str:%s' % parsed_prog)

            if lisp_interpreter:
                for command in parsed_prog:
                    lisp_interpreter.sendline(command) # if I pass several commands I need to expect several outputs
                    lisp_interpreter.expect(lisp_prompt)
                    print(lisp_interpreter.before)
            else:
                # echo behavior
                print(parsed_prog)
                logging.debug("echo")

