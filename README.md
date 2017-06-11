Intro
=====

A bit of syntax for Lisp

The main idea is from:
https://pschombe.wordpress.com/2006/04/16/lisp-without-parentheses/

plus the colon and the semicolon.

Check it out with `Fish` shell, `guile` Lisp interpreter and `Python3`:

	guile -c (python3 parsing_scripts.py example1)

or:

	rlwrap python3 comm.py -i echo | racket
	rlwrap python3 comm.py -i echo | tee /dev/fd/2 | racket
	# inside the "shell" input is multiline, ends with empty input line (hit ENTER twice)
	FILE ls.syntax

	ls /home ..

	EXIT


-- second option shows what is actually passed to `racket`.
It uses Linux's (and Mac OSX' and FreeBSD's etc) `/dev/fd/2` symlink to current `stderr` (also `/dev/stderr`).





Syntax
======

It's all work in progress.
But overall the syntaxis consists of:

* the parentheses,
* meaningful indentation (a-la Python),
* the colon works like & in Haskel -- it nests a node in the current one,
* the semicolon means the end of "current node",
* (TODO) and the backslash \ should cancel the nesting of an indented line.
* for now comment is from `%` till end of line
* (TODO) and coma is like backwards colon/haskel-& -- nests the previous symbols in a node

The punctuation should work mostly in-line,
indentation nests nodes accordingly.

Examples:

	a : b c            = (a (b c))
	a : b : c ; d : r  = (a (b (c))) (d (r))
	a                  = (a (b c))
		b c
	a , b c            = ((a) b c)

From the article

Condition:

	(cond
		((< x -1) (* x x))
		((> x 1) (* x x))
		((< x 0) (sqrt (abs x)))
		(else (sqrt x)))

becomes

	cond
		(< x -1) (* x x)
		(> x 1) (* x x)
		(< x 0) (sqrt (abs x))
		else (sqrt x)

or even

	cond
		(< x -1)
			* x x
		(> x 1)
			* x x
		(< x 0)
			sqrt (abs x)
		else
			sqrt x

The let:

	(let
		((a (+ 1 v)) (b (car z)) (c (avg 8 3 w)) (d w))
		(body-goes-here))

becomes

	let
		(a (+ 1 v)) (b (car z)) (c (avg 8 3 w)) (d w)
		body-goes-here

or

	let
			a (+ 1 v) 
			b (car z)
			c (avg 8 3 w)
			d w
		body-goes-here


Similar projects
================

[ClojureScript Parinfer](https://shaunlebron.github.io/parinfer/).

