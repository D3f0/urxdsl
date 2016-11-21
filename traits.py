from __future__ import print_function
from traitlets import Integer, Unicode, Any, HasTraits
import pandas as pd
from sqlalchemy import create_engine
from parser import MaraFormulaLexer

eng = create_engine('postgres://localhost/nguru')

df = pd.read_sql_table('hmi_formula', eng)

FORMULAS = [f.replace('=', '==') for f in df['formula']]


# TODO: Create traits from Model definitions

class AI(HasTraits):
    value = Integer()
    q = Integer()
    tag = Unicode()


class DI(HasTraits):
    value = Integer()
    bit = Integer()


class EG(HasTraits):
    text = Unicode()
    stroke = Unicode()
    fill = Unicode()


class Tag(HasTraits):
    value = Integer()
    type_ = Any()


def split_ns(ns_tag_attr):
    '''Splits'''
    ns, tag, attr = ns_tag_attr.split('.')
    return ns, tag, attr


class Formula(HasTraits):
    # deps = List()
    value = Integer()
    text = Unicode()
    target = Any()

    def __init__(self, ctx, **kwargs):
        '''
        Creates a formula and binds to its dependencies
        '''
        super(Formula, self).__init__(**kwargs)
        self.ctx = ctx
        text = kwargs.get('text', '')
        assert text
        self.bind_to_deps()

    def bind_to_deps(self):
        '''Based on text, find dependencies in context and bind'''
        deps = self.get_dependencies()  # {'ai': {'TAG': ['atr1', 'attr2']}}
        for ns_name, tags in deps.iteritems():
            for tag_name, attr_names in tags.iteritems():
                var = self.ctx.get_variable(ns_name, tag_name)
                var.observe(self.calculate, names=attr_names)

    def get_dependencies(self):
        '''\
        Returns a dict where each key is a list of attributes to be watched.
        Example output: {u'ai': {u'ASD123': [u'q']}, u'di': {u'ASD123': [u'value']}}
        '''
        tokens = self.ctx.lexer.tokenize(self.text)
        tag_tokens = [tok.value for tok in tokens if tok.type == 'TAG']
        result = {}
        for ns_tag_attr in tag_tokens:
            ns_name, tag_name, attr_name = split_ns(ns_tag_attr)
            ns_dict = result.setdefault(ns_name, {})
            # What attribtues have to be watched for a tag
            attributes = ns_dict.setdefault(tag_name, [])
            attributes.append(attr_name)
        return result

    def calculate(self, change):
        print("Calc! %s" % self.text)

    def __str__(self):
        return "{}({})".format(self.text or "NO TEXT", self.deps)

    __repr__ = __str__


class Context(object):

    LEXER_CLASS = MaraFormulaLexer

    def __init__(self):
        self.lexer = self.LEXER_CLASS()
        self.ns_tags = {}
        self.formulae = {}
        # ai -> lambda, di -> lambda
        self.namespace_ctors = {}

    def get_ns(self, name):
        return self.ns_tags[name]

    def get_variable(self, ns_name, tag=None):
        '''
        Gets a variable form a trait namespace.
        If not found, will be created if there's a registered namespace creator
        it'll be called with the tag as first argument.
        '''
        if not tag:
            ns_name, tag = ns_name.split('.')
        assert ns_name in self.namespace_ctors
        ns = self.ns_tags.setdefault(ns_name, {})
        if tag not in ns:
            try:
                trait_creator = self.namespace_ctors[ns_name]
            except KeyError:
                raise ValueError("You need to register a ns, "
                                 "i.e.: ctx.register_namesapce('name', callable)")
            trait = trait_creator(tag)
            ns[tag] = trait

        return ns[tag]

    def add_formula(self, string, destination=None):
        self.formulae[destination or string] = Formula(self, text=string)

    def register_namespace(self, name, trait_constructor):
        assert name not in self.namespace_ctors
        self.namespace_ctors[name] = trait_constructor

    def update(self, path, new_value):
        '''
        This method updates a Traitlet and all Formula traitlets
        that observe that change should be recalculated.
        ai.AABBCC.value 4

        '''
        ns, tag, attr = split_ns(path)
        return setattr(self.get_variable(ns, tag), attr, new_value)
