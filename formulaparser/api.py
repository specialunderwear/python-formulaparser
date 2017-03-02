from formulaparser.parser import make_parser, floatclause, decimalclause


class Formula(object):
    """
    >>> from argparse import Namespace as KeyedObject
    >>> from formulaparser import Formula
    >>>
    >>> context = KeyedObject()
    >>> context.four = 4
    >>> context.three = 3
    >>> deepercontext = KeyedObject()
    >>> deepercontext.ten = 10
    >>> deepercontext.twelve = 12
    >>> context.nextlevel = deepercontext
    >>>
    >>> Formula("((1 + 2 + 3) + 4 + (3 + 7)) + 5").calculate_value()
    25
    >>> Formula("4!").calculate_value()
    24
    >>> Formula("3.287 / 6").calculate_value()
    0.5478333333333333
    >>> Formula("2 ^ 8").calculate_value()
    256
    >>> Formula("4 - (-4)").calculate_value()
    8
    >>> Formula("(4 * 6) - 8 + 7 - 4 + 3").calculate_value()
    22
    >>> Formula("((1 + four + 3) + nextlevel.ten + (3 + 7)) + 5").calculate_value(context)
    33
    >>> Formula("((four!) - 6) / nextlevel.twelve").calculate_value(context)
    1.5
    >>> Formula("2 ^ three").calculate_value(context)
    8
    >>> Formula("nextlevel.twelve - (-four)").calculate_value(context)
    16
    >>> Formula("(four * 6) - nextlevel.ten + 7 - 4 + 3").calculate_value(context)
    20
    """
    formulaparser = make_parser(floatclause)

    def __init__(self, formula):
        self.formula = formula
        self._parsed_formula = self.formulaparser.parseString(formula, parseAll=True)

    def __repr__(self):
        return "<Formula %s>" % self.formula

    def calculate_value(self, context=None):
        expression = self._parsed_formula.expression
        bound_expression = expression.resolve(context)
        return bound_expression.calculate_value()


class DecimalFormula(Formula):
    formulaparser = make_parser(decimalclause)
