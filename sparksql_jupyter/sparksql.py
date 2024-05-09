import re
from html import escape

from IPython.core.display import HTML
from IPython.core.magic import Magics, cell_magic, magics_class, needs_local_scope
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from pyspark.sql import SparkSession
from pyspark.sql.functions import date_format
from traitlets import Int
from jinja2 import Environment, StrictUndefined


@magics_class
class SparkSql(Magics):
    limit = Int(20, config=True, help='The maximum number of rows to display')
    
    @needs_local_scope
    @cell_magic
    @magic_arguments()
    @argument('variable', nargs='?', type=str, help='Capture dataframe in a local variable')
    @argument('-j', '--jinja', nargs='?', type=str, help='Capture dataframe in a local variable with jinja2 template')
    @argument('-c', '--cache', action='store_true', help='Cache dataframe')
    @argument('-e', '--eager', action='store_true', help='Cache dataframe with eager load')
    @argument('-v', '--view', type=str, help='Create or replace temporary view')
    @argument('-l', '--limit', type=int, help='The maximum number of rows to display')
    def sparksql(self, line='', cell='', local_ns=None):
        if local_ns is None:
            local_ns = {}

        user_ns = self.shell.user_ns.copy()
        user_ns.update(local_ns)

        args = parse_argstring(self.sparksql, line)

        spark = get_instantiated_spark_session()

        if spark is None:
            print("active spark session is not found")
            return

        df = spark.sql(bind_variables(cell, user_ns))
        if args.cache or args.eager:
            print('cache dataframe with %s load' % ('eager' if args.eager else 'lazy'))
            df = df.cache()
            if args.eager:
                df.count()
        if args.view:
            print('create temporary view `%s`' % args.view)
            df.createOrReplaceTempView(args.view)
        if args.variable:
            print('capture dataframe to local variable from jinja template`%s`' % args.variable)
            self.shell.user_ns.update({args.variable: df})

        limit = args.limit or self.limit
        header, contents = get_results(df, limit)
        if len(contents) > limit:
            print('only showing top %d row(s)' % limit)

        html = make_tag('tr',
                        ''.join(map(lambda x: make_tag('td', escape(x), style='font-weight: bold'), header)),
                        style='border-bottom: 1px solid')
        for index, row in enumerate(contents[:limit]):
            html += make_tag('tr', ''.join(map(lambda x: make_tag('td', escape(x)), row)))

        return HTML(make_tag('table', html))


def bind_variables(query, user_ns):
    env = Environment(undefined=StrictUndefined)
    return env.from_string(query).render(user_ns)


def get_results(df, limit):
    def convert_value(value):
        if value is None:
            return 'null'
        return str(value)

    header = df.columns
    for column_name, data_type in df.dtypes:
        if data_type == "timestamp":
            df = df.withColumn(column_name, date_format(df[column_name], "yyyy-MM-dd HH:mm:ss"))
        
    contents = list(map(lambda row: list(map(convert_value, row)), df.take(limit + 1)))

    return header, contents


def make_tag(tag_name, body='', **kwargs):
    attributes = ' '.join(map(lambda x: '%s="%s"' % x, kwargs.items()))
    if attributes:
        return '<%s %s>%s</%s>' % (tag_name, attributes, body, tag_name)
    else:
        return '<%s>%s</%s>' % (tag_name, body, tag_name)


def get_instantiated_spark_session():
    return SparkSession._instantiatedSession
