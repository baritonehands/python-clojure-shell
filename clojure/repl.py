import clj as edn

def py2clj(value):
    if isinstance(value, Evaluation):
        return value.__expr__()
    else:
        return edn.dumps(value)

def camel_case(s):
    components = s.split('_')
    return components[0] + "".join(x.title() for x in components[1:])

def kebab_case(s):
    return s.replace('__BANG', '!').replace('_', '-')

class Evaluation(object):
    def __init__(self, ctx):
        self.ctx = ctx

    def __repr__(self):
        return str(self.get())

    def __expr__(self):
        raise NotImplementedError()

    def get(self):
        return self.ctx.evaluate(self.__expr__())

class MethodCall(Evaluation):
    def __init__(self, ctx, name, varname, args):
        super(MethodCall, self).__init__(ctx)
        print('MethodCall(%s, %s)' % (name, varname))
        self.name = name
        self.varname = varname
        self.args = args

    def __expr__(self):
        return "(" + " ".join(["." + camel_case(self.name), self.varname] + [py2clj(v) for v in self.args]) + ")"

class FunctionCall(Evaluation):
    def __init__(self, ctx, name, args):
        super(FunctionCall, self).__init__(ctx)
        print('FunctionCall(%s)' % (name, ))
        self.name = name
        self.args = args

    def __expr__(self):
        return "(" + " ".join([self.name] + [py2clj(v) for v in self.args]) +")"

class GetProperty(Evaluation):
    def __init__(self, ctx, name, varname):
        super(GetProperty, self).__init__(ctx)
        print 'GetProperty(%s, %s)' % (name, varname)
        self.name = name
        self.varname = varname

    def __getattr__(self, item):
        return GetProperty(self.ctx, item, self.__expr__())

    def __setattr__(self, key, value):
        if key not in ['ctx', 'name', 'varname']:
            self.ctx.evaluate("(.%s %s %s)" % (camel_case('set_' + key), self.__expr__(), py2clj(value)))
        else:
            super(GetProperty, self).__setattr__(key, value)

    def __call__(self, *args, **kwargs):
        return MethodCall(self.ctx, self.name, self.varname, args)

    def __expr__(self):
        return "(.%s %s)" % (camel_case('get_'+self.name), self.varname)

class Var(Evaluation):
    def __init__(self, ctx, name):
        super(Var, self).__init__(ctx)
        self.name = name

    def __getattr__(self, item):
        return GetProperty(self.ctx, item, self.name)

    def __setattr__(self, key, value):
        if key not in ['ctx', 'name']:
            self.ctx.evaluate("(.%s %s %s)" % (camel_case('set_' + key), self.name, py2clj(value)))
        else:
            super(Var, self).__setattr__(key, value)

    def __call__(self, *args, **kwargs):
        return FunctionCall(self.ctx, self.name, args)

    def __expr__(self):
        return self.name

class NamespaceAlias(Evaluation):
    def __init__(self, ctx, ns):
        super(NamespaceAlias, self).__init__(ctx)
        self.ns = ns

    def __getattr__(self, item):
        return Var(self.ctx, "%s/%s" % (self.ns, kebab_case(item)))

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __repr__(self):
        return "<Namespace %s>" % (self.ns, )

class Context(object):
    def __init__(self, nrepl_client):
        self.nrepl_client = nrepl_client

    def var(self, name, value=None):
        """Reference a remote variable, or declare a new one if value is provided"""
        var = Var(self, name)
        if value is not None:
            print(self.evaluate("(def %s %s)" % (name, py2clj(value))))
        return var

    def new(self, classname, name=None, *args):
        """Instantiate a Java class"""
        if name is None:
            name = self.evaluate("(gensym)")
        var = Var(self, name)
        call = " ".join([classname + '.'] + [py2clj(v) for v in args])
        print(self.evaluate("(def %s (%s))" % (name, call)))
        return var

    def require(self, name, alias=None):
        """Require a Clojure namespace, with optional alias"""
        if alias is None:
            req = "(require '%s)" % (name, )
            res = NamespaceAlias(self, name)
        else:
            req = "(require '[%s :as %s])" % (name, alias)
            res = NamespaceAlias(self, alias)
        self.evaluate(req)
        return res

    def import_class(self, classname):
        """Import a Java class, to use its short name"""
        imp = "(import '%s)" % (classname, )
        return self.evaluate(imp)

    def evaluate(self, code):
        print('Evaluating:', code)
        self.nrepl_client.write(dict(op="eval", code=code))
        return self.readall()

    def readall(self):
        pluck = lambda dict, *args: (dict.get(arg, None) for arg in args)
        ret = None
        while True:
            output = self.nrepl_client.read()
            #print output
            (status, stdout, value, error) = pluck(output, 'status', 'out', 'value', 'err')
            if value is not None:
                try:
                    value = edn.loads(value)
                except ValueError: pass
                if ret is not None: print(repr(ret))
                ret = value
            if stdout is not None:
                print(stdout)
            if error is not None:
                print(error)
            if status is not None and 'done' in status:
                break
        return ret