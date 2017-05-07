%; racket implementation of ls
%; it's just a lisp function
%; given a list of targets
%; and a function
%; run function on the target and append output to 1 common list
%; default function
%; will return filename if the target is file
%; or filenames of contents, if it is directory

%; need variable amount of args* here
%; to convert symbols to strings use: symbol->string

%; would be better to do `foldl append` and `map` in 1 go


%;    foldl append (list) , map (compose foo symbol->string) targets

%; sadly you cannot use `,` as a symbol in racket: (quote (. ..))
%; but '(./) works

define (compose f g) : lambda (x)
    f , g x
define (foo t)
    if (file-exists? t) (list t)
        if (directory-exists? t) (directory-list t) (list) 
define (ls targets) : begin
    display targets
    newline
    foldl append (list) , map foo targets
%; this should work now:
display , ls , quote , "." ".." "/home/"

