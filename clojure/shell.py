from .repl import Context
import argparse, nrepl, code

class Shell(object):
    def __init__(self, host='localhost', port=7002):
        self.nrepl_client = nrepl.connect("nrepl://%s:%d" % (host, port))

    def start(self):
        repl = self.nrepl_client
        client = Context(self.nrepl_client)
        var = client.var
        new = client.new
        require = client.require
        import_class = client.import_class

        code.interact(local=locals())
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
