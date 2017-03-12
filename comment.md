Intro
=====

A bit of syntax for Lisp

The main idea is from:
https://pschombe.wordpress.com/2006/04/16/lisp-without-parentheses/

plus a modification and the coma.






Syntax
======

It's all work in progress.
But overall the syntaxis consists of:
* he parentheses,
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







Examples
========


The large function issue:

	(my-large-function
		(car (cdr y))
		(lambda (x) (/ x 2))
		my-list)

(here comes the tweak to the rules of the article)
if `my-list` is 1 symbol, then it is not a call
(a call is several symbols on a line, except the 0-indent level),
and the example becomes what is expected

	my-large-function
		car (cdr y)
		lambda (x) (/ x 2)
		my-list

The lambda example:

	(lambda (x)
		(display x) (newline)
		(* x 42))

has the issue with 2 calls on one line -- `(display x) (newline)`.
With the indent-s it's done as:

	lambda (x)
		display x
		newline
		* x 42

The results of `display x` and `newline` are the initial level.

In the article the backslash is used to suppress the implied call
of the indentation level:

	lambda (x)
		\ (display x) (newline)
		* x 42

-- the slash introduces multiple nodes at the indented line.

It seems the coma with following behavior would also be usefull:

	(foo) (bar)
	# to
	foo , bar

	(lambda (x)
		(display x) (newline)
		(* x 42))
	# maybe to
	lambda (x)
		display x, newline
		* x 42

-- so the coma makes the call and leaves their results on the same level.
It can split a nested function call in:

	((foo) (bar baz) 5 ((x y) z))
	# only the top level (some limit)
	(foo , bar baz , 5 , ( x y , z))
	# so 5 is also called...
	# add quote?
	(foo , bar baz , '5 , ( x y , z))

So it's like Haskell's ampersand, but sets the call not to the end of the current level,
but to the next coma.

Then in indentation it should do the calls and also (like the backslash) suppress the indentation-call?

Then with the coma you can do 1-symbol call (instead of wrapping it in parentheses:

	foo
		bar,   # bar is called and the result is passed to foo, like (bar)
		baz    # baz is passed to foo


The ampersand works as in Haskell.



Thus, the operations, their atomic behaviors in different contexts.

Firstly, let's say that a `node` or level of nesting is `(a b c)`.
I.e. `a` is not the "top" of the node and `b c` are not nested in `a`,
it's one node and one level of call-tree.

Then:

* indentation leaves stuff on the same level,
  but also implies a call on them, if there are many symbols
  (and no call on only 1 symbol)
* the backslash removes the call bit from the indentation
* the coma separates the symbols into two sub-nodes on the same level,
  it might also imply a backslash in case of indentation
* the ampersand separates the rest of the sybmols on the line into a sub-node

-- maybe it is worthwhile separating the call from indentation?
Indentation would just mean the limits of the node
in absence of parentheses to indicate that.

It won't be that bad. The condition is:

	cond
		((< x -1) (* x x))
		((> x 1) (* x x))
		((< x 0) (sqrt (abs x)))
		(else (sqrt x))

The parentheses could be reduced with the coma:

	cond
		, (< x -1) (* x x)
		, (> x 1) (* x x)
		, (< x 0) (sqrt (abs x))
		, else (sqrt x)

(Or at the end of the lines.)

The semi-colon `;` corresponds better to this meaning.
And the coma `,` is better for the ampersand's sematics.

Then, what's the meaning for

	foo bar baz
		ro goo
			boo
		fff

At least the second indentation should imply there is a nested node somewhere.

Then, what's the support for nodes on each line?
(Seems like a popular idiom.)
How does it work on 1 line?

	foo , bar
	# or
	foo ; bar
	# is
	(foo) (bar)
	# like two lines joined

How to do

	(foo (bar) (baz))
	# or
	(foo (bar) 5 (baz))


The problem is:
how to indicate nested call with only 1 symbol insted of parentheses,
with enough flexibility to indicate the end of the nested call, if necessary,
to indicate a sequence of nested calls,
and neatly join it with the indentation.
The meaning of nested node for indentation is very good.
But it mixes with Haskell's ampersand and the thing with coma.
The coma as stop of the current node and start of new one is good on 1 line.

All this stuff should be mixed for maximum practicality and clarity.

What if:

* the indentation by default means new nodes,
  there is no exception for 1-symbol line in the indentation,
  a special sign would change it to no nodes for indented lines, just symbols in the same node
  (the backslash for the whole 1 line of indentation),
  the indentation levels are counted as shown in the article
* the coma works like Haskel's ampersand, i.e. nodes symbols till the end of the current line
* the semi-colon is for original coma -- stops current node and starts new one
* the backslash removes the noding of the indentation
  (if placed for the whole 1 line of indentation -- removes it for the whole indentation)
* if you want to stop noding of the coma (haskel ampersand) you have to use parentheses for the external node of the sequence
  (there is a clear need for marking both ends of the line)

Thus the problematic examples are:

	(my-large-function
		(car (cdr y))
		(lambda (x) (/ x 2))
		my-list)
	# to
	my-large-function
		car (cdr y)
		lambda (x) (/ x 2)
		\ my-list

	(lambda (x)
		(display x) (newline)
		(* x 42))
	# maybe to
	lambda (x)
		display x; newline       # it ended the indented node and started new one, inside the lambda node
		* x 42
	# the semicolon on 1 line is the same as writing on new line
	# either indented or not

	((foo) (bar baz) 5 ((x y) z))
	# only the top level (some limit)
	(foo) ( bar baz ) 5 , (x y)  z
	#            here the (x y) kind of asks for "reverse ampersand"?
	#            but can that be readable?

	foo
		bar    # bar is called
		\ baz  # baz is passed to foo

	foo
		\      # both bar and baz are passed to foo-node as symbols
		bar    #
		baz    #

	# to call something
	foo
		\
		bar
		baz
		(goo)
	# or
	foo
		\
		bar
		baz
		, goo # here the coma doesn't catch the following
		sym   # symbol, since the indentation separates them

What do these mean:

	foo
		bar   ;  # is the foo-node stoped? no, the semicolon stops the indented node, it's useless
		\ baz ;  # now the foo-node is kind of ended?
		sym      # what is this then?
		# the semi-colon in the line of symbols either does nothing
		# or it stops the symbol-line and "works like making a new line" -- starts a node
		# the second option is more logical, yep?

	# and
	foo
		bar
		\ baz sym
			foo2
		# if baz sym are just symbols,
		# what is foo2?
		# it should be an indented node,
		# what does foo2 node with?
		# in principle the backslash just means "no node here"
		# the next indentation nodes with the last symbol on the line
		# the same way it would work without the backslash

And this is the version 1.

There is also the quote sign somewhere.
Maybe just a quote without parentheses quotes from here till the end of the node.






