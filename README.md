Intro
=====

A bit of syntax for Lisp

The main idea is from:
https://pschombe.wordpress.com/2006/04/16/lisp-without-parentheses/

plus the coma and the semicolon.






Syntax
======

It's all work in progress.
But overall the syntaxis consists of:

* the parentheses,
* meaningful indentation (a-la Python),
* the coma works like & in Haskel -- it nests a node in the current one,
* the semicolon means the end of "current node",
* (TODO) and the backslash \ should cancel the nesting of an indented line.

Examples:

	a , b c            = (a (b c))
	a , b , c ; d , r  = (a (b (c))) (d (r))
	a                  = (a (b c))
		b c

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


