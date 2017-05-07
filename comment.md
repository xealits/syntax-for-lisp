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




Pipelines of function calls?
----------------------------

A-la shell `ls -la | grep foo`.
It is a stream of bytes, from `stdout` to `stdin`.
(Special constructions and conventions of Unix, among other particulars.)
It's not the only semantics, there are other needs:

    find .. | xargs ls
    ls -tal `find all logs` # prints the last touched logs

But it is handy, it is cooperation of processes,
it is construction of a larger program from particular pieces.
(Each program is like a function of a library.)
It's an interesting example to consider.
So how to do it?

First aid is to use composition of two functions.
The piping basically is composition.
Add convenient syntax and it will substitute the pipe.

Assume some programming objects (`stdin/out`)?
Don't assume. Everything should be visible.
But if visible -- more key strokes?
Not necessary -- the pipe symbol is still there in the shell-s.

The problem is the "reverse" order of function calls:

    final_call A (second_call B (initial_call C))

-- sometimes it looks awkward.

Inverse Polish notation and stuff..

**On practice, one wants to test the calls in order, adding steps one by one.**
And the function calls break this.

From design/utility point of view,
the call-tree (s-expression of lisp) describes the call completely,
from leaves (the first calls) to the root (final call),
when the pipelines are more "automaton-like" description of current processing,
whithout regarding the previous or following stuff.
Also the pipeline is concurrent cooperation of several processes with some protocol:
whenever each process gets something in stdin it works on it and outputs to stdout.
{The processes-stuff maybe fits into functions with lazy evaluation.}
**But really this doesn't matter**,
the only important point is where each process gets its' inputs from,
how it processes it, whether it waits for the end of input or not, is buisness of the process,
and the only problem on practice we have is exactly the necessity
to easily run parts of the pipeline in order.
The hierarchy look of the tree of calls is also not that important:
it can be "flattened" along one line of branches etc.

Самый простой способ это вставить какой-то символ для "последнего вывода",
как `_` в Python:

    initial_call C
    second_call B _
    final_call A _
    # или
    initial_call C ; second_call B _ ; final_call A _
    # можно и быстро tee устроить, т.е. разветвлять один вывод в несколько процессов:
    initial_call C ; \(second_call B _ ; final_call A _)
    (initial_call C) \((second_call B _) (final_call A _))
    # \((foo) (bar)) обозначает не полную цитату, фуу/бар испольняются и помещяются в список
    # как (list (foo) (bar))

-- это можно и в функциональном смысле читать,
точно как сочетание вложенных вызовов, подстановка ссылок на выводы одних процессов на вводы другим.

В итоге это таки подразумеваемая переменная.
Но вывод функций никак не выделялся/не формулировался до этого -- тут он учтён.

Вообще, тут есть что-то от кэрринга -- какое-то правило создания "неполных функций" и их применения:

    define (a a1 a2) : ...
    a X   = (a X) = lambda (a2) ...

Тогда "перевёрнутый" порядок вызова с композицией функций выглядит:

    cat f * a -l
    cat f | a -l  # типа | это оператор "или" из С

Тут | работает как нестандартный вызов:

    # не просто
    ((cat f) (a -l))
    # а
    (compose (cat f) (a -l))
    # или проще
    ((a -l) (cat f))
    #
    (call-on (cat f) (a -l))

(При этом, кстати, `(cat f)` это функция с 0 аргументов.)


