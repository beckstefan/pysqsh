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

Results
~~~~~~~

After successful execution, you get an ``SQSHResponse`` back with the following attributes:

* ``result`` The output of sqsh as plain text
* ``rows`` The result is splitted into rows. This is nice, if you have a single column.
* ``table`` The result as cells, i.e. list of list. In case there's no output, this is the list containing the empty list ``[[]]``
* ``first_row`` The first row of the result. This is useful if have just one row anyway.
* ``first_cell`` The first cell of the result. This is useful if you want just a single result.

Exceptions
~~~~~~~~~~

In case that ``sqsh`` returns anything to ``stderr``, an exception will be raised.
Further exceptions may rise form the underlying ``subprocess`` module, hence see that documentation.

Additional Options
~~~~~~~~~~~~~~~~~~

You can pass to ``sqsh.call``:

* ``encoding`` Encoding to use for input and output of sqsh - default is ``iso-8859-1``
* ``width`` Width of output of sqsh. Default is 25000 which should be enough for most use cases. Increase if you expect very long lines.
* ``timeout`` Maximum time to wait for ``sqsh`` to finish. Default is 30 seconds.

Then you can pass extra arguments to ``sqsh.call`` which will be directly passed to ``sqsh`` without any further checks!
By design of ``sqsh``, you can safely pass passwords with ``-P`` as ``sqsh`` will obscure the value for e.g. ``ps``.

How it works
------------

PySQSH is, as stated above, a very simple wrapper around ``sqsh``.
Internally, it calls ``subprocess.run`` and does some post-processing of the result.

To make handling of white spaces robust, PySQSH uses the sqsh style ``bcp``, which as downside gives no output for e.g. ``insert`` statements.
Usually you would except ``(n rows affected)``.
