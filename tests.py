import pytest
from traits import Context, AI, DI, EG
from parser import MaraFormulaParser
from collections import namedtuple

t_parser_context = namedtuple('ParserContext', 'parser context')


@pytest.fixture()
def parser():
    ctx = Context()
    ctx.register_namespace('ai', AI)
    ctx.register_namespace('di', DI)
    ctx.register_namespace('eg', EG)
    return MaraFormulaParser(ctx=ctx)


@pytest.fixture()
def par_ctx():
    ctx = Context()
    ctx.register_namespace('ai', AI)
    ctx.register_namespace('di', DI)
    ctx.register_namespace('eg', EG)
    return t_parser_context(MaraFormulaParser(ctx=ctx), ctx)


def test_integers(parser):
    ret = parser.parse('1')
    assert ret.evaluate() == 1


def test_tags_context(par_ctx):
    tag = 'ai.ALFA.value'
    ret = par_ctx.parser.parse('ai.ALFA.value')
    par_ctx.context.update(tag, 1)
    assert ret.evaluate() == 1

    par_ctx.context.update(tag, 2)
    assert ret.evaluate() == 2

def test_function(par_ctx):
    f = 'int(eg.E1289_04.text)'
    ret = par_ctx.parser.parse(f)
    par_ctx.context.update('eg.E1289_04.text', '1')
    assert ret.evaluate() == 1

def test_mult(par_ctx):
    f = '(ai.E4CVV_01.value * ai.E4CVV_01.escala'
    ret = par_ctx.parser.parse(f)
    import ipdb; ipdb.set_trace()

