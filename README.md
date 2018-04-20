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

### require

Require a clojure namespace and assign to a python variable:

```
>>> s = require('clojure.string')
>>> s.upper_case('foo')
FOO
```

### var

Define a clojure var, or get a reference to existing var:

```
>>> my_range = var('my_range', range(100))
#'user/my_range
>>> plus_r = var('+')
>>> reduce_r = var('reduce')
>>> reduce_r(plus_r, my_range)
4950
```

### new

Instantiate a java class:

```
>>> my_map = new('java.util.HashMap')
#'user/G__765
>>> my_map.put('foo', 'bar')
None
>>> my_map
{u'foo': u'bar'}
```

### import_class

Import a java class so it can be referenced by short name:

```
>>> import_class('java.util.HashMap')
u'java.util.HashMap'
>>> my_map = new('HashMap')
>>> my_map.put('foo', 'bar')
>>> my_map
{u'foo': u'bar'}
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
