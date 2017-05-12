import logging
import re
import argparse


examples = [ '  (a b)',
        'a b c : d e f',
        'a b c ; d e',
        '(a b c ; d e)',
        'a bc ;;; d ; (56 jj)',
        '(a (b c ; d) e)',
        '(a b c (d e (f (g))))',
        'a b c : d e : f : g',
        '(system* "ls ..")',     # Guile and shell stuff
        '(system* "ls" "..")',
        '(system* "ls ..")',
        '''(for-each                                                                                                                            
            (lambda (x) (begin (display x) (newline)))
            (string-split (getenv "PATH") #\:))''',
        '''for-each                                                                                                                            
            (lambda (x) : begin (display x ; newline))
            (string-split (getenv "PATH") #\:)''',
        '''for-each                                                                                                                            
            (lambda (x) : begin (display x ; newline) ;
            string-split (getenv "PATH") #\:)'''
        ]

examples_with_indentation = [ 'a b\n\tc e\n\td',
        '(a\nb\nc)',
        'a b: c ; ( d\n\n\te )',
        'a b: c ; ( d\nfoo\n\te )']

class Tabs:
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return '\t' * self.n
    def __repr__(self):
        return "Tabs(%d)" % self.n

syntax_tokens = ['(', ')', '\n', '\t', ';', ',', ':', '%']
syntax_tokens_to_pad = ['(', ')', '\n', '\t', ';', ',', '%']
# , works as & in Haskell but doesn't span to new tab-lines
# : works the same but does wrap the following tab-lines
# quote :
#       a b c
#       + 1 2
# = (quote ((a b c) (+ 1 2)))

def parse_tokens(chars: str) -> 'list(str)':
    '''parse_tokens(line: str) -> 'list(str)'

    returns a list of syntax tokens

    'X ; Y'   -> ['X', ';', 'Y']
    '(X ; Y)' -> ['(', 'X', ';', 'Y', ')']
    'a b\nc'  -> ['a', 'b', '\n', 'c']
    '''

    # now there is a problem with tabs:
    # rlwrap eats them (a commandline-builder utility)
    # ... so
    # I'll accept spaces as input,
    # but they are splited on later
    # thus I'll parse them first and turn into tabs
    pattern = re.compile('\n[ ]+')
    for i in pattern.finditer(chars):
        a, b = i.span()
        n_spaces = b - a - 1
        # the worst part:
        chars = chars[:a+1] + '\t'*n_spaces + chars[b:]

    for t in syntax_tokens_to_pad:
        chars = chars.replace(t, ' %s ' % t)

    res = []
    newline = False
    tabline = 0
    comment = False
    for t in chars.split(' '):
        if t == '':
            continue
        elif comment and not t == '\n':
            continue
        elif t == '%':
            comment = True
            continue
        elif t == '\n':
            if comment: comment = False
            if newline: res += '\n'
            newline = True
            #res.append(t)
        elif t == '\t': # to have all tabs caught
            if newline:
                tabline += 1
            else: pass
            # else skip the tab
        else:
            if tabline:
                res += [Tabs(tabline), t]
                newline, tabline = False, 0
            elif newline:
                res += ['\n', t]
                newline = False
            else:
                res.append(t)

    return res




