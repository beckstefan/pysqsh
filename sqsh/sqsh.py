"""pysqsh main module."""

import re
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


class SQSHCallResponse(SQSHResponse):
    """
    SQSH Response for call function.
    """

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
        return [row.split(COLUMN_SEPARATOR) for row in self.rows]

    @property
    def first_row(self):
        """
        Return the first row, splitted.
        """
        return self.stdout.split(ROW_SEPARATOR, 1)[0].split(COLUMN_SEPARATOR)

    @property
    def first_cell(self):
        """
        Return the first cell.
        """
        return self.first_row[0]


class SQSHRawResponse(SQSHResponse):
    """
    SQSHResponse for raw function.
    """

    @property
    def affected_rows(self):
        """
        Return the number of affected rows.
        """
        rows_affected = int(re.search(r'\d+', self.affected_rows_as_text).group(0))
        return rows_affected

    @property
    def affected_rows_as_text(self):
        """
        Return the number of affected rows as text as coming from sqsh.
        """
        return self.stdout.split('\n')[-2]


class SQSHStripResponse(SQSHResponse):
    """
    SQSHResponse for strip function that disables headers and rowcount.
    """

    pass


def execute_sql(sql, *args, encoding='iso-8859-1', width=25000, timeout=90, **kwargs):
    """
    Execute the sqsh commands with the given parameters.

    :param sql: the actual SQL call
    :param encoding: encoding to use when passing the sql call to sqsh
    :param width: width of the line in sqsh output
    """
    if not isinstance(sql, str):
        raise Exception("sql must be of type string")
    if not isinstance(encoding, str):
        raise Exception("encoding must be of type string")
    if not isinstance(width, int):
        raise Exception("width must be of type int")
    if not isinstance(timeout, int) or timeout <= 0:
        raise Exception("timeout must by of type int and >= 1")

    for key, value in kwargs.items():
        if not isinstance(kwargs[key], str):
            raise Exception("{key} in kwargs must be of type string".format(key=key))

    sqsh_args = {
        'w': width,
    }
    sqsh_args.update(kwargs)

    cmd_with_args = ['sqsh'] + ["-{key}{value}".format(key=key, value=value) for key, value in sqsh_args.items()]

    c = subprocess.run(cmd_with_args, input=sql, encoding=encoding, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout, check=True)

    if c.stderr:
        raise Exception(c.stderr)

    return c


def strip(sql, *args, **kwargs):
    """
    Execute the sqsh commands with the given parameters and set -h.

    This is great if you like the plan data and do formatting already in SQL.
    """
    kwargs['h'] = ''

    c = execute_sql(sql, *args, **kwargs)

    return SQSHStripResponse(c)


def call(sql, *args, **kwargs):
    """
    Execute the sqsh commands with the given parameters and set -mbcp.

    This is really good for processing the result with Python as the response will have nice attributes.
    """
    kwargs['m'] = 'bcp'

    c = execute_sql(sql, *args, **kwargs)

    return SQSHCallResponse(c)


def raw(sql, *args, **kwargs):
    """
    Execute the sqsh commands with the given parameters.

    This is really good if you want to know about the affected rows.
    """
    c = execute_sql(sql, *args, **kwargs)

    return SQSHRawResponse(c)
