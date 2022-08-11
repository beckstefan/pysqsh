PySQSH
======

This is a small, not to say: tiny, wrapper around sqsh with focus on further processing in Python.

Installation
------------

PySQSH is a wrapper for ``sqsh`` and thus requires a running version of ``sqsh``.

.. code:: bash

    pip install git+https://github.com/beckstefan/pysqsh.git#pysqsh

Documentation
-------------

Making Queries
~~~~~~~~~~~~~~

Making queries is rather simple.
Depending on your ``.sqshrc`` and your ``Interfaces``, you simply need to pass to SQL statement -- of course including with the ``go`` after a newline.

.. code:: Python3

    import sqsh
    sql = "select row1 from table where row2 = 'spam' \n go"
    try:
        s = sqsh.call(sql)
    except Exception as e:
        # Do something with the exception ...
        pass
    for r in s.rows:
        # Do something with r


The module comes with the following function calls:

* ``call``
* ``raw``
* ``stripped``

They all take the same parameters, but their response objects differ.

Results
~~~~~~~

After successful execution, you get a subclass of an ``SQSHResponse`` back.
Below you find its attributes.

SQSHResponse
''''''''''''
* ``result`` The output of sqsh as plain text

SQSHCallResponse
''''''''''''''''

* ``rows`` The result is splitted into rows. This is nice, if you have a single column.
* ``table`` The result as cells, i.e. list of list. In case there's no output, this is the list containing the empty list ``[[]]``
* ``first_row`` The first row of the result. This is useful if have just one row anyway.
* ``first_cell`` The first cell of the result. This is useful if you want just a single result.

To this achieve we use sqsh style ``-mbcp`` which strips basically everything, but is rather good for processing.

SQSHRawResponse
'''''''''''''''

* ``affected_rows`` The number of affected rows as integer.
* ``affected_row_as_text`` The original output of sqsh about the affected rows.

SQSHStripResponse
'''''''''''''''''

No special attributes, but we called with sqsh with ``-h`` optiona to strip header and footer.

Exceptions
~~~~~~~~~~

In case that ``sqsh`` returns anything to ``stderr``, an exception will be raised.
Further exceptions may rise form the underlying ``subprocess`` module, hence see that documentation.

Additional Options
~~~~~~~~~~~~~~~~~~

You can pass to ``sqsh``:

* ``encoding`` Encoding to use for input and output of sqsh - default is ``iso-8859-1``
* ``width`` Width of output of sqsh. Default is 25000 which should be enough for most use cases. Increase if you expect very long lines.
* ``timeout`` Maximum time to wait for ``sqsh`` to finish. Default is 90 seconds.

Then you can pass extra arguments to ``sqsh.call`` which will be directly passed to ``sqsh`` without any further checks!
By design of ``sqsh``, you can safely pass passwords with ``-P`` as ``sqsh`` will obscure the value for e.g. ``ps``.

How it works
------------

PySQSH is, as stated above, a very simple wrapper around ``sqsh``.
Internally, it calls ``subprocess.run`` and does some post-processing of the result.
