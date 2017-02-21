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
    VariableTerm,
    UnaryOperator,
    BinaryOperator,
    Expression
)

integer = Word(nums).setParseAction(IntegerTerm).setResultsName('integer')
number = Regex(r"\d+.\d+").setParseAction(FloatTerm).setResultsName('float')
variable = Word(alphas + '.').setParseAction(VariableTerm).setResultsName('variable')
operand = (number | integer | variable)

factop = Literal('!').setParseAction(UnaryOperator).setResultsName('operator')
signop = oneOf('+ -').setParseAction(UnaryOperator).setResultsName('operator')
expop = Literal('^').setParseAction(BinaryOperator).setResultsName('operator')
multop = oneOf('* /').setParseAction(BinaryOperator).setResultsName('operator')
plusop = oneOf('+ -').setParseAction(BinaryOperator).setResultsName('operator')

expression = operatorPrecedence( operand,
    [(factop, 1, opAssoc.LEFT),
     (expop, 2, opAssoc.RIGHT),
     (signop, 1, opAssoc.RIGHT),
     (multop, 2, opAssoc.LEFT),
     (plusop, 2, opAssoc.LEFT),]
    )


formulaparser = expression.setParseAction(Expression).setResultsName('expression')