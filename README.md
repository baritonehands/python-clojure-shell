Python Clojure Shell
======================

A python module to dynamically convert python to Clojure, to evaluate within a Clojure nREPL.

## Overview

The general idea here is to allow connecting to a Clojure nREPL session in a python shell. All the python
code will be converted to Clojure and evaluated inside the remote REPL session. Python data will be converted
to EDN before passing to the REPL. This allows you to mix together remote Clojure data and local python data.
Also, code is automatically converted from snake_case in python to camelCase in Clojure, since those are the
preferred conventions. 

**Note**: This is alpha software and any interfaces are subject to change.

## Installation

To install you don't need to clone this repo. You can just copy the clone link, and use pip:

```pip install git+<paste clone link>```

## Starting the nREPL

You can start the nREPL as you choose, but simplest way is with [Leiningen](https://leiningen.org)

    lein repl :headless :port 7002

If you start from within a Leiningen project, all the code should be accessible in the shell.

## Shell Usage

To use the pyclj-shell, there are some built in functions for easy REPL use:

### Auto imports

All of the vars from the clojure.core and clojure.repl namespaces have been auto-imported into the shell session. You
can refer to them directly by their name. The unsupported characters such as !, ?, etc. have been mangled.

For those names that conflicted with python's built-in module, you'll have to refer to them via the clj or repl namespace
aliases.

```python
>>> mapcat # This function has no python equivalent, so it's auto imported
#object[clojure.core$mapcat 0x221dbc0a "clojure.core$mapcat@221dbc0a"]

>>> map
<built-in function map>

>>> clj.map
#object[clojure.core$map 0x52b28bf6 "clojure.core$map@52b28bf6"]
```  

### require

Require a clojure namespace and assign to a python variable:

```python
>>> s = require('clojure.string')
>>> s.upper_case('foo')
FOO
```

### var

Define a clojure var, or get a reference to existing var:

```python
>>> my_range = var('my_range', range(100))
#'user/my_range
>>> plus = var('+')
>>> clj.reduce(plus, my_range) # Must explicitly mention Clojure's reduce
4950
```

### new

Instantiate a java class:

```python
>>> my_map = new('java.util.HashMap')
#'user/G__765
>>> my_map.put('foo', 'bar')
None
>>> my_map
{u'foo': u'bar'}
```

### import_class

Import a java class so it can be referenced by short name:

```python
>>> import_class('java.util.HashMap')
u'java.util.HashMap'
>>> my_map = new('HashMap')
>>> my_map.put('foo', 'bar')
>>> my_map
{u'foo': u'bar'}
```

### doc

Look up the docstring for a clojure var:

```python
>>> doc(frequencies)

clojure.core/frequencies

([coll])

  Returns a map from distinct items in coll to the number of times
  they appear.

None
```

### Using repl results locally

When using any of the above functions, the shell automatically evaluates the result when the shell calls repr(). If
you want to use a remote result in a local python computation, you need to explicitly call eval():

```python
>>> clj.mapv(inc, range(5, 10)) + [1, 2, 3]
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: unsupported operand type(s) for +: 'FunctionCall' and 'list'

>>> clj.mapv(inc, range(5, 10)).eval() + [1, 2, 3]
[6, 7, 8, 9, 10, 1, 2, 3]
``` 

## Cli Options

```
usage: pyclj-shell [-h] [--host [host]] [-p [port]]

Run a python shell connecting to a Clojure nREPL

optional arguments:
  -h, --help            show this help message and exit
  --host [host]         Host of running clojure nREPL (default localhost)
  -p [port], --port [port]
                        Port of running clojure nREPL (default 7002)
```

## License

Copyright ©2018 Brian Gregg

Distributed under the MIT License. Please see the LICENSE.txt file at the top level of this repo.
