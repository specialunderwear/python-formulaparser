from pyparsing import (
    Word,
    Literal,
    Regex,
    oneOf,
    nums,
    alphas,
    operatorPrecedence,
    opAssoc,
)

from formulaparser.resolve import (
    IntegerTerm,
    FloatTerm,
    DecimalTerm,
    VariableTerm,
    UnaryOperator,
    BinaryOperator,
    Expression
)

integer = Word(nums).setParseAction(IntegerTerm).setResultsName('integer')
number = Regex(r"\d+.\d+").setParseAction(FloatTerm).setResultsName('float')
decimal = Regex(r"\d+(.\d+)?").setParseAction(DecimalTerm).setResultsName('decimal')
variable = Word(alphas + '.').setParseAction(VariableTerm).setResultsName('variable')

factop = Literal('!').setParseAction(UnaryOperator).setResultsName('operator')
signop = oneOf('+ -').setParseAction(UnaryOperator).setResultsName('operator')
expop = Literal('^').setParseAction(BinaryOperator).setResultsName('operator')
multop = oneOf('* /').setParseAction(BinaryOperator).setResultsName('operator')
plusop = oneOf('+ -').setParseAction(BinaryOperator).setResultsName('operator')

# there are 2 options, the parser can generate decimals or floats and ints.
floatclause = (number | integer | variable)
decimalclause = (decimal | variable)


def make_parser(clause):
    expression = operatorPrecedence( clause,
    [(factop, 1, opAssoc.LEFT),
     (expop, 2, opAssoc.RIGHT),
     (signop, 1, opAssoc.RIGHT),
     (multop, 2, opAssoc.LEFT),
     (plusop, 2, opAssoc.LEFT),]
    )

    return  expression.setParseAction(Expression).setResultsName('expression')
