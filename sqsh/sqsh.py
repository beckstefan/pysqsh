"""pysqsh main module."""

import subprocess

# Separator of columns
COLUMN_SEPARATOR = "|"
ROW_SEPARATOR = "|\n"

# Command line arguments that are always passed
SQSH_KWARGS = {
    'm': 'bcp',  # Do not fill up with whitespace, uses | as separator (not changeable)
}

# The standard width, usually this value is sufficient
WIDTH = 25000


class SQSHResponse:
    """
    SQSHS Response class with attributes for easier usage.
    """

    def __init__(self, c):
        """
        Initialize class.

        :param c: subprocess.CompletedProcess
        """
        self.completed_process = c
        self.stdout = c.stdout

    @property
    def result(self):
        """
        Give the result as it comes from sqsh.
        """
        return self.stdout

    @property
    def rows(self):
        r"""
        Split the result into rows by using '\n|' (the default bcp separator).
        """
        return self.stdout.split(ROW_SEPARATOR)[:-1]

    @property
    def table(self):
        """
        Split the result into cells, i.e. list of list.
        """
        return [row.split(COLUMN_SEPARATOR)[:-1] for row in self.rows]


def call(sql, *arg, encoding='iso-8859-1', width=25000, timeout=30, **kwargs):
    """
    Execute the sqsh commands with the given parameters.

    :param sql: the actual SQL call
    :param encoding: encoding to use when passing the sql call to sqsh
    :param width: width of the line in sqsh output
    """
    if not isinstance(sql, str):
        raise Exception("sql must be of type string")
    if not isinstance(encoding, str):
        raise Exception("endoning must be of type string")
    if not isinstance(width, int):
        raise Exception("width must be of type int")
    if not isinstance(timeout, int) or timeout <= 0:
        raise Exception("timeout must by of type int and >= 1")

    for key, value in kwargs.items():
        if not isinstance(kwargs[key], str):
            raise Exception("{key} in kwargs must be of type string".format(key=key))

    sqsh_args = {key: value for key, value in SQSH_KWARGS.items()}
    # Let's take the arguments from kwargs
    # If they overwrite, that's fine
    sqsh_args.update(kwargs)

    # Set the width
    sqsh_args['w'] = width

    cmd_with_args = ['sqsh'] + ["-{key}{value}".format(key=key, value=value) for key, value in sqsh_args.items()]

    c = subprocess.run(cmd_with_args, input=sql, encoding=encoding, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)

    if c.stderr:
        raise Exception(c.stderr)

    return SQSHResponse(c)
