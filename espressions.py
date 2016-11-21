# Based on the idea exposed in


class Expression(object):
    '''
    Base class for deferred evaluation
    '''
    def evaluate(self, context=None):
        return NotImplementedError()


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self, context=None):
        return int(self.value)


class Tag(Expression):
    def __init__(self, value):
        self.ns, self.tag, self.attr_name = value.split('.')

    def evaluate(self, context=None):
        var = context.get_variable(self.ns, self.tag)
        return getattr(var, self.attr_name)

class BinaryOp(Expression):
    def __init__(self, op, arg1, arg2):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2

    def _evaluate(self):
        pass

class Function(Expression):
    def __init__(self, fname, *args):
        self.fname = fname.upper()
        self.args = args

    def evaluate(self):
        if self.fname == 'INT':
            return int(self.args[0].evaluate())
        raise NotImplementedError()
