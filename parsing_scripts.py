special_tokens = [',', ';']
indentation = '\t'

# I cannot just tokenize
# I need to parse indentations
'''
def tokenize(chars):
    "Convert a string of characters into a list of tokens."
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()
'''

# ok, first version without any indentations
# just coma and semi-colon
def parse_line(line: str) -> str:
    '''parse_line(line)

    returns a string with a propper lisp-node,
    where the lispy-syntax of line is substituted by parentheses where needed

    'X ; Y'   -> '(X) (Y)' --- splits the line into several nodes
    '(X ; Y)' -> '(X) (Y)'
    ' , XtillEnd' -> ' ( XtillEnd )' --- makes a node of the rest of the line, until the end or semicolon
    '''

    tokens = line.replace('(', ' ( ').replace(')', ' ) ').split()
    # splits on ' , ' and ' ; ' as well
    # ,,, and ;;; are not considered tokens

    removed_tracing_semicolons = []
    prev_token = None
    for t in tokens:
        if t == ';' == prev_token:
            continue
        removed_tracing_semicolons.append(t)

    tokens = removed_tracing_semicolons

    #print(tokens)

    res = "" # TODO: if input doesn't start with parent -- add it right now?
    coma_nests = [0]
    for t in tokens:
        if t == ',':
            # add a coma-nest, thus the parent
            res += '('
            coma_nests[-1] += 1
        elif t in ';)':
            # finish possible coma nests
            if len(coma_nests):
                res += '%s' % (coma_nests[-1]*')')
                coma_nests.pop()
            if t == ';': # close the current node and open new one
                res += ')('
            else:        # just close the current node
                res += ')' # could just add this token, as in regular case
        elif t == '(':
                # new node for ; and ,
                # thus the new record for coma nests
                coma_nests.append(0)
                res += '('
        else:
            res += ' %s ' % t

    # and if the first token wasn't (
    # the top-level node has to be added
    if tokens[0] != '(':
        res = '(%s)' % res

    return res

examples = [ '  (a b)',
        'a b c , d e f',
        'a b c ; d e',
        '(a b c ; d e)',
        'a bc ;;; d ; (56 jj)',
        '(a (b c ; d) e)',
        '(a b c (d e (f (g))))',
        'a b c , d e , f , g',
        '(system* "ls ..")',     # Guile and shell stuff
        '(system* "ls" "..")',
        '(system* "ls ..")',
        '''(for-each                                                                                                                            
            (lambda (x) (begin (display x) (newline)))
            (string-split (getenv "PATH") #\:))''',
        '''for-each                                                                                                                            
            (lambda (x) , begin (display x ; newline))
            (string-split (getenv "PATH") #\:)''',
        '''for-each                                                                                                                            
            (lambda (x) , begin (display x ; newline) ;
            string-split (getenv "PATH") #\:)'''
        ]



