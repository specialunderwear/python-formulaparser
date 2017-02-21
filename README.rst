formulaparser
-------------

A formula parser for python.

Copyright (C) 2017  Lars van de Kerkhof

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

what it does
============

Parses simple arythmetic formula's containing variables.
Can then be used to compute values resolving the variables from a context
object.

.. code-block:: python

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
