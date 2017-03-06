from __future__ import division
from decimal import Decimal
import math
import operator
from collections import Iterable


class IncompleteExpression(Exception):
    pass


class Bottom(object):
    def __init__(self, context):
        self.context = context

    def calculate_value(self):
        return 0

    def apply(self, rvalue):
        return rvalue


class Term(Bottom):
    def __init__(self, expression, location, parseresult):
        self.expression = expression
        self.location = location
        self.parseresult = parseresult
        self.context = None

    def resolve(self, context):
        self.context = context
        return self

    def apply(self, operator):
        value = self.calculate_value()
        operator.bind_lvalue(value)
        return operator


class BoundOperator(Term):
    def __init__(self, value, context):
        self.value = value
        self.context = context

    def calculate_value(self):
        return self.value


class IntegerTerm(Term):

    def calculate_value(self):
        return int(self.parseresult.integer)

class FloatTerm(Term):

    def calculate_value(self):
        return float(self.parseresult.float)


class DecimalTerm(Term):

    def calculate_value(self):
        return Decimal(self.parseresult.decimal)


class VariableTerm(Term):
    def calculate_value(self):
        contextreader = operator.attrgetter(self.parseresult.variable)
        val = contextreader(self.context)
        if callable(val):
            return val()
        else:
            return val


class UnaryOperator(IntegerTerm):
    op_map = {
        '-' : operator.neg,
        '+' : operator.pos,
        '!' : math.factorial,
    }

    def __init__(self, expression, location, parseresult):
        super(UnaryOperator, self).__init__(expression, location, parseresult)
        self.op = self.op_map[self.parseresult.operator]

    def calculate_value(self):
        return self.op(self.lvalue)

    def bind_lvalue(self, lvalue):
        self.lvalue = lvalue

    def apply(self, rvalue):
        value = rvalue.calculate_value()
        return BoundOperator(self.op(value), self.context)


class BinaryOperator(UnaryOperator):
    op_map = {
        '*' : operator.mul,
        '+' : operator.add,
        '/' : operator.truediv,
        '-' : operator.sub,
        '^' : pow
    }

    def calculate_value(self):
        raise IncompleteExpression("Impossible to calculate value for unbound operator")

    def bind_lvalue(self, lvalue):
        self.lvalue = lvalue

    def apply(self, rvalue):
        value = self.op(self.lvalue, rvalue.calculate_value())
        return BoundOperator(value, self.context)


def combine_results(first, second):
    context = first.context
    second.resolve(context)
    return first.apply(second)


class Expression(Term):
    def __repr__(self):
        return "<Expression %s>" % self.parseresult[0]

    def calculate_value(self):
        expression = self.parseresult[0]
        if isinstance(expression, Iterable):
            result = reduce(combine_results, self.parseresult[0], Bottom(self.context))
        else:
            result = expression.resolve(self.context)

        return result.calculate_value()

