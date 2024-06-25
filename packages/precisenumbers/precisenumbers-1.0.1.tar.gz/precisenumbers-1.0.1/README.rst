=======
PreciseNumbers
=======

PreciseNumbers provides data structures that can represent numeric values that have a particular
level of precision.


Why PreciseNumbers?
=====

PreciseNumbers was created to fill a void in the Python ecosystem. There is not currently
a mathematically useful and numerically stable way to represent numbers that have a particular level
of precision (i.e., a specific number of relevant values after the decimal). PreciseNumbers is an
effort to solve that problem by representing the different components of the value -- including
its precision -- as integers. PreciseNumbers stores every numeric value as 4 distinct numbers,
a "multiplier", an "integer", a "fractional", and a "precision." The number can then be represented as
M * (I + F / 10^P), where M, I, F, and P correspond to the "multiplier", "integer", "fractional", and
"precision" values, respectively.

While PreciseNumbers uses integers as its "under-the-hood" representation of numeric values, it
facilitates easy access to alternative -- e.g., float and string -- representations.


Usage
=====

Below is a typical example of creating a Coordinate that has a particular precision and then
accessing its float and string representations.

.. code-block:: pycon

    >>> from precisenumbers.coordinates import Coordinate
    >>> location = Coordinate(longitude=90.1, latitude=10.23, precision=3)
    >>> location.longitude
    PreciseNumber(multiplier=1, integer=90, fractional=100, precision=3)
    >>> float(location.longitude)
    90.1
    >>> str(location.longitude)
    '90.100'
    >>> location.longitude.precision
    3


Requirements
============

"Look Ma, no requirements!" Seriously, PreciseNumbers has no external dependencies beyond Python>=3.9.


Installation
=====

The easiest way to install precisenumbers is using `pip`::

    pip install precisenumbers
