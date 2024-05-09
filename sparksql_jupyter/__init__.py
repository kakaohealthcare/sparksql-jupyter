__version__ = "0.0.5"

from .sparksql import SparkSql


def load_ipython_extension(ipython):
    ipython.register_magics(SparkSql)
