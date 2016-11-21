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
