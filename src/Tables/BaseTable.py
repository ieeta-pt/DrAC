import pandas as pd

class BaseTable(object):
    """Class base to build the table mapping.

    Constructor arguments:
    :param table:        destination table name
    :param content:      the content sctrutured to be written in a CSV or the database
    """
    def __init__(self, table, content=None ):
        self.table           = table
        self.content         = content

    #####################
    ### Class methods ###
    #####################
    def getDataTypesForSQL(table):
        for cls in BaseTable.__subclasses__():
            if(cls.__name__.lower() == table):
                return cls.getDataTypesForSQL()
        return {}
   