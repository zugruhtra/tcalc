=====
tcalc
=====

CLI calculator with support of time expressions

~~~~~~~~
Examples
~~~~~~~~

.. code-block:: bash

	$ tcalc "(1:: + :45: + :15:) / 2"
	> 01:00:00
	$ tcalc "2:30: * 3"
	> 07:30:00		

~~~~
TODO
~~~~

* The expression "+ 1:: 1::" can be evaluated as an infix expression, although
  it is clearly not! The implementation of a fix is unclear...
