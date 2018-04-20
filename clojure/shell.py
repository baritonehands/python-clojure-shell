from .repl import Context, NamespaceAlias, snake_case
import argparse, nrepl, code

class Shell(object):
    def __init__(self, host='localhost', port=7002):
        self.nrepl_client = nrepl.connect("nrepl://%s:%d" % (host, port))

    def start(self):
        local_vars = locals()
        del local_vars['self']

        client = self.nrepl_client
        ctx = Context(self.nrepl_client)

        clj = NamespaceAlias(ctx, 'clojure.core')
        repl = ctx.require('clojure.repl')

        builtin_keys = set(dir(__builtins__))
        def extract_syms(ns):
            ns_alias = NamespaceAlias(ctx, ns)
            for name in clj.map(clj.str, clj.keys(clj.ns_publics(clj.symbol(ns)))).eval():
                if name not in builtin_keys:
                    local_vars[snake_case(name)] = ns_alias[name]

        clj_syms = extract_syms('clojure.core')
        repl_syms = extract_syms('clojure.repl')

        local_vars['var'] = ctx.var
        local_vars['new'] = ctx.new
        local_vars['require'] = ctx.require
        local_vars['import_class'] = ctx.import_class
        local_vars['clj'] = clj
        local_vars['repl'] = repl

        code.interact(local=local_vars)
        pass

def main():
    parser = argparse.ArgumentParser(description='Run a python shell connecting to a Clojure nREPL')
    parser.add_argument('--host', metavar='host', nargs='?', default='localhost',
                        help='Host of running clojure nREPL (default localhost)')
    parser.add_argument('-p', '--port', metavar='port', nargs='?', default='7002', type=int,
                        help='Port of running clojure nREPL (default 7002)')

    args = parser.parse_args()
    print args

    shell = Shell(host=args.host, port=args.port)
    shell.start()

if __name__ == '__main__':
    main()