def parse_syntax(chars: str) -> str:
    '''
    '''
    tokens = parse_tokens(chars)
    logging.debug('syntax tokens:%s' % tokens)

    nod_tree  = []
    semicolon_nod_stack = [nod_tree] # hook for (coma)colon-semicolon cooperation
    nod_stack = [nod_tree] # current branch of the tree
    open_nods, open_parenthesis = [nod_tree], 0 # track open parentheses
    prev_tabs = 0
    # indent_parent is the last node in nod_tree == the nod_stack[1] node

    for i, t in enumerate(tokens):
        #print(t)
        #print(len(nod_stack))
        # cases for special tokens (ifs for now)
        if t == '(':
            # nest new node in the current one
            new_nod = list()
            nod_stack[-1].append(new_nod)
            nod_stack.append(new_nod) # don't forget to grow the stack
            open_nods.append(new_nod)
            semicolon_nod_stack.append(new_nod)
            open_parenthesis += 1
            # parentheses should somehow work above other syntaxis, but how?
            #indent_parent, indent_prev, prev_tabs = nod_tree, nod_tree, 0

        elif type(t) is Tabs:
            # nest a node in the stack at depth of t.n
            # so, I need the largest level below t.n in the stack, call it N
            # and nest there with t.n - N depth
            #print(nod_stack)
            if t.n == prev_tabs:
                # the previous tab-node ended and it's a new one
                # just nest into the parent of previous node
                # plus close all current open colons
                # thus it should be the same as getting to semicolon_nod?
                while (nod_stack[-1] is not semicolon_nod_stack[-1]):
                    nod_stack.pop()
                # and move to parent
                nod_stack.pop()

            elif t.n < prev_tabs: # TODO: chack if it works
                #print("case A")
                # nest the parent nod of indentation
                # it is the first after the root node nod_tree
                # or the open_nod if it is higher in the stack..
                # TODO: check "no-nest" option of tabs
                #print('open nods:\n%s' % open_nods)
                #print('stack len: %d' % len(nod_stack))

                while (nod_stack[-1] is not open_nods[-1] and len(nod_stack) > 2):
                    nod_stack.pop()
                # now nod_stack[-1] == nod_stack[1] == nod_tree[-1]
                # or nod_stack[-1] == open_node
                #print('stack len: %d' % len(nod_stack))
                #print(nod_stack)
                #print(nod_tree)
                if len(nod_stack) > 1:
                    assert nod_stack[1] == nod_tree[-1] # just to be sure, it sould be true always

            else:
                #print("case B")
                # nest the previous node in the stack
                # and move the semicolon node
                while (nod_stack[-1] is not semicolon_nod_stack[-1]):
                    nod_stack.pop()
                #print(nod_stack)
                pass

            new_nod = list()
            nod_stack[-1].append(new_nod)
            nod_stack.append(new_nod)
            semicolon_nod_stack[-1] = new_nod # so the tab-node is semicolon node
            prev_tabs = t.n

        elif t == '\n':
            if open_parenthesis:
                # probably I need to finish open tabs
                # but remain in the opened node
                # pop the stack untill the open_nod
                while (nod_stack[-1] is not open_nods[-1]):
                    nod_stack.pop()
                semicolon_nod_stack[-1] = nod_stack[-1]
            # otherwise the current node parsing has ended
            # block of tabs ended
            # reset stuff
            else:
                semicolon_nod_stack[-1], nod_stack = nod_tree, [nod_tree]

            # in any case the tabs have ended
            prev_tabs = 0


        elif t == ',':
            # coma nests in current node, but doesn't move the semicolon hook
            new_nod = list()
            nod_stack[-1].append(new_nod)
            nod_stack.append(new_nod) # don't forget to grow the stack
        elif t == ':':
            # (coma^W) colon nests in current node and moves the semicolon hook
            new_nod = list()
            nod_stack[-1].append(new_nod)
            nod_stack.append(new_nod) # don't forget to grow the stack
            semicolon_nod_stack.append(new_nod)

        elif t == ';':
            # semicolon finishes its' node
            # it should move the head of the stack to the semicolon node
            # and it nests new node in the semicolon node
            # (a ; b)? TODO: this will break on different levels of nesting
            #  a ; b?
            while (nod_stack[-1] is not semicolon_nod_stack[-1]):
                nod_stack.pop()
            # and move to parent
            nod_stack.pop()
            # and nest new node:
            new_nod = list()
            nod_stack[-1].append(new_nod)
            nod_stack.append(new_nod)
            # -- thus colon at the end of a node `(a , b ;)` doesn't make sence

            # don't move the stack node:
            #semicolon_nod = nod_stack[-1]

        elif t == ')':
            # the parenthesis should striclty finish the corresp opening parenthesis
            # but with the current semicolons (and indentations) it will not at some cases
            # leaving it as is for now..

            # close the node
            # move the stack up
            open_parenthesis -= 1
            if open_parenthesis < 0:
                raise SyntaxError("closing parenthesis without matchin open one, token %d" % i)
            # otherwise,
            # close all of the stack with the open node
            while (nod_stack[-1] is not open_nods[-1]):
                nod_stack.pop()
            nod_stack.pop() # and close the open node
            open_nods.pop()
            #semicolon_nod = nod_stack[-1]
            semicolon_nod_stack.pop()

        # cases for not special tokens
        elif len(nod_stack) == 1:
            # symbols at root-level open a new node
            #print('nest symbol:\n%s' % t)
            new_nod = [t]
            nod_stack[-1].append(new_nod)
            nod_stack.append(new_nod)
            semicolon_nod_stack.append(new_nod)
        else:
            # just add the symbol to the last nod
            #print(nod_stack)
            #print('adding symbol:\n%s' % t)
            nod_stack[-1].append(t)

    return nod_tree


def nod_tree_to_string(nod_tree: list) -> str:
    '''
    '''
    return ''.join([' %s ' % nod if type(nod) is str else '(%s)' % nod_tree_to_string(nod) for nod in nod_tree])


def nod_tree_to_list(nod_tree: list) -> list:
    '''nod_tree_to_list(nod_tree: list) -> list:

    return list of top nodes, i.e. all consequtive commands in the program
    '''
    return [' %s ' % nod if type(nod) is str else '(%s)' % nod_tree_to_string(nod) for nod in nod_tree]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class = argparse.RawDescriptionHelpFormatter,
        description = "parsing utility for syntaxed lisp",
        epilog = "Example:\n$ python3 parsing_scripts.py example4"
        )

    parser.add_argument('script', help="the filename of the syntaxed-lisp script to execute")
    parser.add_argument('-d', '--debug', help="level of loggin = DEBUG", action="store_true")
    parser.add_argument('-o', '--options', nargs='*', help="options to pass to the script")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug(args)
    logging.debug(args.options)

    with open(args.script) as f:
        inp = f.read()

    # pass options if any
    inp = inp.format(options = ' '.join(args.options) if args.options else "")

    logging.debug('inp:%s' % inp)
    nod_tree = parse_syntax(inp)
    logging.debug('tree:%s' % nod_tree)
    print(nod_tree_to_string(nod_tree))




