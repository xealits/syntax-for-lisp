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


define (compose f g) : lambda (x)
    f , g x

%; foo returns a list of contents for a target path
%; list of the filename if path to a file is given
%; list of content filenames if directory parh is given
%; empty list if a given path doesnt sxist
define (foo t) %; TODO: pattern matching is neded here
    if (file-exists? t) (list t)
        if (directory-exists? t) (directory-list t) (list) 

%; ls loops through targets and returns a merged list of their contents
define (ls targets)
    foldl append (list) , map (compose foo symbol->string) targets
%;    foldl append (list) , map foo targets
%; would be better to do `foldl append` and `map` in 1 go

%; handling commandline inputs
%; sadly you cannot use `,` as a symbol in racket: (quote (. ..))
%; but '(./) works
define options , quote , {options}
define input , if (empty? options) (quote , ./) options

display , ls input


