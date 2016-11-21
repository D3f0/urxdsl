from __future__ import print_function
from ply import lex, yacc


class MaraFormulaLexer(object):
    """
    Lexer for formulas
    """
    __file__ = "formulas"
    tokens = (
        'NUMBER',
        'TAG',
        'PLUS',
        'MULT',
        'MINUS',
        'DIV',
        'FUNC',
        'VAR',
        'LPAREN',
        'RPAREN',
        'COMMA',
        'LESSER',
        'GREATER',
        'EQUAL',
        'FUNCNAME',
        'LAMBDA',
        'COLON',
        'AUXREF',
    )

    t_NUMBER = r'\d+(\.\d+)?'
    t_TAG = r'\w{2}\.[\d\w\_]+\.[\w\d]+'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_DIV = r'\/'
    t_MULT = r'\*'
    t_VAR = r'\w+'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COMMA = r'\,'
    t_LESSER = r'\>'
    t_GREATER = r'\<'
    t_EQUAL = r'=='
    t_FUNCNAME = r'\w[\w\d]+'
    t_LAMBDA = 'lambda'
    t_COLON = ':'
    t_AUXREF = r'\w\.\w[\w\d\_]*'

    t_ignore = ' \t'


#     def t_error(self, t):
#         print("Illegal character '%s'" % t.value[0])
    def __init__(self, ):
        self.lexer = lex.lex(module=self)

    def tokenize(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            yield tok

    def test(self, data, action=print):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            action(tok)


class Expression(object):
    def evaluate(self):
        return NotImplementedError()


class Number(Expression):
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return int(self.value)


class Tag(Expression):
    def __init__(self, value, ctx):
        ns, tag, attr_name = value.split('.')
        self.var = ctx.get_variable(ns, tag)
        self.attr_name = attr_name

    def evaluate(self):
        return getattr(self.var, self.attr_name)


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

class MaraFormulaParser(object):
    precedence = []

    def __init__(self, ctx):
        '''
        Parses text into expression instances
        '''
        self.ctx = ctx
        self.lexer = MaraFormulaLexer()
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(
            module=self,
            write_tables=0,
            debug=False
        )

    def parse(self, data):
        if data:
            return self.parser.parse(data, self.lexer.lexer, 0, 0, None)
        else:
            return []

    def p_error(self, p):
        print ('Error!\n%s\n' % p)

    def p_number(self, p):
        """expr : NUMBER"""
        p[0] = Number(p[1])

    def p_tag(self, p):
        """expr : TAG"""
        p[0] = Tag(p[1], ctx=self.ctx)

    def p_mul(self, p):
        '''expr : expr MULT expr
                | expr PLUS expr
                | expr MINUS expr
                | expr DIV expr
        '''
        p[0] = BinaryOp(p[2], p[1], p[3])


    def p_func(self, p):
        'expr : FUNCNAME LPAREN expr RPAREN'
        import pdb; pdb.set_trace()
        p[0] = Function(p[1], p[3])

    def p_args(self, p):
        'args : expr'
        pass
