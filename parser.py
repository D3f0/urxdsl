from __future__ import print_function
from ply import yacc
import expressions
from lexer import MaraFormulaLexer


class MaraFormulaParser(object):
    precedence = []

    def __init__(self, ctx):
        '''
        Parses text into expression instances
        '''
        self.ctx = ctx
        # TODO: Make this pluggable
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
        p[0] = expressions.Number(p[1])

    def p_tag(self, p):
        """expr : TAG"""
        p[0] = expressions.Tag(p[1], ctx=self.ctx)

    def p_mul(self, p):
        '''expr : expr MULT expr
                | expr PLUS expr
                | expr MINUS expr
                | expr DIV expr
        '''
        p[0] = expressions.BinaryOp(p[2], p[1], p[3])

    def p_func(self, p):
        'expr : FUNCNAME LPAREN expr RPAREN'
        import pdb; pdb.set_trace()
        p[0] = expressions.Function(p[1], p[3])

    def p_args(self, p):
        'args : expr'
        pass
